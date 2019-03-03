Prerequisites
=============

To "compile" documentation into html form you would need to install Sphinx documentation package, which should be relatively trivial.

If you're on macOS:

- Install from source: http://sphinx-doc.org/install.html

If you're on Ubuntu Linux 16.04:

    sudo apt install python3-pip
    sudo pip3 install -U pip setuptools
    sudo pip3 install -U sphinx sphinxcontrib-bibtex sphinxcontrib-fulltoc

Compilation
===========

Just type

    make html

And a set of HTML pages will be build under ``_build/html``


You can also type

    make latexpdf

This way Sphinx will prepare .tex file and will try to build .pdf document.

