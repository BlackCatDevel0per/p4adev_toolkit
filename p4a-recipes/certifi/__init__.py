from pythonforandroid.recipe import PythonRecipe as R


class CertifiRecipe(R):

	name = 'certifi'
	version = '2024.2.2'
	url = 'https://pypi.python.org/packages/source/c/certifi/certifi-{version}.tar.gz'
	depends = ['setuptools']

	call_hostpython_via_targetpython = False


recipe = CertifiRecipe()
