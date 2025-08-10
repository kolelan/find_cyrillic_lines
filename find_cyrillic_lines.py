import re
import os
import argparse
import json
from typing import List, Dict, Union, Optional

def find_russian_content(text: str, all_line: bool = False) -> List[Dict[str, Union[int, str]]]:
    """
    Находит русскоязычный контент в тексте.
    Возвращает список словарей с информацией о найденных фразах.
    """
    results = []
    if all_line:
        # Режим всей строки между первым и последним кириллическим символом
        pattern = re.compile(r'^.*?([а-яА-ЯёЁ].*[а-яА-ЯёЁ]).*?$', re.MULTILINE)
        for match in pattern.finditer(text):
            start_pos = match.start(1)
            phrase = match.group(1)
            results.append({
                'position': start_pos,
                'length': len(phrase),
                'include': phrase,
                'replace': ''
            })
    else:
        # Режим отдельных слов и фраз
        pattern = re.compile(r'[а-яА-ЯёЁ]+(?:\s+[а-яА-ЯёЁ]+)*')
        for match in pattern.finditer(text):
            results.append({
                'position': match.start(),
                'length': len(match.group()),
                'include': match.group(),
                'replace': ''
            })
    return results

def generate_report(input_file: str, output_file: str, all_line: bool = False, json_format: bool = False):
    """
    Генерирует отчёт о русскоязычном контенте в файле.
    """
    report = {
        'filename': os.path.basename(input_file),
        'mode': 'whole_line' if all_line else 'phrases',
        'entries': []
    }

    with open(input_file, 'r', encoding='utf-8') as f_in:
        for line_num, line in enumerate(f_in, start=1):
            phrases = find_russian_content(line, all_line)
            for phrase in phrases:
                phrase['line'] = line_num
                report['entries'].append(phrase)

    if json_format:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            json.dump(report, f_out, ensure_ascii=False, indent=2)
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
    """
    Применяет замены из JSON-отчёта к исходному файлу.
    """
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            report = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: файл отчёта '{report_file}' не найден!")
        return
    except json.JSONDecodeError:
        print(f"Ошибка: файл '{report_file}' не является валидным JSON!")
        return

    # Читаем исходный файл
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Применяем замены
    replacements_count = 0
    for entry in report['entries']:
        if entry.get('replace', ''):
            line_idx = entry['line'] - 1
            if line_idx < len(lines):
                original_line = lines[line_idx]
                start = entry['position']
                end = start + entry['length']
                new_line = original_line[:start] + entry['replace'] + original_line[end:]
                lines[line_idx] = new_line
                replacements_count += 1

    # Записываем изменённый файл
    if replacements_count > 0:
        backup_file = input_file + '.bak'
        os.rename(input_file, backup_file)
        with open(input_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Выполнено {replacements_count} замен. Исходный файл сохранён как '{backup_file}'")
    else:
        print("Не найдено замен для применения.")

def main():
    parser = argparse.ArgumentParser(description='Поиск и замена русскоязычного контента в файле')
    parser.add_argument('input_file', help='Путь к файлу для анализа')
    parser.add_argument('--output', '-o', help='Путь к файлу отчёта')
    parser.add_argument('--all-line', '-a', action='store_true',
                       help='Включать всю строку между первым и последним кириллическим символом')
    parser.add_argument('--json', '-j', action='store_true',
                       help='Генерировать отчёт в формате JSON')
    parser.add_argument('--replace', '-r', action='store_true',
                       help='Применить замены из JSON-отчёта')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Ошибка: файл '{args.input_file}' не найден!")
        return

    if args.replace:
        if not args.json:
            print("Для замены необходимо указать JSON-отчёт (используйте флаг --json)")
            return
        if not args.output:
            args.output = f"{os.path.splitext(args.input_file)[0]}_en.json"
        apply_replacements(args.input_file, args.output)
        return

    # Определяем имя выходного файла
    if not args.output:
        base_name = os.path.splitext(args.input_file)[0]
        args.output = f"{base_name}_en.json" if args.json else f"{base_name}_en.txt"

    try:
        generate_report(args.input_file, args.output, args.all_line, args.json)
        print(f"Отчёт успешно сохранён в: {args.output}")
        print(f"Формат: {'JSON' if args.json else 'TXT'}")
        print(f"Режим: {'Вся строка между кириллическими символами' if args.all_line else 'Отдельные фразы'}")
    except Exception as e:
        print(f"Ошибка при обработке файла: {str(e)}")

if __name__ == "__main__":
    main()