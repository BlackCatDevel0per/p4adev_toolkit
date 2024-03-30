"""Build yarl"""
from __future__ import annotations

import glob
import shutil
import sys
from os.path import dirname
from pathlib import Path

import sh
from pythonforandroid.logger import info, shprint
from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from pythonforandroid.util import current_directory

# A little hack..
recipes_path = Path(__file__).parent.parent.parent

if str(recipes_path) not in sys.path:
    sys.path.insert(0, str(recipes_path))

from utils.bundle_installer import _main as bundle_installer

# TODO: Unite some methods..


class BuildToolCompiledComponentsPythonRecipe(CompiledComponentsPythonRecipe):

	# FIXME: Fully rename plat for build backends..
	# FIXME: (include binaries.. apps works correct, but in build dir sill incorrect plat suffixes/prefixes in binary names..)
	_tool = 'build'

	_tool_in_deps = True

	# to use build & setuptools
	call_hostpython_via_targetpython = False

	def __init__(self, *args, **kwargs):
		if self._tool_in_deps and self._tool not in self.depends:
			self.depends.append(self._tool)

		self.depends = list(set(self.depends))

		super().__init__(*args, **kwargs)


	def get_hostrecipe_env(self, arch):
		env = super().get_hostrecipe_env(arch)
		env['RANLIB'] = shutil.which('ranlib')

		return env


	def build_compiled_components(self, arch):
		""""""
		info('Building compiled components in {}'.format(self.name))

		env = self.get_recipe_env(arch)
		hostpython = sh.Command(self.hostpython_location)
		with current_directory(self.get_build_dir(arch.arch)):
			# Build always using host binaries
			if not self.install_in_hostpython and not self.install_in_targetpython:
				return

			self._build_bundle(hostpython, env)
			# FIXME: Recheck why strips fails..
			# build_dir = glob.glob('build/lib.*')[0]
			# shprint(sh.find, build_dir, '-name', '"*.o"', '-exec',
			# 		env['STRIP'], '{}', ';', _env=env)


	def install_python_package(self, arch, name=None, env=None, is_dir=True):
		""""""
		if name is None:
			name = self.name
		if env is None:
			env = self.get_recipe_env(arch)

		info('Installing {} into site-packages'.format(self.name))

		with current_directory(self.get_build_dir(arch.arch)):
			if self.install_in_targetpython:
				self._install_bundle(self.ctx.get_python_install_dir(arch.arch), arch)

			# If asked, also install in the hostpython build dir
			if self.install_in_hostpython:
				self.install_hostpython_package(arch)

	def _install_bundle(self, prefix, arch):
		wheel_file: str = glob.glob('dist/*.whl')[0]

		bundle_installer(
			[
				'--prefix={}'.format(prefix),
				wheel_file,
			],
		)


	def _build_bundle(self, py_command, env):
		# TODO: Skip if already installed..
		shprint(
			py_command, '-m', self._tool, '--wheel', '--no-isolation', _env=env,
			*self.setup_extra_args,
		)


	def install_hostpython_package(self, arch):
		env = self.get_hostrecipe_env(arch)
		self.rebuild_compiled_components(arch, env)

		# real_hostpython = sh.Command(self.real_hostpython_location)
		self._install_bundle(dirname(self.real_hostpython_location), arch)


	def rebuild_compiled_components(self, arch, env):
		info('Rebuilding compiled components in {}'.format(self.name))

		hostpython = sh.Command(self.real_hostpython_location)
		self._build_bundle(hostpython, env)
