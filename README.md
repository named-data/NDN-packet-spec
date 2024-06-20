<div align="center">

[<img alt height="65" src="ndn-logo.svg"/>](https://named-data.net/)

# NDN Packet Format Specification

</div>

This repository contains the base packet format specification of the Named Data
Networking (NDN) protocol.

An HTML version of the specification can be viewed online at
<https://docs.named-data.net/NDN-packet-spec/>.

## Compiling from source

### Prerequisites

To "compile" the specification in HTML format, you must first install the
[Sphinx](https://www.sphinx-doc.org/en/master/) documentation generator and a
few other dependencies. To do so, first make sure that the following packages
are installed and up to date:

* make
* python 3.9 or later
* pip

For instance, on Ubuntu Linux you can use the following commands:

    sudo apt install make python3-pip
    python3 -m pip install -U pip

On other operating systems, you can either use your preferred package manager or
follow [pip's installation instructions](https://pip.pypa.io/en/stable/installation/).

Finally, run:

    python3 -m pip install -r requirements.txt

to install the recommended version of Sphinx and its dependencies.

### Compilation

Just type:

    make html

And a set of HTML pages will be generated inside `_build/html`.

You can also type:

    make latexpdf

Sphinx will generate a `.tex` file and will try to compile it into a PDF document
using `latexmk` and `pdflatex` (which must be installed). If successful, the final
`.pdf` file can be found in `_build/latex`.

For further options, type `make help`.
