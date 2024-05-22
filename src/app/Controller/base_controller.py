from __future__ import annotations

from typing import TYPE_CHECKING

from app.utility.logger import Loggable

if TYPE_CHECKING:
	from typing import Any

	from app.Model.base_screen import BaseScreenModel
	from app.View.base_view import AnyController, AnyModel, BaseScreenView


class BaseScreenController(Loggable):
	"""The `BaseScreenController` class represents a base class for controllers implementation.

	Coordinates work of the view with the model.
	The controller implements the strategy pattern. The controller connects to
	the view to control its actions.
	"""

	_view: 'BaseScreenView'

	def __init__(self: 'BaseScreenController', model: 'AnyModel') -> None:
		self._check_props()

		self.model: 'BaseScreenModel' = model


	def __post_init__(self: 'BaseScreenController') -> None:
		"""Run after this class and subclass `__init__` constructor method call."""
		self._p_log_prefix: str = f'Controller of View `{self.view._p_log_name}`'  # noqa: SLF001

		super().__post_init__()


	def _find_controller(self: 'AnyController', name_screen: str) -> 'AnyController':
		return self.model._find_oberver(name_screen).controller  # noqa: SLF001


	def _check_props(self: 'BaseScreenController') -> None:
		# if someone not added `_view` or other attributes, or calls this class instance directly
		if type(self) != BaseScreenController:
			return

		self._view = self.__prop_view


	def __abc(self: 'BaseScreenController') -> 'Any':
		"""ABC helper."""
		raise NotImplementedError


	@property
	def __prop_view(self: 'BaseScreenController') -> 'BaseScreenView':
		"""Must be in subclass."""
		return self.__abc()


	@property
	def view(self: 'BaseScreenController') -> 'BaseScreenView':
		"""Controller's view."""
		return self._view
