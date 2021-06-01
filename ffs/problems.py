import logging
from pathlib import Path
from typing import Iterator, Optional, Set, Tuple, List

from .classes import Entry
from .utils import get_child_names, get_list
from .exceptions import EmptyReadme, NoExplicitResponsible


logger = logging.getLogger(__name__)


def find_problems(
    root: Path,
    skip_problem_children=False,
    responsible: Optional[List[str]] = None,
    visited: Optional[Set[Path]] = None,
) -> Iterator[Tuple[List[str], Path, Exception]]:
    root = root.resolve()
    if visited is None:
        visited = set()

    if root in visited:
        return

    visited.add(root)
    skip = False

    try:
        metadata = Entry._read_metadata(root)
    except Exception as e:
        yield (responsible or [], root, e)
        ignore_list = []
        metadata = dict()
        skip = True

    ignore_list = get_list(metadata, "ignore")
    responsible = get_list(metadata, "responsible") or responsible
    if not responsible:
        logger.warning("Nobody responsible, falling back to directory owner")
        responsible = [root.owner()]

        yield (responsible, root, NoExplicitResponsible("No explicit responsibility for dataset"))

    try:
        readme = Entry._read_readme(root)
        if not readme.strip():
            yield (
                responsible, root, EmptyReadme("Readme is empty")
            )
    except Exception as e:
        yield (responsible or [], root, e)
        skip = True

    if skip and skip_problem_children:
        return

    child_names = get_child_names(root, ignore_list)
    for child in child_names:
        yield from find_problems(root / child, visited)
