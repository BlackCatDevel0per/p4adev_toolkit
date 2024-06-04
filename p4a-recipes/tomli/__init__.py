from __future__ import annotations

from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class TomliRecipe(NoSetupPyPiRecipe):
    name = 'tomli'
    version = '2.0.1'
    # In current time we can only use `*.whl`..
    url = 'https://files.pythonhosted.org/packages/97/75/10a9ebee3fd790d20926a90a2547f0bf78f371b2f13aa822c759680ca7b9/tomli-2.0.1-py3-none-any.whl'

    # Install just for build (exclude app)
    # to use setuptools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    install_in_targetpython = False


recipe = TomliRecipe()
