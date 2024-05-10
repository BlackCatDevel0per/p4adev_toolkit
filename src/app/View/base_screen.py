from __future__ import annotations

from typing import TYPE_CHECKING

from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from app.utility.logger import Loggable
from app.utility.observer import Observer
from app.utility.utils import UniteMetas

if TYPE_CHECKING:
	from typing import Any


class BaseScreenView(MDScreen, Observer, Loggable, metaclass=UniteMetas(MDScreen, Loggable)):
	"""A base class that implements a visual representation of the model data.

	The view class must be inherited from this class.
	"""

	controller = ObjectProperty()
	"""
	controller object - :class:`~controller.controller_screen.ClassScreenControler`.

	:attr:`controller` is an :class:`~kivy.properties.ObjectProperty`
	and defaults to `None`.
	"""

	model = ObjectProperty()
	"""
	model object - :class:`~model.model_screen.ClassScreenModel`.

	:attr:`model` is an :class:`~kivy.properties.ObjectProperty`
	and defaults to `None`.
	"""

	manager_screens = ObjectProperty()
	"""
	Screen manager object - :class:`~kivymd.uix.screenmanager.MDScreenManager`.

	:attr:`manager_screens` is an :class:`~kivy.properties.ObjectProperty`
	and defaults to `None`.
	"""

	parent_screen = StringProperty('main_screen')

	def __init__(self: 'BaseScreenView', **kw: 'Any') -> None:
		super().__init__(**kw)
		# Often you need to get access to the application object from the view
		# class. You can do this using this attribute.
		self.app = MDApp.get_running_app()
		# Adding a view class as observer.
		self.model.add_observer(self)


	def __post_init__(self: 'BaseScreenView') -> None:
		"""Run after this class and subclass `__init__` constructor method call."""
		self._p_log_prefix: str = f'View of Model `{self.model._p_log_name}`'  # noqa: SLF001

		super().__post_init__()


	def startup(self) -> None:
		"""Startup screen view actions (example: dynamic menu & etc.)."""
