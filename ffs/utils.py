from fnmatch import fnmatch, fnmatchcase
from pathlib import Path
from typing import List, Mapping


def ensure_list(obj) -> List:
    if isinstance(obj, str):
        return [obj]
    else:
        try:
            return list(obj)
        except TypeError:
            return [obj]


def get_list(d: Mapping, key) -> List:
    val = d.get(key, [])
    return ensure_list(val)


def fnmatch_any(name: str, patterns: List[str], case_sensitive=True):
    fn = fnmatchcase if case_sensitive else fnmatch
    for pattern in patterns:
        if fn(name, pattern):
            return True
    return False


def get_child_names(dpath: Path, ignore_globs: List[str]):
    if "*" in ignore_globs:
        return []

    return sorted(
        p.name
        for p in dpath.iterdir()
        if p.is_dir() and not fnmatch_any(p.name, ignore_globs)
    )
