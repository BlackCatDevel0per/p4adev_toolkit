from __future__ import annotations

from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class ExpandvarsRecipe(NoSetupPyPiRecipe):
    name = 'expandvars'
    version = '0.12.0'
    # In current time we can only use `*.whl`..
    url = 'https://files.pythonhosted.org/packages/df/b3/072c28eace372ba7630ea187b7efd7f09cc8bcebf847a96b5e03e9cc0828/expandvars-0.12.0-py3-none-any.whl'

    # Install just for build (exclude app)
    # to use setuotools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    install_in_targetpython = False


recipe = ExpandvarsRecipe()
