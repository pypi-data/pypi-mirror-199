import subprocess
from pathlib import Path
from typing import Optional
from zipfile import ZipFile


def zip_code(code_dir: Path, zip_path: Path, use_git: bool, code_glob: Optional[str]='*.py') -> None:
    with ZipFile(zip_path, "w") as zip_file:
        if use_git:
            # get .git folder
            # https://alexwlchan.net/2020/11/a-python-function-to-ignore-a-path-with-git-info-exclude/
            git_dir_path = Path(subprocess.check_output(["git", "rev-parse", "--git-dir"]).strip().decode("utf8")).resolve()

            for path in code_dir.rglob('*'):
                if (
                    path.is_file()
                    and (not path.is_relative_to(git_dir_path))  # ignore files in .git
                    and (subprocess.run(['git', 'check-ignore', '-q', str(path)]).returncode == 1)  # ignore files ignored by git
                ):
                    zip_file.write(str(path), arcname=str(path.relative_to(code_dir)))

        else:
            for path in code_dir.rglob(code_glob):
                zip_file.write(str(path), arcname=str(path.relative_to(code_dir)))
