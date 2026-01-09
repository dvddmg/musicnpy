# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os, sys
sys.path.insert(0, os.path.abspath('../..'))


project = 'musicnpy'
copyright = '2025, dvddmg'
author = 'dvddmg'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

# templates_path = ['_templates']
extensions = [
    'nbsphinx',
    'sphinx.ext.autodoc',      # Estrae docstring dal codice
    # 'sphinx.ext.viewcode',     # Aggiunge link al codice sorgente
    'sphinx.ext.napoleon',     # Supporta formati Google/NumPy (opzionale ma consigliato)
]

nbsphinx_execute = 'auto'
nbsphinx_timeout = 60
# nbsphinx_prompt_width = 0

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

html_static_path = ['_static']
# html_css_files = ['custom.css']
html_theme = 'shibuya'
html_theme_options = {
    "page_layout": "compact",
    "accent_color": "blue",
    "nav_links": [
        {
            "title": "info",
            "url": "./logbook"
        },{
            "title": "modules",
            "url": "writing",
            "children": [
                {
                    "title": "core",
                    "url": "./core"
                },{
                    "title": "pitch",
                    "url": "./pitch"
                },{
                    "title": "durs",
                    "url": "./durs"
                },{
                    "title": "velo",
                    "url": "./velo"
                },{
                    "title": "data",
                    "url": "./data"
                },{
                    "title": "topyly",
                    "url": "./topyly"
                }
            ]
        },{
            "title": "example",
            "url": "writing",
            "children": [
                {
                    "title": "core example",
                    "url": "./example/core_example"
                },
                {
                    "title": "pitch example",
                    "url": "./example/pitch_example"
                }
            ]
        }
    ]
}




# html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
# html_theme_options = {
#     # 'bootswatch_theme': 'cerulean',  # Cambia tema colori
#     'navbar_links': [],  # Svuota i link di default
#     'navbar_sidebarrel': False,  # Rimuove prev/next
#     'navbar_pagenav': False,  # Rimuove navigazione pagina
# }
# html_sidebars = {
#     'index': [],  # Nessuna sidebar nella home
#     '**': ['localtoc.html']  # Sidebar nelle altre pagine
# }