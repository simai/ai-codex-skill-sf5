#!/usr/bin/env python3
"""
Compute a lightweight visual similarity score for the Tailwind -> SF5 lab.

The score compares the first visible source/SF5 panel pair in the lab
screenshot. It is intentionally heuristic: use it as a regression signal, not
as a final visual-approval substitute.
"""

from __future__ import annotations

import argparse
import json
import struct
import zlib
from pathlib import Path


def paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def read_png_rgb(path: Path) -> tuple[int, int, list[tuple[int, int, int]]]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a PNG file")
    pos = 8
    width = height = 0
    color_type = -1
    bit_depth = -1
    compressed = bytearray()
    while pos < len(data):
        length = struct.unpack(">I", data[pos : pos + 4])[0]
        chunk_type = data[pos + 4 : pos + 8]
        chunk_data = data[pos + 8 : pos + 8 + length]
        pos += 12 + length
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type = struct.unpack(">IIBB", chunk_data[:10])
        elif chunk_type == b"IDAT":
            compressed.extend(chunk_data)
        elif chunk_type == b"IEND":
            break
    if bit_depth != 8 or color_type not in {2, 6}:
        raise ValueError(f"Unsupported PNG format: bit_depth={bit_depth}, color_type={color_type}")
    channels = 4 if color_type == 6 else 3
    raw = zlib.decompress(bytes(compressed))
    stride = width * channels
    pixels: list[tuple[int, int, int]] = []
    previous = bytearray(stride)
    offset = 0
    for _row in range(height):
        filter_type = raw[offset]
        offset += 1
        scanline = bytearray(raw[offset : offset + stride])
        offset += stride
        for i in range(stride):
            left = scanline[i - channels] if i >= channels else 0
            up = previous[i]
            upper_left = previous[i - channels] if i >= channels else 0
            if filter_type == 1:
                scanline[i] = (scanline[i] + left) & 0xFF
            elif filter_type == 2:
                scanline[i] = (scanline[i] + up) & 0xFF
            elif filter_type == 3:
                scanline[i] = (scanline[i] + ((left + up) // 2)) & 0xFF
            elif filter_type == 4:
                scanline[i] = (scanline[i] + paeth(left, up, upper_left)) & 0xFF
            elif filter_type != 0:
                raise ValueError(f"Unsupported PNG filter: {filter_type}")
        for x in range(width):
            start = x * channels
            pixels.append((scanline[start], scanline[start + 1], scanline[start + 2]))
        previous = scanline
    return width, height, pixels


def average_hash(
    width: int,
    height: int,
    pixels: list[tuple[int, int, int]],
    crop: tuple[int, int, int, int],
    size: int = 32,
) -> list[float]:
    x0, y0, x1, y1 = crop
    x0 = max(0, min(width - 1, x0))
    y0 = max(0, min(height - 1, y0))
    x1 = max(x0 + 1, min(width, x1))
    y1 = max(y0 + 1, min(height, y1))
    result: list[float] = []
    for gy in range(size):
        for gx in range(size):
            sx0 = x0 + (x1 - x0) * gx // size
            sx1 = x0 + (x1 - x0) * (gx + 1) // size
            sy0 = y0 + (y1 - y0) * gy // size
            sy1 = y0 + (y1 - y0) * (gy + 1) // size
            total = 0.0
            count = 0
            for y in range(sy0, max(sy0 + 1, sy1)):
                row_offset = y * width
                for x in range(sx0, max(sx0 + 1, sx1)):
                    r, g, b = pixels[row_offset + x]
                    total += 0.299 * r + 0.587 * g + 0.114 * b
                    count += 1
            result.append(total / max(1, count))
    return result


def luminance_stats(
    width: int,
    height: int,
    pixels: list[tuple[int, int, int]],
    crop: tuple[int, int, int, int],
) -> dict[str, float | int]:
    x0, y0, x1, y1 = crop
    x0 = max(0, min(width - 1, x0))
    y0 = max(0, min(height - 1, y0))
    x1 = max(x0 + 1, min(width, x1))
    y1 = max(y0 + 1, min(height, y1))
    values: list[float] = []
    dark = 0
    light = 0
    for y in range(y0, y1):
        row_offset = y * width
        for x in range(x0, x1):
            r, g, b = pixels[row_offset + x]
            value = 0.299 * r + 0.587 * g + 0.114 * b
            values.append(value)
            if value < 16:
                dark += 1
            if value > 245:
                light += 1
    count = max(1, len(values))
    mean = sum(values) / count
    variance = sum((value - mean) ** 2 for value in values) / count
    return {
        "mean": round(mean, 2),
        "stddev": round(variance**0.5, 2),
        "darkRatio": round(dark / count, 4),
        "lightRatio": round(light / count, 4),
        "pixelCount": count,
    }


def integrity_check(stats: dict[str, dict[str, float | int]]) -> dict[str, object]:
    failures: list[str] = []
    full = stats["full"]
    source = stats["source"]
    sf5 = stats["sf5"]
    if float(full["mean"]) < 24 and float(full["stddev"]) < 12:
        failures.append("Screenshot appears blank or nearly black.")
    if float(source["mean"]) < 24 or float(sf5["mean"]) < 24:
        failures.append("A comparison crop is too dark for a reliable visual score.")
    if float(source["stddev"]) < 2 and float(sf5["stddev"]) < 2:
        failures.append("Both comparison crops have near-zero visual variance.")
    if float(full["darkRatio"]) > 0.92:
        failures.append("Screenshot is dominated by dark pixels.")
    return {
        "ok": not failures,
        "failures": failures,
        "policy": "Reject near-black, blank, or zero-variance screenshots before using similarity score.",
    }


def similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Hash sizes differ")
    diff = sum(abs(a - b) for a, b in zip(left, right)) / (len(left) * 255)
    return max(0.0, min(1.0, 1.0 - diff))


def main() -> int:
    parser = argparse.ArgumentParser(description="Score visual similarity for the Tailwind to SF5 lab screenshot.")
    parser.add_argument("screenshot", help="PNG screenshot path")
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args()

    screenshot = Path(args.screenshot).expanduser().resolve()
    width, height, pixels = read_png_rgb(screenshot)
    full_crop = (0, 0, width, height)
    left_crop = (int(width * 0.04), int(height * 0.23), int(width * 0.49), int(height * 0.80))
    right_crop = (int(width * 0.51), int(height * 0.23), int(width * 0.96), int(height * 0.80))
    score = similarity(average_hash(width, height, pixels, left_crop), average_hash(width, height, pixels, right_crop))
    stats = {
        "full": luminance_stats(width, height, pixels, full_crop),
        "source": luminance_stats(width, height, pixels, left_crop),
        "sf5": luminance_stats(width, height, pixels, right_crop),
    }
    integrity = integrity_check(stats)
    payload = {
        "ok": bool(integrity["ok"]),
        "score": round(score, 4),
        "scorePercent": round(score * 100, 2),
        "method": "grayscale-average-hash-crop-diff",
        "screenshot": screenshot.as_posix(),
        "image": {"width": width, "height": height},
        "crops": {"source": left_crop, "sf5": right_crop},
        "integrity": integrity,
        "luminanceStats": stats,
        "notes": [
            "Heuristic score for the first visible source/SF5 panel pair.",
            "Use as a regression signal together with browser DOM smoke and human visual review.",
        ],
    }
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
