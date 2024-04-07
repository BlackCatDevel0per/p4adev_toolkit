# TODO: Move into under-dir..

from pythonforandroid.recipe import CythonRecipe as R
# TODO: Move to toml..
# TODO: Compare changes..


class AppRecipe(R):

	name = 'app'
	# TODO: Versioning..?
	# TODO: Set sources out of spec..?
	depends = ['setuptools']

	def prebuild_arch(self, arch):
		super().prebuild_arch(arch)

		...

	def should_build(self, arch):
		return True


recipe = AppRecipe()
