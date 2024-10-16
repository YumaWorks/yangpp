# YANG++

YANG++ is a data modeling language under development.

This is an open-source project.

## Project Goals

-  Complete the design and specification of the YANG++ language
-  Design and implement open-source plugins

   -  Native compiler support for YANG++
   -  YANG 1.1 Translation Tool

## modules

YANG Modules for YANG++

- yangpp-classmap.yang: YANG library additions for class mappings

## docs

Sphinx documentation is used.

-  [Install sphinx](https://www.sphinx-doc.org/en/master/usage/installation.html)
-  Make the HTML documentation

```
cd docs
make clean
make html
```

-  The generated HTML files are in the 'docs/build/html' directory.

-  The file 'docs/build/html/index.html' is the entry point for the documentation.

-  The RST source files are in the 'docs/source/yangpp' directory.

-  The output is hosted on [readthedocs.com](https://yangpp.yumaworks.com/en/latest/)
