"""Build yarl"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

# A little hack..
recipes_path = Path(__file__).parent.parent

if str(recipes_path) not in sys.path:
	sys.path.insert(0, str(recipes_path))

from utils.recipe import BuildToolCompiledComponentsPythonRecipe

if TYPE_CHECKING:
	from typing import List


class YarlRecipe(BuildToolCompiledComponentsPythonRecipe):
	name: str = 'yarl'
	version: str = '1.9.4'
	url: str = 'https://pypi.python.org/packages/source/y/yarl/yarl-{version}.tar.gz'
	depends: List[str] = ['setuptools']

	# Install just for build (exclude app)
	# (setuotools from hostpython)
	# install just inside bundle (app's target)
	install_in_hostpython: bool = False
	install_in_targetpython: bool = True


recipe = YarlRecipe()
