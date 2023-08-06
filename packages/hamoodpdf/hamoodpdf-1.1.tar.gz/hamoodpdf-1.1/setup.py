import setuptools
from pathlib import Path

setuptools.setup(
    name="hamoodpdf",
    version=1.1,
    long_description=Path(r"C:\Users\super\hamoodpdf\README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
