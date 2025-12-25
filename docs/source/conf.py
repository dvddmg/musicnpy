# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os, sys
sys.path.insert(0, os.path.abspath('../..'))

# import tibas.tt
# import alabaster
import sphinx_bootstrap_theme

project = 'musicnpy'
copyright = '2025, dvddmg'
author = 'dvddmg'
release = '0.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
extensions = [
    'sphinx.ext.autodoc',      # Estrae docstring dal codice
    'sphinx.ext.viewcode',     # Aggiunge link al codice sorgente
    'sphinx.ext.napoleon',     # Supporta formati Google/NumPy (opzionale ma consigliato)
]

# autodoc_default_options = {
#     'members': True,
#     'undoc-members': False,
#     'private-members': False,
#     'special-members': True,
#     'show-inheritance': True,
#     'imported-members': False,
# }

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'furo'
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_static_path = ['_static']
html_theme_options = {
    'bootswatch_theme': 'cerulean',  # Cambia tema colori
    'navbar_links': [],  # Svuota i link di default
    'navbar_sidebarrel': False,  # Rimuove prev/next
    'navbar_pagenav': False,  # Rimuove navigazione pagina
}
html_css_files = ['custom.css']
html_sidebars = {
    'index': [],  # Nessuna sidebar nella home
    '**': ['localtoc.html']  # Sidebar nelle altre pagine
}