"""Build frozenlist"""
from __future__ import annotations

from typing import TYPE_CHECKING

# FIXME: Fix that old recipe..
from p4adev_recipes.recipe import BuildToolCompiledComponentsPythonRecipe as R

##from p4adev_recipes.recipe import AdvancedCompiledComponentsPythonRecipe
##from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe as R

if TYPE_CHECKING:
	from typing import List


class frozenlistRecipe(R):
	name: str = 'frozenlist'
	version: str = '1.4.1'
	url: str = 'https://pypi.python.org/packages/source/f/frozenlist/frozenlist-{version}.tar.gz'
	# url: str = 'https://files.pythonhosted.org/packages/83/10/466fe96dae1bff622021ee687f68e5524d6392b0a2f80d05001cd3a451ba/frozenlist-1.4.1-py3-none-any.whl'
	depends: List[str] = [
		'setuptools',
		'build',
		# 'git+https://github.com/BlackCatDevel0per/cython/archive/master.tar.gz',
		'cython',
	]

	# Install just for app (exclude native/host machine build)
	# to use setuptools from hostpython
	# install just inside bundle (app's target)
	install_in_hostpython: bool = False
	install_in_targetpython: bool = True


recipe = frozenlistRecipe()
