from __future__ import annotations

from typing import TYPE_CHECKING

# from plyer.utils import platform
# if platform == 'android':
# 	from android import mActivity
from .base_model import BaseScreenModel

if TYPE_CHECKING:
	from .settings_screen import MainScreenModel as SettingsScreenModel


class MainScreenModel(BaseScreenModel):
	"""Implements the logic of the MainScreenView class."""

	@property
	def docs_path(self: 'MainScreenModel') -> str:
		# TODO: Use literals for linter..
		stngs_m: 'SettingsScreenModel' = self.find_model('settings_screen')
		return stngs_m.docs_path

	@docs_path.setter
	def docs_path(self: 'MainScreenModel', value: str) -> None:
		stngs_m: 'SettingsScreenModel' = self.find_model('settings_screen')
		stngs_m.docs_path = value
