"""Build p4adev_tools"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from typing import ClassVar

from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class P4ADevToolsRecipe(NoSetupPyPiRecipe):
	version = 'v0.0.2'
	url = 'https://files.pythonhosted.org/packages/5c/a7/425b81a53dd7de59bfaecb6976d987b381ec80d018fdf7f5cbd09bdf7dbf/p4adev_tools-0.0.2-py3-none-any.whl'

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
	# to use setuotools from hostpython
	call_hostpython_via_targetpython = False
	# install just inside bundle (app's target)
	install_in_hostpython = False
	install_in_targetpython = True


recipe = P4ADevToolsRecipe()
