# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sphinx

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'NDN Packet Format Specification'
copyright = '2013-2024, Named Data Networking Project'
author = 'Named Data Networking Project'

# The short X.Y version.
version = '0.3'
# The full version, including alpha/beta/rc tags.
release = version


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

needs_sphinx = '4.0'
extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# User-Agent header sent with linkcheck HTTP requests.
user_agent = f'Sphinx/{sphinx.__version__}'

# Use ABNF syntax highlighting by default for code blocks.
highlight_language = 'abnf'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_title = f'{project} v{version}'
html_logo = '_static/ndn-logo.svg'
html_last_updated_fmt = ''
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    'light_css_variables': {
        'color-brand-primary': '#d43b0b',
        'color-brand-content': '#c75300',
        'color-brand-visited': '#a55922',
    },
    'dark_css_variables': {
        'color-brand-primary': '#fd861a',
        'color-brand-content': '#f87e00',
        'color-brand-visited': '#dd8d48',
    },
    'source_repository': 'https://github.com/named-data/NDN-packet-spec',
    'source_branch': 'master',
}

pygments_style = 'tango'
pygments_dark_style = 'material'


# -- Options for LaTeX output ------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-latex-output

latex_documents = [
    ('index', 'ndn-packet-spec.tex', project, author, 'manual')
]
