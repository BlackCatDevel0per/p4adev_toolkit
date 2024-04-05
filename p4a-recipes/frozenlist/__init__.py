"""Build frozenlist"""
from __future__ import annotations

from typing import TYPE_CHECKING

from p4adev_recipes.recipe import BuildToolCompiledComponentsPythonRecipe

if TYPE_CHECKING:
	from typing import List


class frozenlistRecipe(BuildToolCompiledComponentsPythonRecipe):
	name: str = 'frozenlist'
	version: str = '1.4.1'
	url: str = 'https://pypi.python.org/packages/source/f/frozenlist/frozenlist-{version}.tar.gz'
	depends: List[str] = ['setuptools']

	# Install just for build (exclude app)
	# (setuotools from hostpython)
	# install just inside bundle (app's target)
	install_in_hostpython: bool = False
	install_in_targetpython: bool = True


recipe = frozenlistRecipe()
