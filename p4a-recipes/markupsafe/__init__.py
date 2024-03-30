"""Build markupsafe"""
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


# Jinja's dependency & p4a dep too..

class MarkupSafeRecipe(AdvancedCompiledComponentsPythonRecipe):
    name: str = 'markupsafe'
    version: str = '2.1.5'
    url: str = 'https://pypi.python.org/packages/source/m/markupsafe/markupsafe-{version}.tar.gz'
    depends: List[str] = ['setuptools']

    # Install just for build (exclude app)
    # to use setuotools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    install_in_targetpython = False


recipe = MarkupSafeRecipe()
