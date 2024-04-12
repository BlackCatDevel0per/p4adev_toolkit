# TODO: Move into under-dir..
import sys

import sh
from pythonforandroid.logger import shprint
from pythonforandroid.recipe import CythonRecipe as R
from pythonforandroid.util import current_directory

# TODO: Move to toml..
# TODO: Compare changes..


class AppRecipe(R):

	name = 'app'
	# TODO: Versioning..?
	# TODO: Set sources out of spec..?
	depends = ['setuptools']

	def prebuild_arch(self, arch):
		with current_directory(self.get_build_dir(arch.arch)):
			# Force remove any `.c` files
			shprint(sh.Command('find'), '.', '-name', '*.c', '-delete')
			# Make new `.c` files
			shprint(sh.Command(sys.executable), 'setup.py', 'sdist')
			# Force clean dists
			shprint(sh.Command('rm'), '-rf', '*.egg-info', 'dist', 'build')

		super().prebuild_arch(arch)

	def should_build(self, arch):
		return True


recipe = AppRecipe()
