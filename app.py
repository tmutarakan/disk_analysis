import os
import sys
import json
from pathlib import Path
from dataclasses import dataclass, is_dataclass, asdict
from typing import Tuple


class Counter:
    id: int = 0
    subdirs: int = 0
    files: int = 0
    size: int = 0

    @classmethod
    def add_data_directory(
        cls, dir_size: int, dir_files: int, dir_subdirs: int, total_size: int,
        count_files: int, subdirs: int
    ) -> Tuple[int, int, int]:
        total_size += dir_size
        count_files += dir_files
        subdirs += dir_subdirs + 1
        cls.subdirs += 1
        cls.id += 1
        cls.__print(cls.subdirs, cls.files, dir_size)
        return total_size, count_files, subdirs

    @classmethod
    def add_data_file(cls, size: int, total_size: int, count_files: int
                      ) -> Tuple[int, int]:
        cls.size += size
        total_size += size
        count_files += 1
        cls.files += 1
        cls.id += 1
        cls.__print(cls.subdirs, cls.files, size)
        return total_size, count_files

    def __print(subdirs: int, files: int, size: int):
        print(
            f'Subdirs: {subdirs}, Files: {files}, Size: {size}',
            end='\r',
            file=sys.stdout,
            flush=True
        )
        sys.stdout.flush()


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        return super().default(obj)


@dataclass
class Directory:
    id: int
    name: str
    readable_size: str
    size: int
    subdirs: int
    files: int
    modified: float
    folder: list


@dataclass
class File:
    id: int
    name: str
    readable_size: str
    size: int
    modified: float = 0


def getAllDirAndFile(path: str) -> Tuple[int, int, int, Counter]:
    itemList = Path(path).glob('*')     # Получить все файлы в текущем каталоге
    items = []      # Обработка каждого файла
    total_size = count_files = subdirs = d_size = 0
    for item in itemList:
        modified = os.path.getmtime(item)
        if os.path.islink(item):
            continue
        if os.path.isdir(item):
            for d_size, d_subdirs, d_files, d_out in getAllDirAndFile(item):
                items.append(
                    Directory(
                        id=Counter.id,
                        name=item.name,
                        readable_size=readable_bytes(d_size),
                        size=d_size,
                        subdirs=d_subdirs,
                        files=d_files,
                        modified=modified,
                        folder=d_out
                    )
                )
                total_size, count_files, subdirs = Counter.add_data_directory(
                    d_size, d_files, d_subdirs, total_size, count_files,
                    subdirs
                )
        else:
            size = os.path.getsize(item)
            items.append(
                File(
                    id=Counter.id,
                    name=item.name,
                    readable_size=readable_bytes(size),
                    size=size,
                    modified=modified
                )
            )
            total_size, count_files = Counter.add_data_file(
                size, total_size, count_files
            )
    yield total_size, subdirs, count_files, items


def make_output(directory: str) -> Directory:
    modified = os.path.getmtime(directory)
    for size, subdirs, files, folder in getAllDirAndFile(directory):
        out = Directory(
            id=Counter.id,
            name=directory,
            readable_size=readable_bytes(size),
            size=size,
            subdirs=subdirs,
            files=files,
            folder=folder,
            modified=modified
        )
    return out


def output_to_json(out: dict):
    with open('out_iter.json', 'w') as f:
        json.dump(out, f, indent=4, cls=EnhancedJSONEncoder)


def readable_bytes(size) -> str:
    suf = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB']
    i = 0
    while size >= 1024:
        size /= 1024
        i += 1
    return f'{round(size, 1)}{suf[i]}'


def go_tree(tree: dict, name: str):
    if tree[name]['isdir']:
        print(f"Direcory: {name} Size: {tree[name]['readable_size']} Subdirs: {tree[name]['subdirs']} Files: {tree[name]['files']}")
        for key in tree[name]['folder']:
            go_tree(tree[name]['folder'], key)
    else:
        print(f"File: {name} Size: {tree[name]['readable_size']}")


def main():
    if len(sys.argv) > 1:
        directory = os.path.abspath(sys.argv[1])
    else:
        directory = os.path.abspath('.')

    out = make_output(directory)
    output_to_json(out)
    # go_tree(out, directory)
    print()


if __name__ == '__main__':
    main()
