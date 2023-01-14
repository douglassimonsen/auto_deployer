try:
    from .deployment import export, release, tagger
except ImportError:
    from deployment import export, release, tagger
import git
import sys
from distutils.core import run_setup
from pathlib import Path
import os
import structlog
logger = structlog.get_logger()


def main(containing_dir: str, force=False):
    force |= "--force" in sys.argv
    containing_dir = str(containing_dir)
    if 'github_token' not in os.environ:
        raise KeyError("You need to set the environment variable 'github_token' to use this utility")
    github_token = os.environ["github_token"]
    setup_path = Path(containing_dir) / "setup.py"

    logger.info("begin running setup.py", stop_after="config")
    package_info = run_setup(
        setup_path, stop_after="config"
    )  # stop_after keeps it from actually

    library_name = package_info.get_name()
    version = package_info.get_version()
    logger.info("finished running setup.py", stop_after="config")
    repo = git.Repo(containing_dir, search_parent_directories=True)
    logger.info("pushing commits to remote", remote=next(repo.remote().urls))
    repo.remote().push()[0]
    if (
        force or tagger.main(containing_dir, library_name, version)
    ):  # we really only need to do the work if a new tag has been added
        logger.info("exporting repo to whl file")
        export.main(containing_dir, library_name, version)
        logger.info("add whl file to release")
        release.main(containing_dir, library_name, version, github_token)


if __name__ == "__main__":
    os.environ["github_token"] = open(Path(__file__).parent / 'token.txt').read()
    main("C:/Users/mwham/Documents/repos/powerbi-decompressor/lib")
