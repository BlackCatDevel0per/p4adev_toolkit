# NOTE: If you want to use partly-working annotations with cython 0.29.x please use this fork:
# https://github.com/BlackCatDevel0per/cython

# NOTE: Relative imports don't works!!!
# Mb can work something like `.some_module_pkg` but not other ways instead of absolute import..

from __future__ import annotations

from os import environ as os_env
from pathlib import Path
from typing import TYPE_CHECKING

from kivy.config import Config
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd2_widgets.pickers import MDThemePicker

from app import module_dir
from app.View.screens import screens

if platform == 'android':
	from android import mActivity
	# TODO: Find or make stubs for java android api used from pyjnius.. or better make mypy plugin..
	context: 'jni[android.content.Context]' = mActivity.getApplicationContext()
	from jnius import autoclass
else:
	import sys
	from multiprocessing import Process
	from subprocess import Popen

if TYPE_CHECKING:
	# NOTE: Type annotations from typing block are still quoted because
	# cython will raise errors in functions & methods annotations.. (but still ok for vars)
	from typing import Any

	from kivy.config import ConfigParser

	from app.View.base_screen import BaseScreenView
	from app.View.screens import ScreenParams


class App(MDApp):

	if platform == 'android':
		app_site: str = str(context.getPackageName())

	def __init__(self: 'App', **kwargs: 'Any') -> None:
		super().__init__(**kwargs)
		self.module_directory: str = module_dir
		self.load_all_kv_files(self.module_directory)
		# This is the screen manager that will contain all the screens of your
		# application.
		self.manager_screens = MDScreenManager()


	def get_application_config(
		self: 'App',
		default_path: str = os_env.get(
			'ANDROID_APP_PATH',
			str(Path(Path.cwd(), 'config.ini')),
		)
	) -> str:
		"""Set default config path."""
		return default_path


	def build_config(self: 'App', config: 'ConfigParser') -> None:
		# TODO: Use TypedDict with Literal(s).. (for easier lint)
		config.setdefaults(
			'theme',
			{
				'palette': 'Teal',
				'accent': 'Green',
				'style': 'Dark',
			},
		)

		config.setdefaults(
			'app',
			{
				'docs_dir': '',
			},
		)


	def build(self: 'App') -> MDScreenManager:
		self.theme_cls.theme_style_switch_animation = True
		self.set_accent_style()

		self.generate_application_screens()
		return self.manager_screens


	def set_accent_style(self: 'App') -> None:
		self.theme_cls.primary_palette = self.config.get('theme', 'palette')
		self.theme_cls.accent_palette = self.config.get('theme', 'accent')
		self.theme_cls.theme_style = self.config.get('theme', 'style')

		self.config.write()


	def save_accent_style(self: 'App') -> None:
		self.config.set('theme', 'palette', self.theme_cls.primary_palette)
		self.config.set('theme', 'accent', self.theme_cls.accent_palette)
		self.config.set('theme', 'style', self.theme_cls.theme_style)

		self.config.write()


	def switch_accent_style(self: 'App') -> None:
		theme_picker = MDThemePicker()
		theme_picker.on_dismiss = self.save_accent_style
		theme_picker.open()


	def generate_application_screens(self: 'App') -> None:
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


	def _start_service(
		self: 'App',
		name: str,
		method: str = 'proc',
		module: 'str | None' = None,
		import_kw: 'dict[str, Any]' = {'fromlist': ['']},  # noqa: B006
	) -> 'Service | Process':
		if platform == 'android':
			sn: str = f'{self.app_site}.Service{name}'
			service = autoclass(sn)
			del sn
			service.start(mActivity, '')
			return service

		if module is None:
			msg = 'Missing module arg for non-android platform..'
			raise TypeError(msg)

		if method == 'proc':
			m = __import__(module, **import_kw)
			process = Process(target=m.main)
			process.start()
		elif method == 'subproc':
			# FIXME: Soooo crutchy..
			module = 'src' + '/' + module
			process = Popen([sys.executable, f"{module.replace('.', '/')}.py"])

		return process


	def start_services(self: 'App') -> None:
		# IPYkernel for jupyter console connect

		# self.dev_ipy_service = self._start_service(
		# 	'Devipykernel',
		# 	'subproc',
		# 	'app.services.dev_ipykernel',
		# )
		...


	def on_start(self: 'App') -> None:
		super().on_start()

		# TODO: Kill procs on exit..
		self.start_services()

		for view in self.manager_screens.screens:
			view.startup()  # TODO: Check/make startup/shutdown methods..


def run() -> None:
	"""Run the app."""
	# TODO: Set config file path..
	# TODO: Handle back button press
	# TODO: Write some info on main screen..

	# TODO: Cookiecutter or etc. template

	Config.set('graphics', 'maxfps', '15')

	# Set startup orientation because value from manifest is ignored..
	# (depends on the system auto-rotate option)
	if platform == 'android':
		ActivityInfo = autoclass('android.content.pm.ActivityInfo')

		mActivity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_FULL_USER)

	App().run()
