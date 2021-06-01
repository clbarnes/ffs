#!/usr/bin/env python3
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

import networkx as nx
import strictyaml as syml

from .utils import get_child_names, get_list

logger = logging.getLogger(__name__)

IntOrFloat = Union[int, float]
JsoValue = Union[str, IntOrFloat, bool, None]
Jso = Union[JsoValue, List["Jso"], Dict[str, "Jso"]]  # type: ignore[misc]


class EntryJso(TypedDict):
    name: str
    metadata: Dict[str, Jso]
    readme: str
    children: Dict[str, EntryJso]  # type: ignore[misc]


class Entry:
    """
    Class representing a directory containing the requisite metadata files to be
    treated as part of the structured file system.
    """

    readme_name = "README.md"
    metadata_name = "METADATA.yaml"

    def __init__(
        self,
        name: str,
        metadata: Dict[str, Any],
        readme: str,
        children: Iterable[Entry] = (),
    ) -> None:
        self.name = name
        self.metadata: Dict[str, Any] = metadata
        self.readme: str = readme
        self.children: Dict[str, Entry] = {c.name: c for c in children}

    @classmethod
    def from_dir(cls, path: Path, recursion=-1, name: Optional[str] = None) -> Entry:
        """
        Read an entry's name and metadata from a file path.

        `recursion` optionally describes how many levels of child entries
        the method is allowed to go into to find descendant entries;
        a negative value (default) is infinite.

        Children in the returned `Entry` instance are sorted by name.
        """
        path = Path(path)
        name = name or path.name
        logger.debug("Traversing in serial from %s", path)
        return cls._from_dir(path, recursion, name)

    def to_jso(self) -> EntryJso:
        """
        Serialise as a JSON-compatible `dict`.
        """
        return {
            "name": self.name,
            "metadata": self.metadata,
            "readme": self.readme,
            "children": {name: c.to_jso() for name, c in self.children.items()},
        }

    @classmethod
    def from_jso(cls, jso: EntryJso) -> Entry:
        """
        Deserialise from a JSON-like `dict`.
        """
        return cls(
            jso["name"],
            jso["metadata"],
            jso["readme"],
            (cls.from_jso(val) for val in jso["children"].values()),
        )

    def to_digraph(self) -> nx.DiGraph:
        """Represent the entry as a directed tree.

        The edges point from parent to child.
        A reference to the original objects are stored on each node
        as an attribute called `"entry"`.

        Note that changing this object's structure will not update
        the children of the entry objects, and vice versa:
        they could get out of sync.
        """
        return self._to_digraph(None)

    @classmethod
    def _read_metadata(cls, dir_path: Path):
        fpath = dir_path / cls.metadata_name
        with open(fpath) as f:
            logger.debug("Reading metadata from %s", fpath)
            contents = f.read()
            yaml = syml.load(contents)
            metadata: Dict[str, Any] = yaml.data or dict()
        return metadata

    @classmethod
    def _read_readme(cls, dir_path: Path):
        fpath = dir_path / cls.readme_name
        with open(fpath) as f:
            logger.debug("Reading readme from %s", fpath)
            readme = f.read()
        return readme

    @classmethod
    def _from_dir(cls, path: Path, recursion: int, name: str):
        metadata = cls._read_metadata(path)
        readme = cls._read_readme(path)

        ignore_globs = get_list(metadata, "ignore")
        child_names = get_child_names(path, ignore_globs) if recursion else []

        new_rec = recursion - 1
        children = [cls._from_dir(path / c, new_rec, c) for c in child_names]

        obj = cls(name, metadata, readme, children)
        logger.debug(
            "Got entry with name '%s' and %s children from '%s'",
            name,
            len(children),
            path,
        )
        return obj

    def _to_digraph(self, existing: Optional[Tuple[nx.DiGraph, str]]):
        if existing is None:
            g = nx.OrderedDiGraph()
            name = self.name or "/"
            g.add_node(name, entry=self)
            root = name
        else:
            g, root = existing

        for child in self.children.values():
            name = "/".join([root.rstrip("/"), child.name])
            g.add_node(name, entry=child)
            g.add_edge(root, name)
            child._to_digraph((g, name))

        return g
