# 西里尔字母分析替换工具

用于检测和替换文本文件中俄语内容的实用工具，具有灵活的报表功能。

## 功能特点

- 检测文本文件中的俄语短语
- 两种搜索模式：
  - 单独词语/短语（默认）
  - 首尾西里尔字符之间的整行内容（`-a`参数）
- 报表格式：
  - 文本格式（默认）
  - JSON格式（`-j`参数）紧凑排版
- 带备份的替换功能（`-r`参数）

## 安装要求

需要Python 3.6+环境：

```bash
git clone https://github.com/your-repo/cyrillic-analyzer.git
cd cyrillic-analyzer
```

## 使用说明

### 基础命令

```bash
# 分析文件（文本报表）
python cyrillic_analyzer.py input.txt

# 生成JSON格式报表
python cyrillic_analyzer.py input.txt -j

# 整行分析模式
python cyrillic_analyzer.py input.txt -a
```

### 高级选项

```bash
# 创建指定名称的报表
python cyrillic_analyzer.py input.txt -o custom_report.json -j

# 根据报表执行替换
python cyrillic_analyzer.py input.txt -r -o report.json

# 组合分析模式（整行+JSON）
python cyrillic_analyzer.py input.txt -a -j
```

## JSON报表格式

示例结构：

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

字段说明：
- `line`: 行号（从1开始）
- `position`: 字符位置（从0开始）
- `length`: 短语长度
- `include`: 发现的文本
- `replace`: 替换内容（默认为空）

## 最佳实践

1. 首先生成报表：
```bash
python cyrillic_analyzer.py document.txt -j -o analysis.json
```

2. 编辑JSON文件，填写需要替换的内容

3. 执行替换：
```bash
python cyrillic_analyzer.py document.txt -r -o analysis.json
```

## 问题反馈

发现错误或有改进建议？请在项目仓库提交issue。

## 🌍 Available Translations | Доступные переводы | 可用翻译
- 🇬🇧 [English](Readme.md) - English version  
- 🇷🇺 [Русский](Readme_ru.md) - Russian version  
- 🇨🇳 [中文](Readme_ch.md) - Chinese version

## 开源协议

MIT License
