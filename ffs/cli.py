import json
import logging
import os
import socket
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import click

from . import __version__
from .classes import Entry, EntryJso
from .problems import find_problems

logger = logging.getLogger(__name__)


def add_common_args(fn):
    return click.option(
        "--recursion",
        "-r",
        type=int,
        default=-1,
        help=(
            "Depth to recurse into entries; negative (default) for infinite. "
            "Directories which are not valid entries are not explored."
        ),
    )(fn)


@click.group()
@click.version_option(version=__version__)
@click.option("-v", "--verbose", count=True, help="Increase logging verbosity.")
def main(verbose):
    """Command line tool for working with a Flexible File Structure."""
    level = {
        None: logging.WARNING,
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
    }.get(verbose, logging.DEBUG)
    logging.basicConfig(level=level)


@main.command()
@click.argument("root", type=Path, default=Path.cwd())
@click.option("--sort", "-s", is_flag=True, help="Whether to sort keys in outupt.")
@click.option(
    "--indent",
    "-s",
    type=int,
    default=None,
    help=(
        "Indentation of output: none by default, 0 for newlines, "
        "a positive number N for N spaces, a negative number -N for N tabs."
    ),
)
@click.option(
    "--flatlines",
    "-l",
    is_flag=True,
    help=(
        "Un-nest the entries and print one object per line. "
        "The 'children' attribute is replaced by an array of string names, "
        "and the 'name' attribute now includes the entry's ancestors (/-separated). "
        "'--indent' option is ignored."
    ),
)
@add_common_args
def export(root, sort, indent, flatlines, recursion):
    """Read the FFS and its metadata into JSON."""
    entry = Entry.from_dir(root, recursion)
    jso = entry.to_jso()

    if not flatlines:
        if indent is not None and indent < 0:
            indent = "\t" * abs(indent)
        json.dump(
            jso, sys.stdout, sort_keys=bool(sort), indent=indent, ensure_ascii=False
        )
        print()
    else:
        for jsoline in flatten_jso(jso):
            json.dump(jsoline, sys.stdout, sort_keys=bool(sort), ensure_ascii=False)
            print()


def flatten_jso(jso: EntryJso):
    to_visit: List[Tuple[Optional[str], EntryJso]] = [(None, jso)]
    while to_visit:
        parent, entry = to_visit.pop()
        if parent is None:
            name = entry["name"]
        else:
            name = f'{parent}/{entry["name"]}'
        to_visit.extend((name, c) for c in reversed(entry["children"].values()))
        d = dict(entry)
        d["name"] = name
        d["children"] = list(d["children"])  # type:ignore
        yield d


@main.command()
@click.argument("root", type=Path, default=Path.cwd())
@click.argument("target", type=Path)
@click.option(
    "-t", "--title", help="Title for generated book, default '{FQDN}:{ROOT_REAL_PATH}'."
)
@add_common_args
def book(root, target, recursion, title=None):
    """Export the FFS metadata into files for mdbook."""
    name = f"{socket.getfqdn()}:{os.path.abspath(root)}"
    from .book import make_mdbook

    entry = Entry.from_dir(root, recursion, name)

    make_mdbook(entry, root, target, title)


@main.command()
@click.argument("root", type=Path, default=Path.cwd())
@click.option(
    "-c", "--check", is_flag=True, help="Exit with an error code at the first problem"
)
@click.option(
    "-s",
    "--skip-problems",
    is_flag=True,
    help="Do not attempt to traverse below problematic directories",
)
def problems(root, check, skip_problems):
    """List problems with the structure of the FFS."""
    for owner, path, err in find_problems(root, skip_problems):
        print(f"{owner}\t{path}\t{err}")
        if check:
            sys.exit(1)
