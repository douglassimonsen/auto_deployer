import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).parent)
import git


def main(containing_dir, library_name, current_version):
    current_version_tag = f"{library_name}-v{current_version}"
    repo = git.Repo(containing_dir, search_parent_directories=True)
    if current_version_tag not in repo.tags:
        tag = repo.create_tag(
            current_version_tag,
            message=f"Automatic Tag for release: {current_version_tag}",
        )
        repo.remotes.origin.push(tag)
        return True
    return False
