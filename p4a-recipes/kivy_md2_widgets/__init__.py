from pythonforandroid.recipe import PythonRecipe as R


class MainRecipe(R):

	name = 'kivy_md2_widgets'
	# TODO: Versioning..?
	# TODO: Set sources out of spec..?
	depends = ['setuptools']

	call_hostpython_via_targetpython = False


recipe = MainRecipe()
