# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys


# -- Project information -----------------------------------------------------

project = "YANG++"
copyright = "2024, YumaWorks, Inc."
author = "Andy Bierman"

# The base version, including alpha/beta/rc tags
version = "alpha1"

# The full version, including alpha/beta/rc tags
# not going to mention release number in the title
# this is the 22.10 release train documentation
release = "alpha1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.autosectionlabel",
]

import os

if "READTHEDOCS" in os.environ:
    extensions.append("sphinx_search.extension")


## not installing this until ready to work on PDF output
#    'rst2pdf.pdfbuilder'


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------


# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_favicon = "_static/favicon.ico"
html_logo = "_static/YumaWorks_Logo_rect_150px.png"

# import sphinx_rtd_theme
html_theme = "sphinx_rtd_theme"
# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html
# need to add analytics_id

# sphinx-build says this is an unsupported option
# html_theme_options = {
#    'navagation_depth': -1
# }

html_theme_options = {"sticky_navigation": True, "navigation_depth": -1}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
# html_css_files = [
#     "css/custom.css",
# ]

html_show_sourcelink = False

html_copy_source = False

# This setting if True causes double quotes to be changed to emquote
smartquotes = False

# This will turn all the code-blocks a pale green.
# Seems to undo pygmentize; do not use for now
# pygments_style = 'sphinx'

# -- Extension configuration -------------------------------------------------
# pdf_documents = [('yumapro-netconfd-manual', u'netconfd', u'YumaPro netconfd-pro User Manual', u'YumaWorks, Inc.'),]
