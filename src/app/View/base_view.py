from __future__ import annotations

from typing import TYPE_CHECKING

from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from app.utility.logger import Loggable
from app.utility.observer import Observer
from app.utility.utils import UniteMetas

if TYPE_CHECKING:
	from typing import Any, TypeVar

	from app.Controller.base_controller import BaseScreenController
	from app.entry.launch import App
	from app.Model.base_model import BaseScreenModel
	from app.View.screenmanager import AppScreenManager

	# Screen..
	AnyScreenModel = TypeVar('AnyScreenModel', bound=BaseScreenModel)
	AnyScreenView = TypeVar('AnyScreenView', bound='BaseScreenView')
	AnyScreenController = TypeVar('AnyScreenController', bound=BaseScreenController)


class BaseScreenView(MDScreen, Observer, Loggable, metaclass=UniteMetas(MDScreen, Loggable)):
	"""A base class that implements a visual representation of the model data.

	The view class must be inherited from this class.
	"""

	# TODO: Better annotate kivy properties..
	controller: 'BaseScreenController' = ObjectProperty()
	"""
	controller object - :class:`~controller.controller_screen.ClassScreenControler`.

	:attr:`controller` is an :class:`~kivy.properties.ObjectProperty`
	and defaults to `None`.
	"""

	model: 'BaseScreenModel' = ObjectProperty()
	"""
	model object - :class:`~model.model_screen.ClassScreenModel`.

	:attr:`model` is an :class:`~kivy.properties.ObjectProperty`
	and defaults to `None`.
	"""

	manager_screens: 'AppScreenManager' = ObjectProperty()
	"""
	Screen manager object - base on :class:`~kivymd.uix.screenmanager.MDScreenManager`.

	:attr:`manager_screens` is an :class:`~kivy.properties.ObjectProperty`
	and defaults to `None`.
	"""

	parent_screen_name: str = StringProperty('main_screen')

	def __init__(self: 'AnyScreenView', **kw: 'Any') -> None:
		super().__init__(**kw)
		# Often you need to get access to the application object from the view
		# class. You can do this using this attribute.
		self.app: 'App' = MDApp.get_running_app()
		# Adding a view class as observer.
		self.model.add_observer(self)


	def __post_init__(self: 'BaseScreenView') -> None:
		"""Run after this class and subclass `__init__` constructor method call."""
		self._p_log_prefix: str = f'View of Model `{self.model._p_log_name}`'  # noqa: SLF001

		super().__post_init__()


	def startup(self: 'BaseScreenView') -> None:
		"""Startup screen view actions (example: dynamic menu & etc.)."""
