from pathlib import Path
from typing import Iterator, Optional, Set, Tuple

from .classes import Entry
from .utils import get_child_names, get_list


def find_problems(
    root: Path,
    skip_problem_children=False,
    visited: Optional[Set[Path]] = None,
) -> Iterator[Tuple[str, Path, Exception]]:
    root = root.resolve()
    if visited is None:
        visited = set()

    if root in visited:
        return

    visited.add(root)

    owner = root.owner()
    skip = False

    try:
        Entry._read_readme(root)
    except Exception as e:
        skip = True
        yield (owner, root, e)

    try:
        metadata = Entry._read_metadata(root)
        ignore_list = get_list(metadata, "ignore")
    except Exception as e:
        skip = True
        yield (owner, root, e)
        ignore_list = []

    if skip and skip_problem_children:
        return

    child_names = get_child_names(root, ignore_list)
    for child in child_names:
        yield from find_problems(root / child, visited)
