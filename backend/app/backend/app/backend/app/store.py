import json
import os
from threading import Lock

DATA_DIR = "/data/projects"
STATUS_FILE = "/data/projects/statuses.json"
_lock = Lock()

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(STATUS_FILE):
    with open(STATUS_FILE,"w",encoding="utf-8") as f:
        json.dump({}, f)

def _read_all():
    with _lock:
        with open(STATUS_FILE,"r",encoding="utf-8") as f:
            return json.load(f)

def _write_all(d):
    with _lock:
        with open(STATUS_FILE,"w",encoding="utf-8") as f:
            json.dump(d, f, indent=2)

def project_status_set(project_id, data):
    d = _read_all()
    d[project_id] = data
    _write_all(d)

def project_status_get(project_id):
    d = _read_all()
    return d.get(project_id, {"phase":"unknown"})
