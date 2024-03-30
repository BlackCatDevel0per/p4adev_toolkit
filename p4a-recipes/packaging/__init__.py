from __future__ import annotations

import sys
from pathlib import Path

# A little hack..
recipes_path = Path(__file__).parent.parent

if str(recipes_path) not in sys.path:
    sys.path.insert(0, str(recipes_path))

from utils.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class PackagingRecipe(NoSetupPyPiRecipe):
    name = 'packaging'
    version = '24.0'
    # In current time we can only use `*.whl`..
    url = 'https://files.pythonhosted.org/packages/49/df/1fceb2f8900f8639e278b056416d49134fb8d84c5942ffaa01ad34782422/packaging-24.0-py3-none-any.whl'

    # Install just for build (exclude app)
    # to use setuotools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    # NOTE: Change if you don't need
    # install_in_targetpython = False
    install_in_targetpython = True


recipe = PackagingRecipe()
