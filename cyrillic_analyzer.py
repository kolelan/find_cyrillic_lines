import re
import os
import argparse
import json
from typing import List, Dict, Union, Optional


class CompactJSONEncoder(json.JSONEncoder):
    """Кастомный JSON-энкодер для компактного форматирования с однострочными объектами в массиве"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indent = None

    def encode(self, obj):
        if isinstance(obj, list):
            # Для массивов делаем каждый элемент на новой строке без дополнительных отступов
            return "[\n" + ",\n".join(
                json.dumps(item, ensure_ascii=False, separators=(',', ':')) for item in obj) + "\n]"
        return super().encode(obj)


def find_russian_content(text: str, all_line: bool = False) -> List[Dict[str, Union[int, str]]]:
    """Находит русскоязычный контент в тексте."""
    results = []
    pattern = re.compile(r'^.*?([а-яА-ЯёЁ].*[а-яА-ЯёЁ]).*?$' if all_line else r'[а-яА-ЯёЁ]+(?:\s+[а-яА-ЯёЁ]+)*')

    for match in pattern.finditer(text):
        group = match.group(1) if all_line else match.group()
        start_pos = match.start(1) if all_line else match.start()
        results.append({
            'line': 0,  # Будет заполнено позже
            'position': start_pos,
            'length': len(group),
            'include': group,
            'replace': ''
        })
    return results


def generate_report(input_file: str, output_file: str, all_line: bool = False, json_format: bool = False):
    """Генерирует отчёт о русскоязычном контенте в файле."""
    report = {
        'filename': os.path.basename(input_file),
        'mode': 'whole_line' if all_line else 'phrases',
        'entries': []
    }

    with open(input_file, 'r', encoding='utf-8') as f_in:
        for line_num, line in enumerate(f_in, start=1):
            for phrase in find_russian_content(line, all_line):
                phrase['line'] = line_num
                report['entries'].append(phrase)

    if json_format:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            # Записываем основную структуру
            f_out.write('{\n')
            f_out.write(f'"filename": {json.dumps(report["filename"], ensure_ascii=False)},\n')
            f_out.write(f'"mode": {json.dumps(report["mode"], ensure_ascii=False)},\n')
            f_out.write('"entries": [\n')

            # Записываем каждый entry в отдельной строке
            entries = report['entries']
            for i, entry in enumerate(entries):
                line = json.dumps(entry, ensure_ascii=False, separators=(',', ':'))
                f_out.write(line)
                if i < len(entries) - 1:
                    f_out.write(',')
                f_out.write('\n')

            f_out.write(']\n}\n')
    else:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(f"Отчёт о русскоязычном контенте в файле: {report['filename']}\n")
            f_out.write(f"Режим: {'ВСЯ СТРОКА между кириллическими символами' if all_line else 'Отдельные фразы'}\n")
            f_out.write("=" * 60 + "\n\n")
            for entry in report['entries']:
                escaped_phrase = entry['include'].translate(str.maketrans({
                    "\n": "\\n",
                    "\t": "\\t",
                    "\r": "\\r"
                }))
                f_out.write(f"Строка {entry['line']}, позиция {entry['position']}: '{escaped_phrase}'\n")


def apply_replacements(input_file: str, report_file: str):
    """Применяет замены из JSON-отчёта к исходному файлу."""
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            report = json.load(f)
    except Exception as e:
        print(f"Ошибка при чтении отчёта: {str(e)}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    replacements = 0
    for entry in report.get('entries', []):
        if entry.get('replace'):
            line_idx = entry['line'] - 1
            if line_idx < len(lines):
                line = lines[line_idx]
                start, end = entry['position'], entry['position'] + entry['length']
                lines[line_idx] = line[:start] + entry['replace'] + line[end:]
                replacements += 1

    if replacements:
        backup = input_file + '.bak'
        os.rename(input_file, backup)
        with open(input_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Выполнено {replacements} замен. Резервная копия: {backup}")
    else:
        print("Нет замен для применения.")


def main():
    parser = argparse.ArgumentParser(description='Поиск и замена русскоязычного контента')
    parser.add_argument('input_file', help='Входной файл для анализа')
    parser.add_argument('--output', '-o', help='Файл для отчёта')
    parser.add_argument('--all-line', '-a', action='store_true', help='Режим всей строки')
    parser.add_argument('--json', '-j', action='store_true', help='JSON формат отчёта')
    parser.add_argument('--replace', '-r', action='store_true', help='Применить замены')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Файл не найден: {args.input_file}")
        return

    if args.replace:
        report_file = args.output or f"{os.path.splitext(args.input_file)[0]}_en.json"
        apply_replacements(args.input_file, report_file)
        return

    output_file = args.output or f"{os.path.splitext(args.input_file)[0]}_en.{'json' if args.json else 'txt'}"

    try:
        generate_report(args.input_file, output_file, args.all_line, args.json)
        print(f"Отчёт сохранён: {output_file}")
    except Exception as e:
        print(f"Ошибка: {str(e)}")


if __name__ == "__main__":
    main()