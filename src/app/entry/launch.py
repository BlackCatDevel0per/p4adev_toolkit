from __future__ import annotations

from typing import TYPE_CHECKING

# Relative imports don't works!!!
# Mb can work something like `.some_module_pkg` but not other ways instead of absolute import..

if TYPE_CHECKING:
	from typing import Any

	from app.View.base_screen import BaseScreenView
	from app.View.screens import ScreenParams


from pathlib import Path

from kivy.config import Config
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd2_widgets.pickers import MDThemePicker

from app.View.screens import screens

if platform == 'android':
	from android import mActivity
	context = mActivity.getApplicationContext()
	from jnius import autoclass
else:
	import sys
	from multiprocessing import Process
	from subprocess import Popen


class App(MDApp):

	if platform == 'android':
		app_site: str = str(context.getPackageName())

	def __init__(self: 'App', **kwargs: 'Any') -> None:
		super().__init__(**kwargs)
		# FIXME: Do it properly..
		self.module_directory = str(Path(self.directory).parent)
		self.load_all_kv_files(self.module_directory)
		# This is the screen manager that will contain all the screens of your
		# application.
		self.manager_screens = MDScreenManager()


	def build_config(self: 'App', config):
		config.setdefaults(
			'theme',
			{
				'palette': 'Teal',
				'accent': 'Green',
				'style': 'Dark',
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


	def switch_accent_style(self) -> None:
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
		import_kw: 'dict[str, Any]' = {'fromlist': ['']},
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
	Config.set('graphics', 'maxfps', '15')

	App().run()
