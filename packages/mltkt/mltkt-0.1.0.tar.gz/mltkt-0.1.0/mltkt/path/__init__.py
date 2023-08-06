import sys
from pathlib import Path
from typing import Iterable, Optional
import os


def search_proj_root_marker(path: Path, proj_root_markers: Iterable[str]) -> Optional[Path]:
    for p in [path] + list(path.parents):
        if any((p / m).exists() for m in proj_root_markers):
            return p
    return None

def set_proj_root(
    cur_path: Path,
    set_sys: bool,
    set_cwd: bool,
    root_markers: Iterable[str] = ('.project-root-anchor',)
) -> None:
    root_path = search_proj_root_marker(cur_path, root_markers)
    assert root_path is not None, f"Cannot find project root with makers: {root_markers}"
    if set_sys:
        sys.path.insert(0, root_path.as_posix())
    if set_cwd:
        os.chdir(root_path)
