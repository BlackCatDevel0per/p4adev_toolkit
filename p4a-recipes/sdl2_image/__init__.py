import os

import sh
from buildozer.scripts.cachetools import select_git
from pythonforandroid.logger import shprint
from pythonforandroid.recipe import BootstrapNDKRecipe
from pythonforandroid.util import current_directory


class LibSDL2Image(BootstrapNDKRecipe):
	"""Overrides original recipe for using caching."""

	version = '2.6.2'
	url = 'https://github.com/libsdl-org/SDL_image/releases/download/release-{version}/SDL2_image-{version}.tar.gz'
	dir_name = 'SDL2_image'

	patches = ['enable-webp.patch']

	def prebuild_arch(self, arch):
		# We do not have a folder for each arch on BootstrapNDKRecipe, so we
		# need to skip the external deps download if we already have done it.
		external_deps_dir = os.path.join(self.get_build_dir(arch.arch), "external")
		if not os.path.exists(os.path.join(external_deps_dir, "libwebp")):
			with current_directory(external_deps_dir):
				if os.environ.get('USE_P4A_RECIPES_CACHING'):
					with open('download.sh', 'r') as df:
						data = df.read()
					# Crutchy~ but works..
					with open('download.sh', 'w') as df:
						data = data.replace(
							'git clone', f'{select_git(allow_cache=True, force_cache=True)} clone',
						)
						df.write(data)
						del data
				shprint(sh.Command("./download.sh"))
		super().prebuild_arch(arch)


recipe = LibSDL2Image()
