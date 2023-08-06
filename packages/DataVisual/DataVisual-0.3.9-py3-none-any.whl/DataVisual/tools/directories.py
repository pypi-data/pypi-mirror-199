#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import DataVisual


root_path = Path(DataVisual.__path__[0])

project_path = root_path.parents[0]

static_doc_path = root_path.parents[0].joinpath('docs/images')

examples_path = root_path.joinpath('examples')

version_path = root_path.joinpath('VERSION')

doc_path = root_path.parents[0].joinpath('docs')

logo_path = doc_path.joinpath('images/logo.png')

doc_css_path = doc_path.joinpath('source/_static/default.css')

rtd_example = 'https://datavisual.readthedocs.io/en/latest/Examples.html'

# -
