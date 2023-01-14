import requests
import json
from pathlib import Path
import git
from inspect import cleandoc
from urllib.parse import urlparse
import structlog
logger = structlog.get_logger()



def get_url(containing_dir):
    repo = git.Repo(containing_dir, search_parent_directories=True)
    remote_urls = [urlparse(x) for x in repo.remote().urls if urlparse(x).netloc == "github.com"]
    if len(remote_urls) == 0:
        logger.error("Missing Remote", remotes=list(repo.remote().urls), repo=str(Path(repo.git_dir).parent))
        raise ValueError("There are no remotes pointing to github.com for this repository")
    owner, remote_repo_name = remote_urls[0].path[1:-4].split('/')
    return f"https://api.github.com/repos/{owner}/{remote_repo_name}/releases"


def create_release(containing_dir, library_name, version, github_api_url, github_token):
    repo = git.Repo(containing_dir, search_parent_directories=True)
    release_notes = cleandoc(
        f"""
        Automatic generated release for version {version}.
        Some of the new updates:
    """
    )
    release_notes += "\n\n" + repo.head.commit.message
    resp = requests.post(
        github_api_url,
        json={
            "tag_name": f"{library_name}-v{version}",
            "target_commitish": "main",
            "name": f"{library_name}-v{version}",
            "body": release_notes,
            "draft": False,
            "prerelease": False,
            "generate_release_notes": True,
        },
        headers={
            "Authorization": f"Bearer {github_token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json",
        },
    )


def add_wheel(containing_dir, library_name, version, github_api_url, github_token):
    x = requests.get(github_api_url + "/latest", headers={
            "Authorization": f"Bearer {github_token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json",
        })
    data = json.loads(x.text)
    if data["tag_name"] != f"{library_name}-v{version}":
        raise ValueError("The tag/release failed to generate")
    upload_url = data["upload_url"].split("{")[0] + f"?name={library_name}.tar.gz"
    try:
        requests.post(
            upload_url,
            data=open(
                Path(containing_dir) / f"dist/{library_name}-latest.tar.gz", "rb"
            ).read(),
            headers={
                "Authorization": f"Bearer {github_token}",
                "Content-Type": "application/zip",
            },
        )
    except requests.exceptions.ConnectionError:
        pass


def main(containing_dir, library_name, version, github_token):
    github_api_url = get_url(containing_dir)
    create_release(containing_dir, library_name, version, github_api_url, github_token)
    add_wheel(containing_dir, library_name, version, github_api_url, github_token)


if __name__ == "__main__":
    main("C:/Users/mwham/Documents/repos/powerbi-decompressor/lib", 0, 0, 0)
