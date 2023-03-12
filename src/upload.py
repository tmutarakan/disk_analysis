import json
import csv
from dataclasses import is_dataclass, asdict
from base import Directory
import sqlite3


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        return super().default(obj)


def to_json(out: Directory):
    with open('out_iter.json', 'w') as f:
        json.dump(out, f, indent=4, cls=EnhancedJSONEncoder)


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
                'subdirs': None,
                'files': None,
                'modified': out.modified,
                'type': out.__class__.__name__,
                'parent_id': p_id
            }
        )


def to_csv(out: Directory):
    out_list = []
    parent_id = -1
    straighten_dict(out, out_list, parent_id)
    with open('out.csv', 'w') as csvfile:
        fieldnames = ["id", "name", "size", "subdirs", "files", "modified", "type", "parent_id"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_list)


def to_sqlite3(out: Directory):
    out_list = []
    parent_id = -1
    straighten_dict(out, out_list, parent_id)
    conn = sqlite3.connect('out.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS files(
            id INT PRIMARY KEY,
            myid INT,
            name TEXT,
            size INT,
            subdirs INT,
            files INT,
            modified FLOAT,
            type TEXT
            parent_id INT);
        """)
    conn.commit()
    for elem in out_list:
        cur.execute(
            "INSERT INTO files VALUES(?, ?, ?, ?, ?, ?, ?, ?);",
            [_ for _ in elem.values()])
    conn.commit()
