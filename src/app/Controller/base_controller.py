from __future__ import annotations

from typing import TYPE_CHECKING

from app.utility.logger import Loggable

if TYPE_CHECKING:
	from typing import Any

	from app.Model.base_model import BaseScreenModel
	from app.View.base_screen import BaseScreenView


class BaseController(Loggable):
	"""The `BaseController` class represents a base class for controllers implementation.

	Coordinates work of the view with the model.
	The controller implements the strategy pattern. The controller connects to
	the view to control its actions.
	"""

	_view: 'BaseScreenView'

	def __init__(self: 'BaseController', model: 'BaseScreenModel') -> None:
		self._check_props()

		self.model: 'BaseScreenModel' = model


	def __post_init__(self: 'BaseController') -> None:
		"""Run after this class and subclass `__init__` constructor method call."""
		self._p_log_prefix: str = f'Controller of View `{self.view._p_log_name}`'  # noqa: SLF001

		super().__post_init__()


	def _check_props(self: 'BaseController') -> None:
		# if someone not added `_view` or other attributes, or calls this class instance directly
		if type(self) != BaseController:
			return

		self._view = self.__prop_view


	def __abc(self: 'BaseController') -> 'Any':
		"""ABC helper."""
		raise NotImplementedError


	@property
	def __prop_view(self: 'BaseController') -> 'BaseScreenView':
		"""Must be in subclass."""
		return self.__abc()


	@property
	def view(self: 'BaseController') -> 'BaseScreenView':
		"""Controller's view."""
		return self._view
