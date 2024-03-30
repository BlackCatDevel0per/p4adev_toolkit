"""Build charset_normalizer"""
from typing import TYPE_CHECKING

from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe

if TYPE_CHECKING:
    from typing import List


class CharsetNormalizerRecipe(CppCompiledComponentsPythonRecipe):
    version: str = '3.3.2'
    url: str = 'https://pypi.python.org/packages/source/c/charset_normalizer/charset_normalizer-{version}.tar.gz'
    name: str = 'charset_normalizer'
    depends: List[str] = ['setuptools']


recipe = CharsetNormalizerRecipe()
