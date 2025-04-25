# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sphinx

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'NDN Packet Format Specification'
copyright = '2013-2025, Named Data Networking Project'
author = 'Named Data Networking Project'

# The short X.Y version.
version = '0.3'
# The full version, including alpha/beta/rc tags.
release = version


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

needs_sphinx = '4.0'
extensions = []

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Use ABNF syntax highlighting as the default for code blocks.
highlight_language = 'abnf'

# User-Agent header sent with linkcheck HTTP requests.
user_agent = f'Sphinx/{sphinx.__version__}'

# Generate warnings for all missing references.
nitpicky = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_title = f'{project} v{version}'
html_logo = 'ndn-logo.svg'
html_last_updated_fmt = ''
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    'light_css_variables': {
        'color-brand-primary': '#bc4010',
        'color-brand-content': '#c85000',
        'color-brand-visited': '#c85000',
    },
    'dark_css_variables': {
        'color-brand-primary': '#fd861a',
        'color-brand-content': '#f87e00',
        'color-brand-visited': '#f87e00',
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

latex_logo = 'ndn-logo.pdf'
latex_show_pagerefs = True
# latex_show_urls = 'footnote'
