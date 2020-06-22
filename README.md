# NDN Packet Format Specification

## Prerequisites

To "compile" the specification in HTML format, you must first install the Sphinx documentation generator.

If you're running Ubuntu Linux:

    sudo apt install make python3-pip
    pip3 install -U pip setuptools
    pip3 install -U sphinx sphinxcontrib-bibtex sphinxcontrib-fulltoc

If you're running macOS or another operating system, see the instructions at https://www.sphinx-doc.org/en/master/usage/installation.html

## Compilation

Just type:

    make html

And a set of HTML pages will be generated under `_build/html`.

You can also type:

    make latexpdf

Sphinx will generate a `.tex` file and will try to create a `.pdf` document from it using `pdflatex` (which must be installed).

For further options, type `make help`.
