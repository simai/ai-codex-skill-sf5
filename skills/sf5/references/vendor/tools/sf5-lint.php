<?php

declare(strict_types=1);

/**
 * SF5 HTML Linter.
 *
 * Проверяет:
 * 1) что все CSS-классы в HTML существуют в `catalog-lite.json` (или в `catalog-lite.sf-only.json`);
 * 2) что все значения `sf-code="..."` (если используются) входят в список допустимых smart-компонентов;
 * 3) что inline-style не содержит неизвестных `--sf-*` токенов (если включена проверка токенов).
 *
 * Usage:
 * php sf5-lint.php --catalog=/path/to/catalog-lite.sf-only.json --file=/path/to/file.html \
 *   [--smart=/path/to/sf5.smart.json] [--no-smart] \
 *   [--tokens=/path/to/sf5.tokens.sf.json] [--no-tokens] \
 *   [--exclude=/path/to/sf5.excluded-non-sf-classes.json]
 *
 * Exit codes:
 * 0 - OK
 * 1 - Найдены неизвестные классы / sf-code / --sf-* токены
 * 2 - Ошибка аргументов/чтения/JSON
 */

final class Sf5Linter
{
    /**
     * @var array<string, true>
     */
    private array $knownClasses = [];

    /**
     * @var array<string, true>
     */
    private array $allowedSfCodes = [];

    /**
     * @var array<string, true>
     */
    private array $knownTokens = [];

    /**
     * @var array<string, true>
     */
    private array $excludedClasses = [];

    /**
     * @param array<string, mixed> $catalog
     * @param list<string> $allowedSfCodes
     * @param list<string> $knownTokens
     * @param list<string> $excludedClasses
     */
    public function __construct(array $catalog, array $allowedSfCodes = [], array $knownTokens = [], array $excludedClasses = [])
    {
        $this->excludedClasses = $this->buildStringSet($excludedClasses);
        $this->knownClasses = $this->buildKnownClassMap($catalog);
        $this->allowedSfCodes = $this->buildStringSet($allowedSfCodes);
        $this->knownTokens = $this->buildStringSet($knownTokens);
    }

    /**
     * @param string $html
     * @param bool $checkSmart
     * @param bool $checkTokens
     * @return array{
     *     unknown_classes: list<string>,
     *     unknown_sf_codes: list<string>,
     *     unknown_tokens: list<string>,
     *     used_classes: list<string>,
     *     used_sf_codes: list<string>,
     *     used_tokens: list<string>
     * }
     */
    public function lintHtml(string $html, bool $checkSmart = true, bool $checkTokens = true): array
{
    $usedClasses = [];
    $unknownClasses = [];

    $usedSfCodes = [];
    $unknownSfCodes = [];

    $usedTokens = [];
    $unknownTokens = [];

    $tokenPattern = '/(--sf-[A-Za-z0-9\-\/_\\\\]+)/';

    $canUseDom = class_exists('DOMDocument') && class_exists('DOMXPath');

    if ($canUseDom) {
        $dom = new DOMDocument();
        libxml_use_internal_errors(true);
        $dom->loadHTML($html, LIBXML_NOERROR | LIBXML_NOWARNING);
        libxml_clear_errors();

        $xpath = new DOMXPath($dom);

        $classNodes = $xpath->query('//*[@class]');

        if ($classNodes !== false) {
            foreach ($classNodes as $node) {
                $attr = $node->attributes?->getNamedItem('class');
                $classAttr = $attr !== null ? (string) $attr->nodeValue : '';
                $parts = preg_split('/\s+/', trim($classAttr)) ?: [];

                foreach ($parts as $cls) {
                    if ($cls === '') {
                        continue;
                    }

                    $usedClasses[$cls] = $cls;

                    if (!isset($this->knownClasses[$cls])) {
                        $unknownClasses[$cls] = $cls;
                    }
                }
            }
        }

        if ($checkSmart) {
            $sfNodes = $xpath->query('//*[@sf-code]');

            if ($sfNodes !== false) {
                foreach ($sfNodes as $node) {
                    $attr = $node->attributes?->getNamedItem('sf-code');
                    $code = $attr !== null ? (string) $attr->nodeValue : '';

                    if ($code === '') {
                        continue;
                    }

                    $usedSfCodes[$code] = $code;

                    if (!isset($this->allowedSfCodes[$code])) {
                        $unknownSfCodes[$code] = $code;
                    }
                }
            }
        }

        if ($checkTokens && $this->knownTokens !== []) {
            $styleNodes = $xpath->query('//*[@style]');

            if ($styleNodes !== false) {
                foreach ($styleNodes as $node) {
                    $attr = $node->attributes?->getNamedItem('style');
                    $style = $attr !== null ? (string) $attr->nodeValue : '';

                    if ($style === '') {
                        continue;
                    }

                    if (preg_match_all($tokenPattern, $style, $m) > 0) {
                        foreach ($m[1] as $token) {
                            $usedTokens[$token] = $token;

                            if (!isset($this->knownTokens[$token])) {
                                $unknownTokens[$token] = $token;
                            }
                        }
                    }
                }
            }
        }
    } else {
        // Regex fallback (works without ext-dom). Less strict than DOM parsing, but good enough for CI.
        if (preg_match_all('/\bclass\s*=\s*(?:"([^"]*)"|\'([^\']*)\')/i', $html, $m) > 0) {
            $vals = array_merge($m[1], $m[2]);

            foreach ($vals as $classAttr) {
                $parts = preg_split('/\s+/', trim((string) $classAttr)) ?: [];

                foreach ($parts as $cls) {
                    if ($cls === '') {
                        continue;
                    }

                    $usedClasses[$cls] = $cls;

                    if (!isset($this->knownClasses[$cls])) {
                        $unknownClasses[$cls] = $cls;
                    }
                }
            }
        }

        if ($checkSmart) {
            if (preg_match_all('/\bsf-code\s*=\s*(?:"([^"]*)"|\'([^\']*)\')/i', $html, $m) > 0) {
                $vals = array_merge($m[1], $m[2]);

                foreach ($vals as $code) {
                    $code = (string) $code;

                    if ($code === '') {
                        continue;
                    }

                    $usedSfCodes[$code] = $code;

                    if (!isset($this->allowedSfCodes[$code])) {
                        $unknownSfCodes[$code] = $code;
                    }
                }
            }
        }

        if ($checkTokens && $this->knownTokens !== []) {
            if (preg_match_all('/\bstyle\s*=\s*(?:"([^"]*)"|\'([^\']*)\')/i', $html, $m) > 0) {
                $vals = array_merge($m[1], $m[2]);

                foreach ($vals as $style) {
                    $style = (string) $style;

                    if ($style === '') {
                        continue;
                    }

                    if (preg_match_all($tokenPattern, $style, $mm) > 0) {
                        foreach ($mm[1] as $token) {
                            $usedTokens[$token] = $token;

                            if (!isset($this->knownTokens[$token])) {
                                $unknownTokens[$token] = $token;
                            }
                        }
                    }
                }
            }
        }
    }

    ksort($usedClasses);
    ksort($unknownClasses);
    ksort($usedSfCodes);
    ksort($unknownSfCodes);
    ksort($usedTokens);
    ksort($unknownTokens);

    return [
        'unknown_classes' => array_values($unknownClasses),
        'unknown_sf_codes' => array_values($unknownSfCodes),
        'unknown_tokens' => array_values($unknownTokens),
        'used_classes' => array_values($usedClasses),
        'used_sf_codes' => array_values($usedSfCodes),
        'used_tokens' => array_values($usedTokens),
    ];
}

