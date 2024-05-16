from __future__ import annotations

from typing import TYPE_CHECKING

# from kivy.metrics import dp
# from plyer.utils import platform
# if platform == 'android':
# 	from android import mActivity
from .base_model import BaseScreenModel

if TYPE_CHECKING:
	from kivy.uix.textfield import MDTextField


class MainScreenModel(BaseScreenModel):
	"""Implements the logic of the MainScreenView class."""

	# TODO: Make special metaclass for this stuff..
	@property
	def write_txtfield(self: 'MainScreenModel') -> 'MDTextField':
		return self._write_txtfield

	@write_txtfield.setter
	def write_txtfield(self: 'MainScreenModel', value: 'MDTextField') -> None:
		self._write_txtfield = value
