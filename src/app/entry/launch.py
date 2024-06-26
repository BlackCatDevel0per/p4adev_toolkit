# NOTE: If you want to use partly-working annotations with cython 0.29.x please use this fork:
# https://github.com/BlackCatDevel0per/cython

# NOTE: Relative imports don't works!!!
# Mb can work something like `.some_module_pkg` but not other ways instead of absolute import..

from __future__ import annotations  # noqa: I001

from typing import TYPE_CHECKING

# Log conf
from app.utility import logger  # noqa: F401

from kivy.config import Config

from app.bases import (
	AdsAdmob,
	AppBase,
	AppBroadcast,
	AppConf,
	AppDebug,
	AppServices,
	AppStyle,
	AppTweaks,
)

if TYPE_CHECKING:
	# NOTE: Type annotations from typing block are still quoted because
	# cython v0.29.37 will raise errors in functions & methods annotations.. (but still ok for vars)
	...


class App(AppTweaks, AppConf, AppServices, AppStyle, AppDebug, AdsAdmob, AppBase, AppBroadcast):
	...


def run() -> None:
	"""Run the app."""
	# TODO: i18n
	# TODO: More ads apis integrate..
	# TODO: AsyncIO branch
	# TODO: Cythonize command to check if annotations are correct for build
	# TODO: Make docker container with all stuff & notebook on google colab

	# TODO: Cookiecutter or etc. template

	Config.set('graphics', 'maxfps', '15')

	App().run()
