import setuptools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from auto_deployer import __version__


setuptools.setup(
    name="auto_deployer",
    packages=setuptools.find_packages(),
    version=__version__,
    description="A package that automatically tags and deploys ",
    url="https://github.com/douglassimonsen/auto_deployer",
    author="Matthew Hamilton",
    author_email="mwhamilton6@gmail.com",
    license="MIT",
    classifiers=[],
    include_package_data=True,
    install_requires=["GitPython", "requests"],
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
)