    /**
     * @param array<string, mixed> $catalog
     * @return array<string, true>
     */
    private function buildKnownClassMap(array $catalog): array
    {
        $known = [];

        // catalog-lite.json: classes is a list of strings
        $classes = $catalog['classes'] ?? null;

        if (is_array($classes)) {
            foreach ($classes as $cls) {
                if (is_string($cls) && $cls !== '') {
                    $known[$cls] = true;
                }
            }
        }

        // fallback: manifest/sf5.class-meta.min.json: classes is a map
        $classesMap = $catalog['classesMap'] ?? null;

        if (is_array($classesMap)) {
            foreach ($classesMap as $cls => $_meta) {
                if (is_string($cls) && $cls !== '') {
                    $known[$cls] = true;
                }
            }
        }

        // Remove excluded non-SF classes
        foreach ($this->excludedClasses as $cls => $_true) {
            unset($known[$cls]);
        }

        return $known;
    }

    /**
     * @param list<string> $items
     * @return array<string, true>
     */
    private function buildStringSet(array $items): array
    {
        $map = [];

        foreach ($items as $item) {
            if (is_string($item) && $item !== '') {
                $map[$item] = true;
            }
        }

        return $map;
    }
}

/**
 * @param array<int, string> $argv
 * @return array{catalog: string, file: string, smart: string, tokens: string, exclude: string, noSmart: bool, noTokens: bool}
 */
function parseArgs(array $argv): array
{
    $catalog = '';
    $file = '';
    $smart = '';
    $tokens = '';
    $exclude = '';
    $noSmart = false;
    $noTokens = false;

    foreach ($argv as $arg) {
        if (str_starts_with($arg, '--catalog=')) {
            $catalog = (string) substr($arg, strlen('--catalog='));
        }

        if (str_starts_with($arg, '--file=')) {
            $file = (string) substr($arg, strlen('--file='));
        }

        if (str_starts_with($arg, '--smart=')) {
            $smart = (string) substr($arg, strlen('--smart='));
        }

        if (str_starts_with($arg, '--tokens=')) {
            $tokens = (string) substr($arg, strlen('--tokens='));
        }

        if (str_starts_with($arg, '--exclude=')) {
            $exclude = (string) substr($arg, strlen('--exclude='));
        }

        if ($arg === '--no-smart') {
            $noSmart = true;
        }

        if ($arg === '--no-tokens') {
            $noTokens = true;
        }
    }

    return [
        'catalog' => $catalog,
        'file' => $file,
        'smart' => $smart,
        'tokens' => $tokens,
        'exclude' => $exclude,
        'noSmart' => $noSmart,
        'noTokens' => $noTokens,
    ];
}

