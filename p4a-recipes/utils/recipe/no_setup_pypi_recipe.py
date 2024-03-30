"""Build yarl"""
from __future__ import annotations

import sys
from os.path import dirname, join
from pathlib import Path

import sh
from pythonforandroid.logger import info, shprint
from pythonforandroid.recipe import PythonRecipe
from pythonforandroid.util import current_directory

# A little hack..
# TODO: Make function to do this stuff properly & clean sys after script main jobs ends..
recipes_path = Path(__file__).parent.parent.parent

if str(recipes_path) not in sys.path:
    sys.path.insert(0, str(recipes_path))

from utils.bundle_installer import _main as bundle_installer


class NoSetupPyPiRecipe(PythonRecipe):

	filename: 'str | None' = None
	# TODO: Use pkginfo to install some dependencies..

	def __init__(self, *args, **kwargs):
		# TODO: Extract basename without system tools using pathlib or url parsers..
		if not self.filename:
			self.filename = shprint(sh.basename, self.versioned_url).stdout[:-1].decode('utf-8')

		super().__init__(*args, **kwargs)


	def prepare_build_dir(self, arch=None):
		# Do nothing because we don't need unpack, because all stuff do installer
		return


	def install_python_package(self, arch, name=None, env=None, is_dir=True):
		""""""
		if name is None:
			name = self.name
		if env is None:
			env = self.get_recipe_env(arch)

		info('Installing {} into site-packages'.format(self.name))

		with current_directory(join(self.ctx.packages_path, self.name)):
			if self.install_in_targetpython:
				bundle_installer(
					[
						'--prefix={}'.format(self.ctx.get_python_install_dir(arch.arch)),
						self.filename,
					],
				)

			# If asked, also install in the hostpython build dir
			if self.install_in_hostpython:
				self.install_hostpython_package(arch)


	def install_hostpython_package(self, arch):
		with current_directory(join(self.ctx.packages_path, self.name)):
			bundle_installer(
				[
					# TODO: Check it..
					'--prefix={}'.format(
						join(
							self.get_build_dir(arch.arch),
							dirname(self.real_hostpython_location),
							'Lib/site-packages',
						),
					),
					self.filename,
				],
			)
