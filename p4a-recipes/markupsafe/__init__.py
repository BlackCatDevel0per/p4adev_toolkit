"""Build markupsafe"""
from __future__ import annotations

from typing import TYPE_CHECKING

from p4adev_recipes.recipe import AdvancedCompiledComponentsPythonRecipe

if TYPE_CHECKING:
    from typing import List


# Jinja's dependency & p4a dep too..

class MarkupSafeRecipe(AdvancedCompiledComponentsPythonRecipe):
    name: str = 'markupsafe'
    version: str = '2.1.5'
    url: str = 'https://pypi.python.org/packages/source/m/markupsafe/markupsafe-{version}.tar.gz'
    depends: List[str] = ['setuptools']

    # Install just for build (exclude app)
    # to use setuptools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside hostpython (native python build on this machine)
    install_in_hostpython = True
    install_in_targetpython = False


recipe = MarkupSafeRecipe()
