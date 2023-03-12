import json
import pandas as pd
from dataclasses import is_dataclass, asdict
from base import Directory, straighten_dict


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        return super().default(obj)
    

def to_json(out: Directory):
    with open('out_iter.json', 'w') as f:
        json.dump(out, f, indent=4, cls=EnhancedJSONEncoder)


def to_csv(out: Directory):
    out_list = []
    parent_id = -1
    straighten_dict(out, out_list, parent_id)
    pd.DataFrame(out_list).to_csv('out.csv', index=False)
