"""Shared helpers for the Python sections.

Each section runs one kit tool as a reader would: as a script, from a folder,
on files the test writes. Set WSS_KIT to the kit's top folder if it is not
beside this repo (default ../world-saga-seed, then ../story-kit).
"""
import os, pathlib, subprocess, sys
import pytest

HERE = pathlib.Path(__file__).resolve().parent
BOOK = HERE.parent / 'book'


def kit_root():
    env = os.environ.get('WSS_KIT')
    for c in ([env] if env else []) + [HERE.parent.parent / 'world-saga-seed', HERE.parent.parent / 'story-kit']:
        if c and (pathlib.Path(c) / 'tools' / 'links.py').exists():
            return pathlib.Path(c).resolve()
    pytest.exit('kit not found: set WSS_KIT to the kit folder', returncode=2)


KIT = kit_root()


def run(tool, *args, cwd=None, stdin=None):
    """Run tools/<tool>.py with args in cwd; return (exit code, stdout + stderr)."""
    p = subprocess.run([sys.executable, str(KIT / 'tools' / f'{tool}.py'), *map(str, args)],
                       cwd=cwd, input=stdin, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def write(root, files):
    """Write {relative path: text} under root; return root."""
    root = pathlib.Path(root)
    for rel, text in files.items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding='utf-8')
    return root


@pytest.fixture
def book(tmp_path):
    """A fresh copy of the test book, to run a tool on or change a file in."""
    import shutil
    dest = tmp_path / 'book'
    shutil.copytree(BOOK, dest)
    return dest
