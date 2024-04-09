from multiprocessing import cpu_count
from os.path import join

import sh
from pythonforandroid.logger import shprint
from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory


class LibffiRecipe(Recipe):
	"""libffi recipe.

	Require additional system dependencies on Ubuntu:
		- `automake` for the `aclocal` binary
		- `autoconf` for the `autoreconf` binary
		- `libltdl-dev` which defines the `LT_SYS_SYMBOL_USCORE` macro
	"""

	name = 'libffi'
	version = 'v3.4.6'
	url = 'https://github.com/libffi/libffi/archive/{version}.tar.gz'

	patches = ['remove-version-info.patch']

	built_libraries = {'libffi.so': '.libs'}

	def build_arch(self, arch):
		env = self.get_recipe_env(arch)
		with current_directory(self.get_build_dir(arch.arch)):
			# old way:
			# if not exists('configure'):
			#     shprint(sh.Command('./autogen.sh'), _env=env)
			shprint(sh.Command('autoreconf'), '-vif', _env=env)
			shprint(
				sh.Command('./configure'),
				'--host=' + arch.command_prefix,
				'--prefix=' + self.get_build_dir(arch.arch),
				'--disable-builddir',
				'--enable-shared',
				_env=env,
			)
			shprint(sh.make, '-j', str(cpu_count()), 'libffi.la', _env=env)

	def get_include_dirs(self, arch):
		return [join(self.get_build_dir(arch.arch), 'include')]


recipe = LibffiRecipe()
