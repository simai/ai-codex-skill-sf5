#!/usr/bin/env node
/**
 * SF5 HTML validator (classes & tokens).
 *
 * Usage:
 *   node validate-sf5-html.js path/to/file.html
 *
 * Checks:
 * - all class names exist in registries/classes.sf.json
 * - inline styles do not contain unknown --sf-* tokens
 */
'use strict';

const fs = require('fs');
const path = require('path');

function loadJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

const file = process.argv[2];
if (!file) {
  console.error('Usage: node validate-sf5-html.js path/to/file.html');
  process.exit(2);
}

const baseDir = path.resolve(__dirname, '..');
const classesDb = loadJson(path.join(baseDir, 'registries', 'classes.sf.json')).classes;
const tokensJson = loadJson(path.join(baseDir, 'manifest', 'sf5.tokens.sf.json'));
const tokensDb = new Set(Object.keys(tokensJson.sfTokens || {}));

const html = fs.readFileSync(file, 'utf8');

// Extract class attributes (naive but effective for CI)
const classRe = /class\s*=\s*(?:"([^"]+)"|\'([^\']+)\')/g;
const unknownClasses = new Set();
let m;
while ((m = classRe.exec(html)) !== null) {
  const raw = (m[1] ?? m[2] ?? '').trim();
  if (!raw) continue;
  raw.split(/\s+/).forEach(cls => {
    if (!classesDb[cls]) {
      unknownClasses.add(cls);
    }
  });
}

// Extract inline styles for --sf-* tokens
const styleRe = /style\s*=\s*(?:"([^"]+)"|\'([^\']+)\')/g;
const unknownTokens = new Set();
const tokenRe = /(--sf-[a-zA-Z0-9\-\/_\\]+)/g;
while ((m = styleRe.exec(html)) !== null) {
  const style = (m[1] ?? m[2] ?? '');
  let t;
  while ((t = tokenRe.exec(style)) !== null) {
    const token = t[1];
    if (!tokensDb.has(token)) {
      unknownTokens.add(token);
    }
  }
}

if (unknownClasses.size || unknownTokens.size) {
  if (unknownClasses.size) {
    console.error('Unknown classes:');
    console.error([...unknownClasses].sort().join('\n'));
  }
  if (unknownTokens.size) {
    console.error('Unknown --sf-* tokens in inline styles:');
    console.error([...unknownTokens].sort().join('\n'));
  }
  process.exit(1);
}

console.log('OK: SF5 HTML validated');
