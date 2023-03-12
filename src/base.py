from dataclasses import dataclass


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
