from __future__ import annotations

from kivymd.toast import toast

# if platform == 'android':
# 	from android import mActivity
from .base_model import BaseScreenModel


class MainScreenModel(BaseScreenModel):
	"""Implements the logic of the MainScreenView class."""

	# TODO: Better use setter-getter & write.. && mb fully wrap usually conf)
	@property
	def docs_path(self: 'MainScreenModel') -> str:
		return self.config.get('app', 'docs_path')


	@docs_path.setter
	def docs_path(self: 'MainScreenModel', uri: str) -> None:
		self.config.set('app', 'docs_path', uri)
		self.config.write()

		toast('Docs path set!')


	def save_settings(self: 'MainScreenModel', btn) -> None:
		...
