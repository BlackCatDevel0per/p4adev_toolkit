"""Build openssl."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import sh
from pythonforandroid.logger import shprint
from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory

if TYPE_CHECKING:
    from typing import Any, ClassVar

    from pythonforandroid.archs import Arch
    from pythonforandroid.build import Context


class OpenSSLRecipe(Recipe):
    """The OpenSSL libraries for python-for-android.

    This recipe will generate the
    following libraries as shared libraries (*.so):

        - crypto
        - ssl

    The generated openssl libraries are versioned, where the version is the
    recipe attribute :attr:`version` e.g.: ``libcrypto1.1.so``,
    ``libssl1.1.so``...so...to link your recipe with the openssl libs,
    remember to add the version at the end, e.g.:
    ``-lcrypto1.1 -lssl1.1``. Or better, you could do it dynamically
    using the methods: :meth:`include_flags`, :meth:`link_dirs_flags` and
    :meth:`link_libs_flags`.

    .. warning:: This recipe is very sensitive because is used for our core
        recipes, the python recipes. The used API should match with the one
        used in our python build, otherwise we will be unable to build the
        _ssl.so python module.

    .. versionchanged:: 0.6.0

        - The gcc compiler has been deprecated in favour of clang and libraries
          updated to version 1.1.1 (LTS - supported until 11th September 2023)
        - Added two new methods to make easier to link with openssl:
          :meth:`include_flags` and :meth:`link_flags`
        - subclassed versioned_url
        - Adapted method :meth:`select_build_arch` to API 21+
        - Add ability to build a legacy version of the openssl libs when using
          python2legacy or python3crystax.

    .. versionchanged:: 2019.06.06.1.dev0

        - Removed legacy version of openssl libraries

    """

    version: str = '1.1'
    """the major minor version used to link our recipes"""

    url_version: str = '1.1.1w'
    """the version used to download our libraries"""

    url: str = 'https://www.openssl.org/source/openssl-{url_version}.tar.gz'

    built_libraries: ClassVar[dict[str, str]] = {
        f'libcrypto{version}.so': '.',
        f'libssl{version}.so': '.',
    }

    ctx: Context


    @property
    def versioned_url(self: OpenSSLRecipe) -> str:
        if self.url is None:
            return None
        return self.url.format(url_version=self.url_version)


    def get_build_dir(self: OpenSSLRecipe, arch: str) -> str:
        return str(
            Path(
                self.get_build_container_dir(arch), self.name + self.version,
            ),
        )


    def include_flags(self: OpenSSLRecipe, arch: Arch) -> str:
        """Return a string with the include folders."""
        openssl_includes: str = str(Path(self.get_build_dir(arch.arch), 'include'))

        return (
            ' '
            '-I' + openssl_includes + ' '
            '-I' + str(Path(openssl_includes, 'internal')) + ' '
            '-I' + str(Path(openssl_includes, 'openssl'))
        )


    def link_dirs_flags(self: OpenSSLRecipe, arch: Arch) -> str:
        """Return a string with the appropriate `-L<lib directory>` to link with the openssl libs.

        This string is usually added to the environment
        variable `LDFLAGS`
        """
        return ' -L' + self.get_build_dir(arch.arch)


    def link_libs_flags(self: OpenSSLRecipe) -> str:
        """Return the appropriate `-l<lib>` flags to link with the openssl libs.

        This string is usually added to the environment
        variable `LIBS`
        """
        return f' -lcrypto{self.version} -lssl{self.version}'


    def link_flags(self: OpenSSLRecipe, arch: Arch) -> str:
        """Return the flags to link with the openssl libraries.

        Format: `-L<lib directory> -l<lib>`
        """
        return self.link_dirs_flags(arch) + self.link_libs_flags()


    def get_recipe_env(self: OpenSSLRecipe, arch: Arch | None = None) -> dict[str, Any]:
        env = super().get_recipe_env(arch)
        env['OPENSSL_VERSION'] = self.version
        env['MAKE'] = 'make'  # This removes the '-j5', which isn't safe
        env['CC'] = 'clang'
        env['ANDROID_NDK_HOME'] = self.ctx.ndk_dir
        return env

    def select_build_arch(self: OpenSSLRecipe, arch: Arch) -> str:
        aname = arch.arch
        if 'arm64' in aname:
            return 'android-arm64'
        if 'v7a' in aname:
            return 'android-arm'
        if 'arm' in aname:
            return 'android'
        if 'x86_64' in aname:
            return 'android-x86_64'
        if 'x86' in aname:
            return 'android-x86'
        return 'linux-armv4'

    def build_arch(self: OpenSSLRecipe, arch: Arch) -> None:
        env = self.get_recipe_env(arch)

        with current_directory(self.get_build_dir(arch.arch)):
            # sh fails with code 255 trying to execute ./Configure
            # so instead we manually run perl passing in Configure
            perl = sh.Command('perl')

            buildarch: str = self.select_build_arch(arch)

            config_args = [
                # TODO: Try to use system certeficates (or make it optional in the near future..)
                'shared',
                'no-dso',
                'no-asm',
                buildarch,
                f'-D__ANDROID_API__={self.ctx.ndk_api}',
            ]

            shprint(perl, 'Configure', *config_args, _env=env)
            self.apply_patch('disable-sover.patch', arch.arch)
            self.apply_patch('use_app_path_env4conf.patch', arch.arch)

            shprint(sh.make, 'build_libs', _env=env)


recipe = OpenSSLRecipe()
