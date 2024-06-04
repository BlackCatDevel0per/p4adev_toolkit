"""Build cython"""
from __future__ import annotations

from p4adev_recipes.recipe import AdvancedCompiledComponentsPythonRecipe


class CythonRecipe(AdvancedCompiledComponentsPythonRecipe):
	name = 'cython'
	version = '0.29.28'  # real ~0.29.37
	url = 'https://github.com/BlackCatDevel0per/cython/archive/master.tar.gz'  # my fork with crutchy~ turned on partly annotations support
	# url = 'https://github.com/cython/cython/archive/{version}.tar.gz'  # default (in current time) cython
	# site_packages_name = 'cython'
	depends = ['setuptools']

	# Install just for build (exclude app)
	# to use setuptools from hostpython
	call_hostpython_via_targetpython = False
	# install just inside hostpython (native python build on this machine)
	install_in_hostpython = True
	install_in_targetpython = False


recipe = CythonRecipe()
