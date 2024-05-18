from __future__ import annotations

from kivymd.toast import toast
from plyer.utils import platform
from PyScopedStorage.filechooser import filechooser

from app.utility.utils import StrCall

# if platform == 'android':
# 	from android import mActivity
from .base_model import BaseScreenModel


class MainScreenModel(BaseScreenModel):
	"""Implements the logic of the MainScreenView class."""


	# TODO: Better use setter-getter & write.. && mb fully wrap usually conf)
	@property
	def docs_path_conf(self: 'MainScreenModel') -> str:
		return self.config.get('app', 'docs_path')


	@docs_path_conf.setter
	def docs_path_conf(self: 'MainScreenModel', uri: str) -> None:
		self.config.set('app', 'docs_path', uri)
		self.config.write()

		toast('Docs path set!')


	def set_docs_path_callback(self: 'MainScreenModel', sel: 'list[android.net.Uri]') -> None:
		if not sel:
			return

		uri_or_path: 'android.net.Uri | str' = sel[0]

		if platform != 'android':
			self.log.debug('Access path: `%s`', uri_or_path)
			assert isinstance(uri_or_path, str)  # linter plug
			self.docs_path_conf = uri_or_path  # TODO: Solve normally -_-
			self.notify_observers('settings_screen')
			return

		self.log.debug('Access SS Uri: %s', StrCall(uri_or_path.toString))

		uri_full_path: str = uri_or_path.toString()

		self.docs_path_conf = uri_full_path
		self.notify_observers('settings_screen')


	def set_docs_path(self: 'MainScreenModel') -> None:
		filechooser.choose_dir(
			# on_selection=lambda s: self.log.warning(f'result: {s}'),
			on_selection=self.set_docs_path_callback,
		)


	def save_settings(self: 'MainScreenModel', btn) -> None:
		...
