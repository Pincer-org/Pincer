# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath("../.."))
sys.path.append(os.path.abspath('extensions'))

from pincer import __version__

# -- Project information -----------------------------------------------------


project = "Pincer Library"
copyright = '2021, Pincer'
author = "Sigmanificient, Arthurdw"


# The full version, including alpha/beta/rc tags.
release = __version__

branch = 'main' if __version__.endswith('a') else 'v' + __version__

# -- General configuration ---------------------------------------------------


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_design',
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'exception_hierarchy',
    'attributetable',
    'silence',
    'sphinxcontrib_trio'
]

add_module_names = False

autodoc_typehints = 'none'

autodoc_member_order = 'alphabetical'

set_type_checking_flag = True

resource_links = {
    'discord': 'https://discord.gg/et54DgVjMX',
    'issues': 'https://github.com/Pincer-org/Pincer/issues',
    'discussions': 'https://github.com/Pincer-org/Pincer/discussions',
    'examples': f'https://github.com/Pincer-org/Pincer/tree/{branch}/examples',
}

intersphinx_mapping = {
    'py': ('https://docs.python.org/3', None),
    'ws': ('https://websockets.readthedocs.io/en/stable', None),
    'pil': ('https://pillow.readthedocs.io/en/stable', None)
}

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_default_options = {
    'members': True,
    'show-inheritance': True
}

with open('../requirements.txt') as f:
    autodoc_mock_imports = f.read().splitlines()

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_logo = '../assets/img/icon_small.png'
html_favicon = '../assets/img/icon.ico'
html_theme = 'furo'
# Material theme options (see theme.conf for more information)
html_theme_options = {
    'light_css_variables': {
        'color-brand-primary': '#4C8CBF',
        'color-brand-content': '#306998',
        'color-admonition-background': 'blue',
    },
    'dark_css_variables': {
        'color-brand-primary': '#306998',
        'color-brand-content': '#FFE871',
        'color-admonition-background': 'yellow',
    },
    "sidebar_hide_name": True,
}
pygments_style = 'monokai'
default_dark_mode = True
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named 'default.css' will overwrite the builtin 'default.css'.
html_static_path = ['_static']
html_css_files = ["custom.css"]

rst_prolog = '''
.. |coro| replace:: This function is a |coroutine_link|_.\n\n
.. |maybecoro| replace:: This function *could be a* |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: https://docs.python.org/3/library/asyncio-task.html#coroutine
.. |default| raw:: html

    <div class="default-value-section"> <span class="default-value-label">Default:</span>
'''

# The suffix of source filenames.
source_suffix = '.rst'
