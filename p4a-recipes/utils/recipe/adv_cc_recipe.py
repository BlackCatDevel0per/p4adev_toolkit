import glob

import sh
from pythonforandroid.logger import info, shprint
from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from pythonforandroid.util import current_directory


class AdvancedCompiledComponentsPythonRecipe(CompiledComponentsPythonRecipe):

	def build_compiled_components(self, arch):
		""""""
		info('Building compiled components in {}'.format(self.name))

		env = self.get_recipe_env(arch)
		hostpython = sh.Command(self.hostpython_location)
		with current_directory(self.get_build_dir(arch.arch)):
			# Build always using host binaries
			if not self.install_in_hostpython and not self.install_in_targetpython:
				return

			if self.install_in_hostpython:
				shprint(hostpython, 'setup.py', 'clean', '--all', _env=env)
			shprint(hostpython, 'setup.py', self.build_cmd, '-v',
					_env=env, *self.setup_extra_args)

			build_dir = glob.glob('build/lib.*')[0]
			shprint(sh.find, build_dir, '-name', '"*.o"', '-exec',
					env['STRIP'], '{}', ';', _env=env)


	def install_python_package(self, arch, name=None, env=None, is_dir=True):
		""""""
		if name is None:
			name = self.name
		if env is None:
			env = self.get_recipe_env(arch)

		info('Installing {} into site-packages'.format(self.name))

		hostpython = sh.Command(self.hostpython_location)
		hpenv = env.copy()
		with current_directory(self.get_build_dir(arch.arch)):
			if self.install_in_targetpython:
				shprint(hostpython, 'setup.py', 'install', '-O2',
					'--root={}'.format(self.ctx.get_python_install_dir(arch.arch)),
					'--install-lib=.',
					_env=hpenv, *self.setup_extra_args)

			# If asked, also install in the hostpython build dir
			if self.install_in_hostpython:
				self.install_hostpython_package(arch)
