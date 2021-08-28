import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding='utf8')

# This call to setup() does all the work
setup(
    name="pyscord",
    version="0.0.1",
    description="Discord API wrapper rebuild from scratch.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Pyscord/Pyscord",
    author="Pyscord",
    author_email="...",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=['pyscord'],
    include_package_data=True,
    install_requires=[]
)
