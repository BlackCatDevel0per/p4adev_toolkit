"""Build p4adev_tools"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from typing import ClassVar

from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class P4ADevToolsRecipe(NoSetupPyPiRecipe):
	version = 'v0.0.3'
	url = 'https://files.pythonhosted.org/packages/cd/25/d9105a3fcaec2cb42c66375ccf83b0249fe558f9dcb1f6b734112b24917b/p4adev_tools-0.0.3-py3-none-any.whl'

	depends: ClassVar[list[str]] = [
		'pyftpdlib',
		'wcwidth',
		'pure-eval',
		'ptyprocess',
		'traitlets',
		'tornado',
		'six',
		'pyzmq',
		'pygments',
		'psutil',
		'prompt-toolkit',
		'platformdirs',
		'pexpect',
		'parso',
		'packaging',
		'nest-asyncio',
		'executing',
		'exceptiongroup',
		'decorator',
		'python-dateutil',
		'jupyter-core',
		'jedi==0.19.1',
		'comm',
		'asttokens',
		'stack-data',
		'jupyter-client',
		'typing-extensions',
		'ipython',
		'ipykernel',
		'background_zmq_ipython',
	]

	# Install just for app (exclude native/host machine build)
	# to use setuptools from hostpython
	call_hostpython_via_targetpython = False
	# install just inside bundle (app's target)
	install_in_hostpython = False
	install_in_targetpython = True


recipe = P4ADevToolsRecipe()
