from __future__ import annotations

from p4adev_recipes.recipe.no_setup_pypi_recipe import NoSetupPyPiRecipe


##
class BuildRecipe(NoSetupPyPiRecipe):
    name = 'build'
    version = '1.1.1'
    # TODO: Recheck deps..
    depends = [
        'colorama',

        # 'setuptools',##
        # 'cython==0.29.28',##
        # 'git+https://github.com/BlackCatDevel0per/cython/archive/master.tar.gz',

        'expandvars',
        'importlib_metadata',
        'packaging',
        'pyproject_hooks',
        'tomli',
        'wheel',
        'zipp',
    ]
    # In current time we can only use `*.whl`..
    url = 'https://files.pythonhosted.org/packages/4f/81/4849059526d02fcc9708e19346dd740e8b9edd2f0675ea7c38302d6729df/build-1.1.1-py3-none-any.whl'

    # Install just for build (exclude app)
    call_hostpython_via_targetpython = False
    install_in_hostpython = True
    install_in_targetpython = False


recipe = BuildRecipe()
