"""Build colorama"""
from __future__ import annotations

from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class ColoramaRecipe(NoSetupPyPiRecipe):
    name = 'colorama'
    version = '0.4.6'
    # In current time we can only use `*.whl`..
    url = 'https://files.pythonhosted.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl'

    # Install just for build (exclude app)
    # to use setuotools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    # NOTE: Change if you don't need
    # install_in_targetpython = False
    install_in_targetpython = True


recipe = ColoramaRecipe()
