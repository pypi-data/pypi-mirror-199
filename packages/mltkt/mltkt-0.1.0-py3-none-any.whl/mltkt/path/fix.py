from . import set_proj_root
from pathlib import Path
import os


set_proj_root(
    Path(os.getcwd()),
    set_sys=True,
    set_cwd=True
)