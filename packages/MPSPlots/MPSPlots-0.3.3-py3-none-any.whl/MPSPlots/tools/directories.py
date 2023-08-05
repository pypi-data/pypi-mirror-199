#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import MPSPlots


root_path = Path(MPSPlots.__path__[0])

project_path = root_path.parents[0]

example_directory = root_path.joinpath('examples')

doc_path = root_path.parents[0].joinpath('docs')

doc_css_path = doc_path.joinpath('source/_static/default.css')

style_directory = root_path.joinpath('styles')

logo_path = doc_path.joinpath('images/logo.png')

version_path = root_path.joinpath('VERSION')

examples_path = root_path.joinpath('examples')

# -
