import json
import csv
import sqlite3
import pickle
from dataclasses import is_dataclass, asdict
from base import Directory, straighten_dict


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        return super().default(obj)


def to_json(out: Directory, filename: str):
    with open(filename, 'w') as f:
        json.dump(out, f, indent=4, cls=EnhancedJSONEncoder)


def to_csv(out: Directory, filename: str):
    out_list = []
    parent_id = -1
    straighten_dict(out, out_list, parent_id)
    with open(filename, 'w') as csvfile:
        fieldnames = [
            "id", "name", "size", "subdirs",
            "files", "modified", "type", "parent_id"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_list)


def to_sqlite3(out: Directory, filename: str):
    out_list = []
    parent_id = -1
    straighten_dict(out, out_list, parent_id)
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS files(
            id INT PRIMARY KEY,
            name TEXT,
            size INT,
            subdirs INT,
            files INT,
            modified FLOAT,
            type TEXT,
            parent_id INT);
        """)
    conn.commit()
    for elem in out_list:
        cur.execute(
            "INSERT INTO files VALUES(?, ?, ?, ?, ?, ?, ?, ?);",
            [_ for _ in elem.values()])
    conn.commit()
    conn.close()


def to_pickle(out: Directory, filename: str):
    out_list = []
    parent_id = -1
    straighten_dict(out, out_list, parent_id)
    with open(filename, 'wb') as f:
        pickle.dump(out_list, f)
