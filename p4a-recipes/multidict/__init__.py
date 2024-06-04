"""Build multidict"""
from __future__ import annotations

from typing import TYPE_CHECKING

from p4adev_recipes.recipe import AdvancedCompiledComponentsPythonRecipe

if TYPE_CHECKING:
    from typing import List


class MultiDictRecipe(AdvancedCompiledComponentsPythonRecipe):
    name: str = 'multidict'
    version: str = '6.0.5'
    url: str = 'https://pypi.python.org/packages/source/m/multidict/multidict-{version}.tar.gz'
    depends: List[str] = ['setuptools']

    # Install just for app (exclude native/host machine build)
    # to use setuptools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside bundle (app's target)
    install_in_hostpython = False
    install_in_targetpython = True


recipe = MultiDictRecipe()
