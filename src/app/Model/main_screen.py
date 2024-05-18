from __future__ import annotations

from typing import TYPE_CHECKING

# from plyer.utils import platform
# if platform == 'android':
# 	from android import mActivity
from .base_model import BaseScreenModel

if TYPE_CHECKING:
	...


class MainScreenModel(BaseScreenModel):
	"""Implements the logic of the MainScreenView class."""
