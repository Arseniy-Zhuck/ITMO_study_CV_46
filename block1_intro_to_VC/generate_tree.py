#!/usr/bin/env python3
"""
Скрипт для генерации Markdown-файла с деревом директории и ссылками на каждый элемент.

Пример запуска:
    python generate_tree.py --dir . --output tree.md
"""

import os
import argparse
from pathlib import Path


def get_relative_path(full_path, root_path):
    """Возвращает относительный путь с прямыми слешами для совместимости с GitHub."""
    rel = os.path.relpath(full_path, root_path)
    return rel.replace(os.sep, '/')


def generate_md_tree(startpath, output_file, ignored_dirs=None, ignored_exts=None):
    """
    Генерирует markdown-файл с деревом директории.

    startpath    - корневая директория для обхода
    output_file  - путь к выходному файлу (.md)
    ignored_dirs - множество имён папок для игнорирования
    ignored_exts - множество расширений файлов для игнорирования
    """
    if ignored_dirs is None:
        ignored_dirs = {'.git', '__pycache__', '.idea', '.vscode', 'node_modules', '.venv', 'env'}
    if ignored_exts is None:
        ignored_exts = {'.pyc', '.pyo', '.DS_Store'}

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('# Структура проекта\n\n')
        f.write(f'Корневая директория: `{os.path.abspath(startpath)}`\n\n')

        # Сортируем содержимое корня
        items = sorted(os.listdir(startpath))
        for item in items:
            full = os.path.join(startpath, item)
            # Пропускаем игнорируемые папки и файлы
            if os.path.isdir(full):
                if item in ignored_dirs:
                    continue
                _write_item(f, full, startpath, 0, ignored_dirs, ignored_exts)
            else:
                if any(full.endswith(ext) for ext in ignored_exts):
                    continue
                _write_item(f, full, startpath, 0, ignored_dirs, ignored_exts)


def _write_item(file_obj, path, rootpath, level, ignored_dirs, ignored_exts):
    """
    Рекурсивно записывает элемент (файл или папку) в markdown.
    """
    rel_path = get_relative_path(path, rootpath)
    indent = '  ' * level
    name = os.path.basename(path)

    if os.path.isdir(path):
        # Пишем папку со ссылкой (в GitHub ссылка на папку работает)
        file_obj.write(f'{indent}- [{name}/]({rel_path}/)\n')
        # Обходим содержимое папки, сначала сортируем
        subitems = sorted(os.listdir(path))
        for sub in subitems:
            sub_full = os.path.join(path, sub)
            if os.path.isdir(sub_full):
                if sub in ignored_dirs:
                    continue
                _write_item(file_obj, sub_full, rootpath, level + 1, ignored_dirs, ignored_exts)
            else:
                if any(sub_full.endswith(ext) for ext in ignored_exts):
                    continue
                _write_item(file_obj, sub_full, rootpath, level + 1, ignored_dirs, ignored_exts)
    else:
        # Файл: пишем ссылку
        file_obj.write(f'{indent}- [{name}]({rel_path})\n')


def main():
    parser = argparse.ArgumentParser(description='Генерация markdown-дерева директории')
    parser.add_argument('--dir', default='.', help='Корневая директория для обхода (по умолчанию: текущая)')
    parser.add_argument('--output', default='tree.md', help='Выходной файл (по умолчанию: tree.md)')
    parser.add_argument('--ignore-dirs', nargs='*', default=None,
                        help='Дополнительные папки для игнорирования (пробел разделитель)')
    parser.add_argument('--ignore-exts', nargs='*', default=None,
                        help='Дополнительные расширения файлов для игнорирования (пробел разделитель)')

    args = parser.parse_args()

    # Базовые игнорируемые папки и расширения
    ignored_dirs = {'.git', '__pycache__', '.idea', '.vscode', 'node_modules', '.venv', 'env'}
    ignored_exts = {'.pyc', '.pyo', '.DS_Store'}

    if args.ignore_dirs:
        ignored_dirs.update(args.ignore_dirs)
    if args.ignore_exts:
        ignored_exts.update(args.ignore_exts)

    startpath = os.path.abspath(args.dir)
    output_path = os.path.abspath(args.output)

    print(f'Генерация дерева для: {startpath}')
    print(f'Выходной файл: {output_path}')
    print(f'Игнорируемые папки: {sorted(ignored_dirs)}')
    print(f'Игнорируемые расширения: {sorted(ignored_exts)}')

    generate_md_tree(startpath, output_path, ignored_dirs, ignored_exts)
    print('Готово!')


if __name__ == '__main__':
    main()