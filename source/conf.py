# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'The Text Processing Cookbook'
copyright = '2024, Jud Dagnall'
author = 'Jud Dagnall'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages'
]

templates_path = ['_templates']
exclude_patterns = []

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_theme_options = {
        'description': 'Tools and techniques for processing text and data on the command line',
        'show_relbars': True,
        'github_banner': True,
        'github_button': True,
        'github_user':  'thejud',
        'github_repo':  'the-text-processing-cookbook',
        'github_type': 'star',
        'github_count': True,
#        'logo': '../80s_keycaps.png',
        'canonical_url': 'https://thejud.github.io/text-processing-cookbook/'
}
html_logo = '80s_keycaps.png'
smart_quotes = False

myst_heading_anchors = 3
myst_enable_extensions = [
    'colon_fence',
    'attrs_block',
    'attrs_inline',
]


