from distutils.core import setup
from os import path
from re import search, MULTILINE

this_dir = path.abspath(path.dirname(__file__))

with open(path.join(this_dir, "README.md"), encoding='utf-8') as f:
    dyn_props = {
        "long_description": f.read(),
        "long_description_content_type": "text/markdown"
    }

with open(path.join(this_dir, "pyscord", "__init__.py"), encoding='utf-8') as f:
    _re_match_str = r'\s*[\'"]([^\'"]*)[\'"]'
    content = f.read()


    def get_content(name: str):
        match = search(name + _re_match_str, content, MULTILINE).group(1)
        if not match:
            raise RuntimeError(f"{name} is not set!")
        return match


    dyn_props = {
        **dyn_props,
        "name": get_content("package"),
        "version": get_content("__version__"),
        "packages": ["pyscord", "pyscord.utils"],
        "license": get_content("__license__"),
        "description": get_content("__description__"),
        "author": get_content("__author__"),
        "copyright": get_content("__copyright__")
    }

with open(path.join(this_dir, "requirements.txt"), encoding='utf-8') as f:
    dyn_props = {
        **dyn_props,
        "install_requires": [itm.strip() for itm in f.read().strip().split(" ")]
    }

setup(
    **dyn_props,
    project_urls={
        "Documentation": "-- WIP --",
    },
    url="https://github.com/Pyscord/Pyscord",
    author_email="...",
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    include_package_data=True,
    keywords=["discord", "api", "asynchronous"],
    extras_require={},
)
