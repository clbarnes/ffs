import subprocess as sp
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).parent.parent
SRC_DIR: Path = PROJECT_DIR / "data-policy"
TGT_DIR: Path = PROJECT_DIR / "ffs"


@pytest.mark.parametrize(["fname"], [("FILE_STRUCTURE.md",), ("GUIDELINES.md",)])
def test_correct_documents(fname: str):
    src = SRC_DIR / fname
    tgt = TGT_DIR / fname

    assert src.read_text() == tgt.read_text()


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
    readme_txt = (PROJECT_DIR / "README.md").read_text()
    args = ["ffs"]
    if cmd:
        args.append(cmd)
    args.append("--help")
    result = sp.run(args, capture_output=True, check=True, text=True)
    assert result.stdout in readme_txt
