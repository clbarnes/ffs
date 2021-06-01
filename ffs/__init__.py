from .version import version as __version__  # noqa: F401
from .version import version_tuple as __version_info__  # noqa: F401
from .spec_version import SPEC_VERSION

from .classes import Entry, EntryJso

__all__ = ["Entry", "EntryJso", "SPEC_VERSION"]
