# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from os import path, walk
from re import search, MULTILINE

from setuptools import setup

this_dir = path.abspath(path.dirname(__file__))

with open(path.join(this_dir, "docs", "PYPI.md"), encoding='utf-8') as f:
    dyn_props = {
        "long_description": f.read(),
        "long_description_content_type": "text/markdown"
    }

with open(path.join(this_dir, "pincer", "__init__.py"), encoding='utf-8') as f:
    _re_match_str = r'.=*.\s*[\'"]([^\'"]*)[\'"]'
    content = f.read()


    def get_content(name: str):
        match = search(name + _re_match_str, content, MULTILINE)
        if not match:
            raise RuntimeError(f"{name} is not set!")
        return match.group(1)


    def get_packages():
        return [
            item[0].replace("./", "").replace("\\", ".").replace("/", ".")
            for item in list(walk('./pincer'))
            if "__pycache__" not in item[0]
        ]


    dyn_props = {
        **dyn_props,
        "name": get_content("__package__"),
        "version": get_content("__version__"),
        "packages": get_packages(),
        "license": get_content("__license__"),
        "description": get_content("__description__"),
        "author": get_content("__author__"),
    }

with open(path.join(this_dir, "requirements.txt"), encoding='utf-8') as f:
    dyn_props = {
        **dyn_props,
        "install_requires": [itm.strip() for itm in f.read().strip().split(" ")]
    }

setup(
    **dyn_props,
    project_urls={
        # "Documentation": "-- WIP --",
        "Github repository": "https://github.com/pincer-org/pincer",
        "ReadTheDocs": "https://pincer.readthedocs.org",
        "Discord": "https://discord.gg/8WkYz3fNFm"
    },
    url="https://pincer.dev",
    author_email="contact@pincer.dev",
    classifiers=[
        # Development statuses:
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    include_package_data=True,
    keywords=["discord", "api", "asynchronous"],
    extras_require={},
)
