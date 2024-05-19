from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from kivy.lang import Builder
from kivy.logger import Logger
from kivy.resources import resource_add_path
from kivy.utils import platform
from kivymd.app import MDApp

from app import APP_CONF_PATH, module_dir
from app.utility.kv_conf import exclude_kvs, force_include_kvs, unload_kvs
from app.View.screenmanager import AppScreenManager
from app.View.screens import screens

if platform == 'android':
	from android import mActivity
	# TODO: Find or make stubs for java android api used from pyjnius.. or better make mypy plugin..
	context: 'jni[android.content.Context]' = mActivity.getApplicationContext()

if TYPE_CHECKING:
	# NOTE: Type annotations from typing block are still quoted because
	# cython will raise errors in functions & methods annotations.. (but still ok for vars)
	from collections.abc import Callable
	from typing import Any, TypeAlias

	from app.View.base_screen import BaseScreenView
	from app.View.screens import ScreenParams

	BindType: TypeAlias = 'Callable[[Any | str], str]'
	BindsType: TypeAlias = 'dict[BindType, str] | None'


class AppBase(MDApp):

	# TODO: Think about call order..
	# ex. `{'on_build': lambda: print(0), 'on_start': 'cls_method'}`
	# TODO: Use FrozenDict..?
	_binds: 'BindsType' = None
	on_app_init: 'Callable[[], Any]'

	# Exclude helpers (filename, relative path, dirname)
	exclude_kvs: tuple[str, ...] = exclude_kvs
	force_include_kvs: tuple[str, ...] = force_include_kvs
	unload_kvs: tuple[str, ...] = unload_kvs

	app_site: str = ''
	if platform == 'android':
		app_site = str(context.getPackageName())

	app_conf_path: str = APP_CONF_PATH

	def __init__(self: 'AppBase', *args: 'Any', **kwargs: 'Any') -> None:
		super().__init__(*args, **kwargs)

		self.module_directory: str = module_dir
		# for include work
		resource_add_path(self.module_directory)
		# unload some kvs
		# TODO: Move to method..
		fn = None
		for fn in self.unload_kvs:
			Logger.info('kv: Unloading: %s', fn)
			Builder.unload_file(fn)
		del fn
		# load kvs
		self.load_all_kv_files(self.module_directory, self.exclude_kvs, self.force_include_kvs)
		# This is the screen manager that will contain all the screens of your
		# application.
		# TODO: Make transition & some other opts more configurable
		self.manager_screens = AppScreenManager()

		if not self._binds:
			self._binds = {}

		for cls in type(self).mro():
			if hasattr(cls, 'on_app_init'):
				cls.on_app_init(self, **kwargs)


	def load_all_kv_files(
		self: 'AppBase',
		path_to_directory: str,
		excludes: 'tuple[str, ...] | tuple' = (),
		force_includes: 'tuple[str, ...] | tuple' = (),
	) -> None:
		make_tpaths = lambda t: tuple(Path(p) for p in t)  # noqa: E731
		exclude_paths: 'tuple[Path, ...] | tuple' = make_tpaths(excludes)
		force_include_paths: 'tuple[Path, ...] | tuple' = make_tpaths(force_includes)

		search_path = Path(path_to_directory)
		# Filter only kv
		for filepath in search_path.rglob('**/*.kv'):
			path_to_dir = Path(filepath).parent
			# Convert to relative for easier comparison
			path_to_dir_relative: Path = Path(path_to_dir).relative_to(path_to_directory)
			filepath_relative: Path = filepath.relative_to(path_to_directory)
			del path_to_dir, filepath

			# Stuff from standard load:

			# When using the `load_all_kv_files` method, all KV files
			# from the `KivyMD` library were loaded twice, which leads to
			# failures when using application built using `PyInstaller`.
			if 'kivymd' in path_to_dir_relative.parents:
				Logger.critical(
					'KivyMD: '
					"Do not use the word 'kivymd' in the name of the directory "
					'from where you download KV files',
				)

			# Exclude filter
			is_excluded: bool = False
			epath = None
			for epath in exclude_paths:
				if any(
					(
						# Exclude filename
						(len(epath.parents) == 1 and str(epath) == filepath_relative.name),
						# Exclude relative path (directory or file)
						(len(epath.parents) > 1 and (
							epath == filepath_relative or epath in filepath_relative.parents)),
					),
				):
					is_excluded = True
					break
			del epath

			# TODO: Unite..
			# Force include filter
			is_force_included: bool = False
			ipath = None
			for ipath in force_include_paths:
				if any(
					(
						# Include filename
						(len(ipath.parents) == 1 and str(ipath) == filepath_relative.name),
						# Include relative path (directory or file)
						(len(ipath.parents) > 1 and (
							ipath == filepath_relative or ipath in filepath_relative.parents)),
					),
				):
					is_excluded = False
					is_force_included = True
					break
			del ipath

			if is_excluded:
				Logger.info('kv: Excluded "%s"', str(filepath_relative))
				continue

			if is_force_included:
				Logger.info('kv: Force included "%s"', str(filepath_relative))

			path_to_kv_file: str = str(filepath_relative)
			Logger.info('kv: Loading "%s"', path_to_kv_file)
			Builder.load_file(path_to_kv_file)


	# TODO: Not recreate set..


	def bind_to(self: 'AppBase', dct: 'BindsType') -> None:
		# TODO: Mb need more params with more plexible options..
		self._binds.update(dct)


	@property
	def binds(self: 'AppBase') -> 'BindsType':
		return self._binds


	def build(self: 'AppBase') -> AppScreenManager:
		self.theme_cls.theme_style_switch_animation = True
		self.binds_run('on_build')

		self.generate_application_screens()
		return self.manager_screens


	def generate_application_screens(self: 'AppBase') -> None:
		"""Create and add screens to the screen manager.

		You should not change this cycle unnecessarily. He is self-sufficient.

		If you need to add any screen, open the `view.screens.py` module and
		see how new screens are added according to the given application
		architecture.
		"""
		# FIXME: DRYS..
		# TODO: More annotate..
		screen: 'ScreenParams'
		for screen_name, screen in screens.items():
			model = screen['model']()
			controller = screen['controller'](model)
			view: BaseScreenView = controller.view

			# TODO: Use other way to set these properties..
			##
			view.manager_screens = self.manager_screens
			view.name = screen_name
			self.manager_screens.add_widget(view)


	def binds_run(self: 'AppBase', on_event: str) -> None:
		for action, on in self.binds.items():
			if on != on_event:
				continue

			if isinstance(action, str):
				ins_act: 'Callable[[], Any]' = getattr(self, action)
				ins_act()
				continue

			action()


	def on_start(self: 'AppBase') -> None:
		super().on_start()

		self.binds_run('on_start')

		for view in self.manager_screens.screens:
			view.startup()  # TODO: Check/make startup/shutdown methods..
