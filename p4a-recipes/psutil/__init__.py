"""Build psutil"""
from __future__ import annotations

from typing import TYPE_CHECKING

from p4adev_recipes.recipe import AdvancedCompiledComponentsPythonRecipe

if TYPE_CHECKING:
    from typing import List


class PsutilRecipe(AdvancedCompiledComponentsPythonRecipe):
    name: str = 'psutil'
    version: str = '5.9.8'
    url: str = 'https://pypi.python.org/packages/source/p/psutil/psutil-{version}.tar.gz'
    depends: List[str] = ['setuptools']

    # Install just for app (exclude native/host machine build)
    # to use setuotools from hostpython
    call_hostpython_via_targetpython = False
    # install just inside bundle (app's target)
    install_in_hostpython = False
    install_in_targetpython = True


recipe = PsutilRecipe()
