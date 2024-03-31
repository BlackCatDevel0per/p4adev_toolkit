from pythonforandroid.recipe import BootstrapNDKRecipe


class LibSDL2TTF(BootstrapNDKRecipe):
    version = '2.22.0'
    url = 'https://github.com/libsdl-org/SDL_ttf/releases/download/release-{version}/SDL2_ttf-{version}.tar.gz'
    dir_name = 'SDL2_ttf'

    def get_recipe_env(self, arch=None, with_flagc_in_cc=True) -> 'env':
        env = super().get_recipe_env(arch, with_flagc_in_cc).copy()

        # TODO: Open issue on github
        # to avoid SDL2_ttf warning
        env['CPPFLAGS'] += ' -Wno-cast-function-type-strict'

        return env


recipe = LibSDL2TTF()
