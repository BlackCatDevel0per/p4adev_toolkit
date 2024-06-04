"""Build jedi"""
from __future__ import annotations

from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class JediRecipe(NoSetupPyPiRecipe):
    version = 'v0.19.1'
    url = 'https://files.pythonhosted.org/packages/20/9f/bc63f0f0737ad7a60800bfd472a4836661adae21f9c2535f3957b1e54ceb/jedi-0.19.1-py2.py3-none-any.whl'

    # Install just for app (exclude native/host machine build)
    # to use setuptools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside bundle (app's target)
    install_in_hostpython = False
    install_in_targetpython = True


recipe = JediRecipe()
