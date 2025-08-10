# Кириллический Анализатор и Заменитель

Утилита для поиска и замены русскоязычного контента в текстовых файлах с гибкими настройками отчётов.

## Возможности

- Поиск русскоязычных фраз в текстовых файлах
- Два режима поиска:
  - Отдельные слова/фразы (по умолчанию)
  - Целые строки между первыми и последними кириллическими символами (`-a`)
- Генерация отчётов в форматах:
  - Текстовый (по умолчанию)
  - JSON (`-j`) с компактным форматированием
- Функция замены с резервным копированием (`-r`)

## Установка

Требуется Python 3.6+:

```bash
git clone https://github.com/ваш-репозиторий/кириллический-анализатор.git
cd кириллический-анализатор
```

## Использование

### Базовые команды

```bash
# Анализ файла (текстовый отчёт)
python kirillic_analyzer.py input.txt

# Анализ с JSON-отчётом
python kirillic_analyzer.py input.txt -j

# Анализ в режиме всей строки
python kirillic_analyzer.py input.txt -a
```

### Расширенные возможности

```bash
# Создание именованного отчёта
python kirillic_analyzer.py input.txt -o custom_report.json -j

# Применение замен из отчёта
python kirillic_analyzer.py input.txt -r -o report.json

# Комбинированный анализ (вся строка + JSON)
python kirillic_analyzer.py input.txt -a -j
```

## Формат JSON-отчёта

Пример структуры отчёта:

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

Поля:
- `line`: Номер строки (1-based)
- `position`: Позиция в строке (0-based)
- `length`: Длина фразы
- `include`: Найденный текст
- `replace`: Поле для замены (изначально пустое)

## Лучшие практики

1. Сначала создайте отчёт:
```bash
python kirillic_analyzer.py document.txt -j -o analysis.json
```

2. Отредактируйте JSON-файл, заполнив поле `replace` для нужных фраз

3. Примените изменения:
```bash
python kirillic_analyzer.py document.txt -r -o analysis.json
```

## Обратная связь

Нашли ошибку или есть предложения? Создайте issue в репозитории проекта.

## Лицензия

MIT License
