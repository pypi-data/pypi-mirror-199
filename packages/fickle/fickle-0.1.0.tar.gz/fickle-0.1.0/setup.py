from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text("utf-8")

setup(
    name="fickle",
    description="load pickled data as safely as possible",
    version="0.1.0",
    author="Eduard Christian Dumitrescu",
    author_email="eduard.c.dumitrescu@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
