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


def straighten_dict(out: Directory, out_list: list, p_id: int):
    if hasattr(out, 'folder'):
        out_list.append(
            {
                'id': out.id,
                'name': out.name,
                'size': out.size,
                'subdirs': out.subdirs,
                'files': out.files,
                'modified': out.modified,
                'type': out.__class__.__name__,
                'parent_id': p_id
            }
        )
        for key in out.folder:
            straighten_dict(key, out_list, out.id)
    else:
        out_list.append(
            {
                'id': out.id,
                'name': out.name,
                'size': out.size,
                'modified': out.modified,
                'type': out.__class__.__name__,
                'parent_id': p_id
            }
        )
