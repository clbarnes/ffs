from pathlib import Path

import pytest
from click.testing import CliRunner

from ffs.cli import main

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


def normalise_whitespace(s: str):
    return " ".join(s.split())


@pytest.mark.parametrize(
    ["cmd"],
    [
        ("",),
        ("export",),
        ("book",),
        ("problems",),
    ],
)
def test_correct_help(cmd):
    readme_txt = normalise_whitespace((PROJECT_DIR / "README.md").read_text())
    args = ["--help"]
    if cmd:
        args.insert(0, cmd)
    runner = CliRunner()
    result = runner.invoke(main, args)
    assert result.exit_code == 0
    msg = normalise_whitespace(result.output)
    replaced = msg.replace("Usage: main ", "Usage: ffs ")
    assert replaced in readme_txt
