from __future__ import annotations

from typing import TYPE_CHECKING

from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from app import module_dir
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

	app_site: str = ''
	if platform == 'android':
		app_site = str(context.getPackageName())

	def __init__(self: 'AppBase', **kwargs: 'Any') -> None:
		super().__init__(**kwargs)
		self.module_directory: str = module_dir
		self.load_all_kv_files(self.module_directory)
		# This is the screen manager that will contain all the screens of your
		# application.
		self.manager_screens = MDScreenManager()

		if not self._binds:
			self._binds = {}

		for cls in type(self).mro():
			if hasattr(cls, 'on_app_init'):
				cls.on_app_init(self, **kwargs)


	# TODO: Not recreate set..


	def bind_to(self: 'AppBase', dct: 'BindsType') -> None:
		self._binds.update(dct)


	@property
	def binds(self: 'AppBase') -> 'BindsType':
		return self._binds


	def build(self: 'AppBase') -> MDScreenManager:
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
		screen: 'ScreenParams'
		for screen_name, screen in screens.items():
			model = screen['model']()
			controller = screen['controller'](model)
			view: BaseScreenView = controller.view

			# TODO: Use other way to set these properties..
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
