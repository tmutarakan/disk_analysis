import os
import sys
from pathlib import Path
from typing import Tuple
import upload
from base import Directory, File


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

    @staticmethod
    def __print(subdirs: int, files: int, size: int):
        print(
            f'Subdirs: {subdirs}, Files: {files}, Size: {size}',
            end='\r',
            file=sys.stdout,
            flush=True
        )
        sys.stdout.flush()


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


def readable_bytes(size) -> str:
    suf = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB']
    i = 0
    while size >= 1024:
        size /= 1024
        i += 1
    return f'{round(size, 1)}{suf[i]}'


def main():
    if len(sys.argv) > 1:
        directory = os.path.abspath(sys.argv[1])
    else:
        directory = os.path.abspath('.')

    out = make_output(directory)
    upload.to_json(out)
    upload.to_csv(out)
    print()


if __name__ == '__main__':
    main()
