"""Build yarl"""
from __future__ import annotations

from typing import TYPE_CHECKING

from p4adev_recipes.recipe import BuildToolCompiledComponentsPythonRecipe

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
