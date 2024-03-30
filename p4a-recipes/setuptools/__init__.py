from __future__ import annotations

import sys
from pathlib import Path

# A little hack..
recipes_path = Path(__file__).parent.parent

if str(recipes_path) not in sys.path:
    sys.path.insert(0, str(recipes_path))

from utils.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


class SetuptoolsRecipe(NoSetupPyPiRecipe):
    name = 'setuptools'
    version = '69.2.0'
    # url = 'https://pypi.python.org/packages/source/s/setuptools/setuptools-{version}.tar.gz'
    url = 'https://files.pythonhosted.org/packages/92/e1/1c8bb3420105e70bdf357d57dd5567202b4ef8d27f810e98bb962d950834/setuptools-69.2.0-py3-none-any.whl'

    # Install just for build (exclude app)
    # to use setuotools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    install_in_targetpython = False


recipe = SetuptoolsRecipe()
