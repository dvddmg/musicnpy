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

extensions = [
    'nbsphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

nbsphinx_execute = 'auto'
nbsphinx_timeout = 60
nbsphinx_allow_errors = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
html_theme = 'shibuya'
html_theme_options = {
    "page_layout": "compact",
    "accent_color": "blue",
    "nav_links": [
        {
            "title": "info",
            "url": "./introduzione"
        }, {
            "title": "modules",
            # "url": "writing",
            "children": [
                {"title": "core", "url": "./core"},
                {"title": "pitch", "url": "./pitch"},
                {"title": "durs", "url": "./durs"},
                {"title": "velo", "url": "./velo"},
                {"title": "data", "url": "./data"},
                {"title": "topyly", "url": "./topyly"},
            ]
        }, {
            "title": "example",
            "url": "./example",
            "children": [
                {"title": "core example", "url": "./example/core_example"},
                {"title": "pitch example", "url": "./example/pitch_example"},
                {"title": "complete example", "url": "./example/complete_example"},
            ]
        }
    ]
}

# -- Options for LaTeX/PDF output --------------------------------------------

latex_engine = 'xelatex'

latex_documents = [
    ('index', 'musicnpy.tex', 'musicnpy',
     'dvddmg', 'manual'),
]

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '12pt',

    # Rimuove "Chapter N" e mostra solo il titolo (es. "Core", "Pitch")
    'preamble': r'''
\usepackage{titlesec}
\titleformat{\chapter}[display]
  {\normalfont\huge\bfseries}{}{0pt}{\Huge}
\titlespacing*{\chapter}{0pt}{-20pt}{40pt}
\setcounter{tocdepth}{3}
\setcounter{secnumdepth}{3}
''',

    # Margini
    'geometry': r'\usepackage[margin=2.5cm]{geometry}',

    # Per avere capitoli che iniziano su qualsiasi pagina (no pagine bianche)
    'extraclassoptions': 'openany,oneside',
}

# Escludi i notebook dal PDF se danno problemi
# latex_exclude_patterns = ['example/*']