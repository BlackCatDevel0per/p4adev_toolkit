# TODO: Move into under-dir..

from pythonforandroid.recipe import CythonRecipe as R
# TODO: Move to toml..
# TODO: Compare changes..


class MainRecipe(R):

	name = 'p4a_dev'
	# TODO: Versioning..?
	# TODO: Set sources out of spec..?
	depends = ['setuptools']

	def prebuild_arch(self, arch):
		super().prebuild_arch(arch)

		...

	def should_build(self, arch):
		return True


recipe = MainRecipe()
