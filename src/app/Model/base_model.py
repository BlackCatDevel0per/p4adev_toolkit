# The model implements the observer pattern. This means that the class must
# support adding, removing, and alerting observers. In this case, the model is
# completely independent of controllers and views. It is important that all
# registered observers implement a specific method that will be called by the
# model when they are notified (in this case, it is the `model_is_changed`
# method). For this, observers must be descendants of an abstract class,
# inheriting which, the `model_is_changed` method must be overridden.

from __future__ import annotations

from typing import TYPE_CHECKING

# from kivy.event import EventDispatcher
from kivymd.app import MDApp

from app.utility.logger import Loggable

if TYPE_CHECKING:
	from typing import Any, ClassVar

	from kivy.config import ConfigParser

	from app.View.base_view import AnyScreenModel, AnyScreenView, BaseScreenView


class BaseScreenModel(Loggable):
	"""Implements a base class for model modules."""

	_p_log_prefix: str = 'Model'

	_observers: 'ClassVar[list[BaseScreenView]]' = []


	def __init__(self: 'BaseScreenModel', *args: 'Any', **kwargs: 'Any') -> None:
		super().__init__(*args, **kwargs)

		self.config: 'ConfigParser' = MDApp.get_running_app().config


	def startup(self: 'BaseScreenModel') -> None:
		raise NotImplementedError


	def add_observer(self: 'BaseScreenModel', observer: 'AnyScreenView') -> None:
		self._observers.append(observer)


	def remove_observer(self: 'BaseScreenModel', observer: 'AnyScreenView') -> None:
		self._observers.remove(observer)


	def model_is_changed(self: 'BaseScreenModel') -> None:
		raise NotImplementedError


	def _find_oberver(self: 'BaseScreenModel', name_screen: str) -> 'AnyScreenView':
		for observer in self._observers:
			if observer.name == name_screen:
				return observer

		raise NameError


	# TODO: Cache..
	def find_model(self: 'BaseScreenModel', name_screen: str) -> 'AnyScreenModel':
		return self._find_oberver(name_screen).model


	def notify_observers(self: 'BaseScreenModel', name_screen: str) -> None:
		"""Call by the observer when the model data change.

		:param name_screen:
			name of the view for which the method should be called
			:meth:`model_is_changed`.
		"""
		observer: 'BaseScreenView' = self._find_oberver(name_screen)
		observer.model_is_changed()
