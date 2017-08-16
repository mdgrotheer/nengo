# -*- coding: utf-8 -*-
#
# This file is execfile()d with the current directory set
# to its containing dir.

import os
import os.path
import shutil
import sys

try:
    import nbsphinx
    import nengo
    import guzzle_sphinx_theme
except ImportError:
    print("To build the documentation, nengo and guzzle_sphinx_theme must be "
          "installed in the current environment. Please install these and "
          "their requirements first. A virtualenv is recommended!")
    sys.exit(1)


if 'NENGO_NBSPHINX_KERNEL' in os.environ:
    nbsphinx_kernel_name = os.environ['NENGO_NBSPHINX_KERNEL']
else:
    from jupyter_client.kernelspecapp import KernelSpecManager
    kernels = sorted(KernelSpecManager().find_kernel_specs())
    print("Available Jupyter kernels:")
    for i, kernel in enumerate(kernels):
        print(" {}. {}".format(i + 1, kernel))
    nbsphinx_kernel_name = None
    while nbsphinx_kernel_name not in kernels:
        nbsphinx_kernel_name = input(
            "Select kernel for executing Jupyter notebooks: ")
        try:
            nbsphinx_kernel_name = kernels[int(nbsphinx_kernel_name) - 1]
        except (IndexError, ValueError):
            pass
    print("To make this choice permanent add the following to your shell "
          "startup file (e.g., .bashrc):")
    print("export NENGO_NBSPHINX_KERNEL={!r}".format(nbsphinx_kernel_name))


if os.path.exists('examples'):
    shutil.rmtree('examples')
shutil.copytree('../examples', 'examples')
for dirpath, dirnames, _ in os.walk('examples'):
    for d in dirnames:
        with open(os.path.join(dirpath, d, 'nengorc'), 'w') as f:
            f.write('[progress]\nprogress_bar = False\n')


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'guzzle_sphinx_theme',
    'nbsphinx',
    'numpydoc',
    'nengo.utils.docutils',
]

# -- sphinx.ext.autodoc
autoclass_content = 'both'  # class and __init__ docstrings are concatenated
autodoc_default_flags = ['members']
autodoc_member_order = 'bysource'  # default is alphabetical

# -- sphinx.ext.intersphinx
intersphinx_mapping = {
    'numpy': ('https://docs.scipy.org/doc/numpy', None),
    'python': ('https://docs.python.org/3/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
}

# -- sphinx.ext.todo
todo_include_todos = True
# -- numpydoc config
numpydoc_show_class_members = False

# -- sphinx
exclude_patterns = ['_build', '**/.ipynb_checkpoints']
source_suffix = ['.rst', '.ipynb']
source_parsers = {'.ipynb': nbsphinx.NotebookParser}
source_encoding = 'utf-8'
master_doc = 'index'

# -- nbsphinx
nbsphinx_timeout = 600

# Need to include https Mathjax path for sphinx < v1.3
mathjax_path = ("https://cdn.mathjax.org/mathjax/latest/MathJax.js"
                "?config=TeX-AMS-MML_HTMLorMML")

project = u'Nengo'
authors = u'Applied Brain Research'
copyright = nengo.__copyright__
version = '.'.join(nengo.__version__.split('.')[:2])  # Short X.Y version
release = nengo.__version__  # Full version, with tags
pygments_style = 'default'

# -- Options for HTML output --------------------------------------------------

pygments_style = "sphinx"
templates_path = ["_templates"]
html_static_path = ["_static"]

html_theme_path = guzzle_sphinx_theme.html_theme_path()
html_theme = "guzzle_sphinx_theme"

html_theme_options = {
    "project_nav_name": "Nengo core %s" % (version,),
    "base_url": "https://www.nengo.ai/nengo",
}

html_title = "Nengo core {0} docs".format(release)
htmlhelp_basename = 'Nengo core'
html_last_updated_fmt = ''  # Suppress 'Last updated on:' timestamp
html_show_sphinx = False

# -- Options for LaTeX output -------------------------------------------------

latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '11pt',
    # 'preamble': '',
}

latex_documents = [
    # (source start file, target, title, author, documentclass [howto/manual])
    ('index', 'nengo.tex', html_title, authors, 'manual'),
]

# -- Options for manual page output -------------------------------------------

man_pages = [
    # (source start file, name, description, authors, manual section).
    ('index', 'nengo', html_title, [authors], 1)
]

# -- Options for Texinfo output -----------------------------------------------

texinfo_documents = [
    # (source start file, target, title, author, dir menu entry,
    #  description, category)
    ('index', 'nengo', html_title, authors, 'Nengo',
     'Large-scale neural simulation in Python', 'Miscellaneous'),
]
