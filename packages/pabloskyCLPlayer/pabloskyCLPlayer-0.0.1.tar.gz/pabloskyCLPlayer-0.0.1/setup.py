import setuptools
from pathlib import Path

longDesc = Path("README.md").read_text()

setuptools.setup(
    name="pabloskyCLPlayer",
    version="0.0.1",
    long_description=longDesc,
    packages=setuptools.find_packages(
        exclude=["mocks", "tests"]
    )
)
