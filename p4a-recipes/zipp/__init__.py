"""Build zipp"""
from __future__ import annotations

from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class ZippRecipe(NoSetupPyPiRecipe):
    name = 'zipp'
    version = '1.1.1'
    # In current time we can only use `*.whl`..
    url = 'https://files.pythonhosted.org/packages/c2/0a/ba9d0ee9536d3ef73a3448e931776e658b36f128d344e175bc32b092a8bf/zipp-3.18.1-py3-none-any.whl'

    # Install just for build (exclude app)
    # to use setuotools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    # NOTE: Change if you don't need
    # install_in_targetpython = False
    install_in_targetpython = True


recipe = ZippRecipe()
