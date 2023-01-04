from distutils.core import run_setup
import shutil
from pathlib import Path
import os
import sys

def main(containing_dir, library_name, version):
    old_dir = os.getcwd()
    os.chdir(containing_dir)
    sys.stdout = open(os.devnull, "w")
    run_setup("setup.py", script_args=["sdist"])
    sys.stdout = sys.__stdout__
    os.chdir(old_dir)
    shutil.copy(
        Path(containing_dir) / f"dist/{library_name}-{version}.tar.gz",
        Path(containing_dir) / f"dist/{library_name}-latest.tar.gz",
    )


if __name__ == "__main__":
    main()
