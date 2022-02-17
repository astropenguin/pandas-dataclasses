# Project information
author = "Akio Taniguchi"
copyright = "2021-2022 Akio Taniguchi"


# General configuration
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# Options for HTML output
html_static_path = ["_static"]
html_logo = "_static/logo.svg"
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/astropenguin/pandas-dataclasses/",
    "twitter_url": "https://twitter.com/astropengu_in/",
}
