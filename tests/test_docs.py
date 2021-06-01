from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).parent.parent
SRC_DIR: Path = PROJECT_DIR / "data-policy"
TGT_DIR: Path = PROJECT_DIR / "ffs"

has_submodule = SRC_DIR.exists() and any(SRC_DIR.iterdir())


requires_submodule = pytest.mark.skipif(
    not has_submodule,
    reason="data-policy submodule not available",
)


@requires_submodule
@pytest.mark.parametrize(["fname"], [("FILE_STRUCTURE.md",), ("GUIDELINES.md",)])
def test_correct_documents(fname: str):
    src = SRC_DIR / fname
    tgt = TGT_DIR / fname

    assert src.read_text() == tgt.read_text()
