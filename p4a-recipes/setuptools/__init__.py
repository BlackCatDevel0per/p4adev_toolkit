from __future__ import annotations

from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class SetuptoolsRecipe(NoSetupPyPiRecipe):
    name = 'setuptools'
    version = '69.2.0'
    # url = 'https://pypi.python.org/packages/source/s/setuptools/setuptools-{version}.tar.gz'
    url = 'https://files.pythonhosted.org/packages/92/e1/1c8bb3420105e70bdf357d57dd5567202b4ef8d27f810e98bb962d950834/setuptools-69.2.0-py3-none-any.whl'

    # Install just for build (exclude app)
    # to use setuptools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    install_in_targetpython = False


recipe = SetuptoolsRecipe()
