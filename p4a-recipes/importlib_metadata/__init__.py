from __future__ import annotations

from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class ImportlibMetadataRecipe(NoSetupPyPiRecipe):
    name = 'importlib_metadata'
    version = '7.1.0'
    # In current time we can only use `*.whl`..
    url = 'https://files.pythonhosted.org/packages/2d/0a/679461c511447ffaf176567d5c496d1de27cbe34a87df6677d7171b2fbd4/importlib_metadata-7.1.0-py3-none-any.whl'

    # Install just for build (exclude app)
    # to use setuptools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    # NOTE: Change if you don't need
    # install_in_targetpython = False
    install_in_targetpython = True


recipe = ImportlibMetadataRecipe()