/**
 * @param string $path
 * @return array<string, mixed>
 * @throws RuntimeException
 */
function readJsonFile(string $path): array
{
    $raw = file_get_contents($path);

    if ($raw === false) {
        throw new RuntimeException("Cannot read file: {$path}");
    }

    $json = json_decode($raw, true);

    if (!is_array($json)) {
        throw new RuntimeException("File is not valid JSON: {$path}");
    }

    return $json;
}

$args = parseArgs($argv);

if ($args['catalog'] === '' || $args['file'] === '') {
    fwrite(
        STDERR,
        "Usage: php sf5-lint.php --catalog=/path/to/catalog-lite.sf-only.json --file=/path/to/file.html "
        . "[--smart=/path/to/sf5.smart.json] [--no-smart] "
        . "[--tokens=/path/to/sf5.tokens.sf.json] [--no-tokens] "
        . "[--exclude=/path/to/sf5.excluded-non-sf-classes.json]\n"
    );
    exit(2);
}

try {
    $catalog = readJsonFile($args['catalog']);
} catch (RuntimeException $e) {
    fwrite(STDERR, $e->getMessage() . "\n");
    exit(2);
}

$html = file_get_contents($args['file']);

if ($html === false) {
    fwrite(STDERR, "Cannot read file: {$args['file']}\n");
    exit(2);
}

// Default list (generated from manifest/sf5.smart.json)
$allowedSfCodes = [
    'accordion', 'ajax', 'button', 'buttons', 'cards', 'close', 'contentDivider', 'debug',
    'edit', 'icons', 'inputs', 'list', 'news', 'pagination', 'search', 'select', 'sfAccordion',
    'span', 'table', 'tabs', 'tags', 'text', 'textarea',
];

if ($args['smart'] !== '') {
    try {
        $smart = readJsonFile($args['smart']);
        $smartList = $smart['smart'] ?? [];

        if (is_array($smartList)) {
            $codes = [];
            foreach ($smartList as $item) {
                if (is_array($item) && isset($item['sf_code']) && is_string($item['sf_code'])) {
                    $codes[] = $item['sf_code'];
                }
            }
            $allowedSfCodes = $codes;
        }
    } catch (RuntimeException $e) {
        fwrite(STDERR, $e->getMessage() . "\n");
        exit(2);
    }
}

// Tokens list (manifest/sf5.tokens.sf.json)
$knownTokens = [];

if (!$args['noTokens']) {
    $tokensPath = $args['tokens'];

    if ($tokensPath === '') {
        $guess = __DIR__ . '/../manifest/sf5.tokens.sf.json';
        if (file_exists($guess)) {
            $tokensPath = $guess;
        }
    }

    if ($tokensPath !== '') {
        try {
            $tokensJson = readJsonFile($tokensPath);
            $sfTokens = $tokensJson['sfTokens'] ?? [];

            if (is_array($sfTokens)) {
                $knownTokens = array_keys($sfTokens);
            }
        } catch (RuntimeException $e) {
            fwrite(STDERR, $e->getMessage() . "\n");
            exit(2);
        }
    }
}

// Excluded non-SF classes (optional)
$excludedClasses = [];
$excludePath = $args['exclude'];

if ($excludePath === '') {
    $guess = __DIR__ . '/../manifest/sf5.excluded-non-sf-classes.json';
    if (file_exists($guess)) {
        $excludePath = $guess;
    }
}

if ($excludePath !== '') {
    try {
        $excludeJson = readJsonFile($excludePath);
        $excl = $excludeJson['excludedNonSfClasses'] ?? [];

        if (is_array($excl)) {
            $excludedClasses = array_keys($excl);
        }
    } catch (RuntimeException $e) {
        fwrite(STDERR, $e->getMessage() . "\n");
        exit(2);
    }
}

$linter = new Sf5Linter($catalog, $allowedSfCodes, $knownTokens, $excludedClasses);
$result = $linter->lintHtml($html, !$args['noSmart'], !$args['noTokens']);

$hasErrors = false;

if ($result['unknown_classes'] !== []) {
    $hasErrors = true;
    fwrite(STDERR, "Unknown SF5 classes:\n");

    foreach ($result['unknown_classes'] as $cls) {
        fwrite(STDERR, "  - {$cls}\n");
    }
}

if (!$args['noSmart'] && $result['unknown_sf_codes'] !== []) {
    $hasErrors = true;
    fwrite(STDERR, "Unknown sf-code values:\n");

    foreach ($result['unknown_sf_codes'] as $code) {
        fwrite(STDERR, "  - {$code}\n");
    }
}

if (!$args['noTokens'] && $result['unknown_tokens'] !== []) {
    $hasErrors = true;
    fwrite(STDERR, "Unknown --sf-* tokens in inline styles:\n");

    foreach ($result['unknown_tokens'] as $token) {
        fwrite(STDERR, "  - {$token}\n");
    }
}

if ($hasErrors) {
    exit(1);
}

fwrite(STDOUT, "OK: SF5 classes, sf-code and tokens are valid.\n");
exit(0);
