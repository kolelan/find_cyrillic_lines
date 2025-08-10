import re
import os
import argparse
from typing import List, Tuple, Optional


def find_russian_content(text: str, all_line: bool = False) -> List[Tuple[int, str]]:
    """
    Находит русскоязычный контент в тексте.
    Если all_line=True, возвращает всю строку от первого до последнего кириллического символа.
    """
    if all_line:
        # Ищем всю строку между первым и последним кириллическим символом
        pattern = re.compile(r'^.*?([а-яА-ЯёЁ].*[а-яА-ЯёЁ]).*?$', re.MULTILINE)
        matches = pattern.finditer(text)
        return [(m.start(1), m.group(1)) for m in matches if m.group(1)]
    else:
        # Ищем отдельные русские слова и фразы (поведение по умолчанию)
        pattern = re.compile(r'[а-яА-ЯёЁ]+(?:\s+[а-яА-ЯёЁ]+)*')
        return [(m.start(), m.group()) for m in pattern.finditer(text)]


def generate_report(input_file: str, output_file: str, all_line: bool = False):
    """
    Генерирует отчёт о русскоязычном контенте в файле.
    """
    with open(input_file, 'r', encoding='utf-8') as f_in, \
            open(output_file, 'w', encoding='utf-8') as f_out:

        f_out.write(f"Отчёт о русскоязычном контенте в файле: {os.path.basename(input_file)}\n")
        f_out.write("Режим: " + ("ВСЯ СТРОКА между кириллическими символами" if all_line else "Отдельные фразы") + "\n")
        f_out.write("=" * 60 + "\n\n")

        for line_num, line in enumerate(f_in, start=1):
            phrases = find_russian_content(line, all_line)
            if phrases:
                for pos, phrase in phrases:
                    # Экранируем спецсимволы для лучшей читаемости
                    escaped_phrase = phrase.translate(str.maketrans({
                        "\n": "\\n",
                        "\t": "\\t",
                        "\r": "\\r"
                    }))
                    f_out.write(f"Строка {line_num}, позиция {pos}: '{escaped_phrase}'\n")


def main():
    parser = argparse.ArgumentParser(description='Поиск русскоязычного контента в файле')
    parser.add_argument('input_file', help='Путь к файлу для анализа')
    parser.add_argument('--output', '-o', help='Путь к файлу отчёта (по умолчанию: <input>_en.txt)')
    parser.add_argument('--all-line', '-a', action='store_true',
                        help='Включать всю строку между первым и последним кириллическим символом')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Ошибка: файл '{args.input_file}' не найден!")
        return

    output_file = args.output if args.output else \
        f"{os.path.splitext(args.input_file)[0]}_en.txt"

    try:
        generate_report(args.input_file, output_file, args.all_line)
        print(f"Отчёт успешно сохранён в: {output_file}")
        print(f"Режим: {'Вся строка между кириллическими символами' if args.all_line else 'Отдельные фразы'}")
    except Exception as e:
        print(f"Ошибка при обработке файла: {str(e)}")


if __name__ == "__main__":
    main()