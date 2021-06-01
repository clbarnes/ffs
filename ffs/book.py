import datetime as dt
import itertools
import logging
import os
import re
import shutil
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse

import pkg_resources
import toml

from . import __version__
from .classes import Entry

logger = logging.getLogger(__name__)


NOTES_TEXT = f"""
# Notes

This site was last updated at `{dt.datetime.now().isoformat()}` \
using `{__name__}` version `{__version__}`.
""".strip()

GITIGNORE = """
book/
""".strip()

DEFAULT_CONFIG = """
[book]
authors = []
language = "en"
title = "Standardised File Structure"
multilingual = false
src = "src"

[output.html]
no-section-label = true
fold = { enable = true, level = 1 }
""".strip()


def get_structure_text():
    return pkg_resources.resource_string(__name__, "FILE_STRUCTURE.md").decode("utf-8")


def get_guidelines_text():
    return pkg_resources.resource_string(__name__, "GUIDELINES.md").decode("utf-8")


def mdbook_init(target: Path, title=None):
    target.mkdir(parents=True)

    if title:
        d = toml.loads(DEFAULT_CONFIG)
        d["book"]["title"] = title
        config = toml.dumps(d)
    else:
        config = DEFAULT_CONFIG

    with open(target / "book.toml", "w") as f:
        f.write(config)

    with open(target / ".gitignore", "w") as f:
        f.write(GITIGNORE)

    book = target / "book"
    book.mkdir()

    src = target / "src"
    src.mkdir()


include_re = re.compile(r"\{\{\s*#include\s+(.+)\s*\}\}")
img_re = re.compile(r"\!\[\s*.*\s*\]\(\s*(.+)\s*\)")


def process_srcdir(dpath: Path) -> Tuple[str, List[Path]]:
    """
    Return README content with METADATA content inserted,
    and list of relative paths referenced by the README
    """
    md_txt = (dpath / Entry.readme_name).read_text()
    paths = []
    for match in itertools.chain(include_re.finditer(md_txt), img_re.finditer(md_txt)):
        path = match.group(1)
        if not path.startswith(os.path.sep) and not urlparse(path).scheme:
            paths.append(Path(path))

    meta_txt = (dpath / Entry.metadata_name).read_text().strip()
    outlines = []

    if not meta_txt:
        return md_txt, paths

    insert = f"\n```yaml\n{meta_txt}\n```\n"

    for line in md_txt.splitlines():
        if insert and line and not line.startswith("#"):
            outlines.append(insert)
            insert = ""
        outlines.append(line)

    if insert:
        outlines.append(insert)

    return "\n".join(outlines), paths


def copy_metadata(entry_root: Path, book_src_root: Path, rel_dir_path: Path) -> Path:
    """Return relative path of README"""
    index_txt, fpaths = process_srcdir(entry_root / rel_dir_path)
    rel_index_path = rel_dir_path / "index.md"
    book_index_path = book_src_root / rel_index_path
    book_index_path.parent.mkdir(parents=True, exist_ok=True)
    book_index_path.write_text(index_txt)

    for fpath in fpaths:
        rel_fpath = rel_dir_path / fpath
        book_fpath = book_src_root / rel_fpath
        book_fpath.parent.mkdir(exist_ok=True, parents=True)
        shutil.copyfile(entry_root / rel_fpath, book_fpath)

    return rel_index_path


def make_mdbook(entry: Entry, entry_path: Path, target: Path, title=None):
    if title is None:
        title = entry.name + "/"
    if not target.is_dir():
        logger.info("Target directory does not exist; creating default config")
        mdbook_init(target, title)

    abs_root = Path(entry_path).resolve()
    copied_root = (target / "src").resolve()
    copied_root.mkdir(exist_ok=True, parents=True)

    indent = " " * 2

    (target / "src" / "structure.md").write_text(get_structure_text())
    (target / "src" / "guidelines.md").write_text(get_guidelines_text())
    (target / "src" / "notes.md").write_text(NOTES_TEXT)

    lines = [
        "# Summary",
        "\n[Structure](structure.md)",
        "\n[Guidelines](guidelines.md)",
        "\n[Notes](notes.md)",
        "\n---\n",
    ]

    to_visit = [(0, Path("."), entry)]
    while to_visit:
        depth, rel_path, item = to_visit.pop()
        rel_index_path = copy_metadata(abs_root, copied_root, rel_path)
        lines.append(f"{indent * depth}- [{item.name}]({rel_index_path})")
        for child in reversed(item.children.values()):
            to_visit.append((depth + 1, rel_path / child.name, child))

    summary_path = target / "src" / "SUMMARY.md"
    if summary_path.is_file():
        logger.warning("Overwriting mdBook index at %s", summary_path)

    with open(summary_path, "w") as f:
        f.write("\n".join(lines))
