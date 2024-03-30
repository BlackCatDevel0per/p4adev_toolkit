"""Build multidict"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

# A little hack..
recipes_path = Path(__file__).parent.parent

if str(recipes_path) not in sys.path:
    sys.path.insert(0, str(recipes_path))

from utils.recipe import AdvancedCompiledComponentsPythonRecipe

if TYPE_CHECKING:
    from typing import List


class MultiDictRecipe(AdvancedCompiledComponentsPythonRecipe):
    name: str = 'multidict'
    version: str = '6.0.5'
    url: str = 'https://pypi.python.org/packages/source/m/multidict/multidict-{version}.tar.gz'
    depends: List[str] = ['setuptools']

    # Install just for app (exclude native/host machine build)
    # to use setuotools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside bundle (app's target)
    install_in_hostpython = False
    install_in_targetpython = True


recipe = MultiDictRecipe()
