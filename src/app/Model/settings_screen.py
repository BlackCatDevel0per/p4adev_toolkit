from __future__ import annotations

from kivy.metrics import dp
from plyer.utils import platform

# if platform == 'android':
# 	from android import mActivity
from .base_model import BaseScreenModel


class MainScreenModel(BaseScreenModel):
	"""Implements the logic of the MainScreenView class."""
