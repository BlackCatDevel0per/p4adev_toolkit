from __future__ import annotations

from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class PyProjectHooksRecipe(NoSetupPyPiRecipe):
    name = 'pyproject_hooks'
    version = '1.0.0'
    # In current time we can only use `*.whl`..
    url = 'https://files.pythonhosted.org/packages/d5/ea/9ae603de7fbb3df820b23a70f6aff92bf8c7770043254ad8d2dc9d6bcba4/pyproject_hooks-1.0.0-py3-none-any.whl'

    # Install just for build (exclude app)
    # to use setuotools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    install_in_targetpython = False


recipe = PyProjectHooksRecipe()
