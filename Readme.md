```markdown
# Cyrillic Analyzer and Replacer

Utility for detecting and replacing Russian-language content in text files with flexible reporting options.

## Features

- Detect Russian phrases in text files
- Two search modes:
  - Individual words/phrases (default)
  - Full lines between first/last Cyrillic characters (`-a`)
- Report formats:
  - Text (default)
  - JSON (`-j`) with compact formatting
- Replacement function with backup (`-r`)

## Installation

Requires Python 3.6+:

```bash
git clone https://github.com/your-repo/cyrillic-analyzer.git
cd cyrillic-analyzer
```

## Usage

### Basic Commands

```bash
# Analyze file (text report)
python cyrillic_analyzer.py input.txt

# Analyze with JSON report
python cyrillic_analyzer.py input.txt -j

# Analyze in full-line mode
python cyrillic_analyzer.py input.txt -a
```

### Advanced Options

```bash
# Create named report
python cyrillic_analyzer.py input.txt -o custom_report.json -j

# Apply replacements from report
python cyrillic_analyzer.py input.txt -r -o report.json

# Combined analysis (full-line + JSON)
python cyrillic_analyzer.py input.txt -a -j
```

## JSON Report Format

Example structure:

```json
{
"filename": "example.txt",
"mode": "phrases",
"entries": [
{"line":1,"position":0,"length":6,"include":"Привет","replace":""},
{"line":1,"position":7,"length":5,"include":"мир","replace":""}
]
}
```

Fields:
- `line`: Line number (1-based)
- `position`: Character position (0-based)
- `length`: Phrase length
- `include`: Found text
- `replace`: Replacement field (empty by default)

## Best Practices

1. First create report:
```bash
python cyrillic_analyzer.py document.txt -j -o analysis.json
```

2. Edit JSON file, fill `replace` fields as needed

3. Apply changes:
```bash
python cyrillic_analyzer.py document.txt -r -o analysis.json
```

## Feedback

Found a bug or have suggestions? Create an issue in the project repository.


## 🌍 Available Translations | Доступные переводы | 可用翻译
- 🇬🇧 [English](Readme.md) - English version  
- 🇷🇺 [Русский](Readme_ru.md) - Russian version  
- 🇨🇳 [中文](Readme_ch.md) - Chinese version

## License

MIT License
