# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from setuptools import setup, find_packages
import re

with open("src/pincer/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

extra_requires = {
    "img": [
        "Pillow>=8.4.0",
    ],
    "speed": [
        "orjson>=3.5.4",
        "Brotli>=1.0.9",
        "aiodns>=1.1",
        "cchardet>=2.1.7",
    ],
}

setup(
    name="pincer",
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    project_urls={
        "Website": "https://pincer.dev",
        "Documentation": "https://docs.pincer.dev",
        "Discord": "https://discord.gg/8WkYz3fNFm",
        "Issue Tracker": "https://github.com/pincer-org/pincer/issues",
        "Pull Request Tracker": "https://github.com/pincer-org/piner/pulls",
    },
    url="https://github.com/pincer-org/pincer",
    license="MIT",
        author="Sigmanificient, Arthurdw",
    author_email="contact@pincer.dev",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extra_requires=extra_requires,
    description="Discord API wrapper rebuild from scratch.",
    python_requires=">=3.8",
    classifiers=[ # https://pypi.org/classifiers
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: AsyncIO",
        "Framework :: aiohttp",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)