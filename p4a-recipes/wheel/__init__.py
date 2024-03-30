from __future__ import annotations

import sys
from pathlib import Path

# A little hack..
recipes_path = Path(__file__).parent.parent

if str(recipes_path) not in sys.path:
    sys.path.insert(0, str(recipes_path))

from utils.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class WheelRecipe(NoSetupPyPiRecipe):
    name = 'wheel'
    version = '0.43.0'
    # In current time we can only use `*.whl`..
    url = 'https://files.pythonhosted.org/packages/7d/cd/d7460c9a869b16c3dd4e1e403cce337df165368c71d6af229a74699622ce/wheel-0.43.0-py3-none-any.whl'

    # Install just for build (exclude app)
    # to use setuotools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    install_in_targetpython = False


recipe = WheelRecipe()
