from __future__ import annotations

from typing import TYPE_CHECKING

from app.Controller.base_controller import BaseController
from app.View.settings_screen import MainScreenView

if TYPE_CHECKING:
	from typing import Any


class MainScreenController(BaseController):
	"""The `MainScreenController` class represents a controller implementation.

	Coordinates work of the view with the model.
	The controller implements the strategy pattern. The controller connects to
	the view to control its actions.
	"""

	def __init__(self: 'MainScreenController', *args: 'Any', **kwargs: 'Any') -> None:
		super().__init__(*args, **kwargs)

		self._view = MainScreenView(controller=self, model=self.model)
