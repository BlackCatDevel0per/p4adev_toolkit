from __future__ import annotations

from typing import TYPE_CHECKING

from p4a_dev.view.main_screen.main_screen import MainScreenView

if TYPE_CHECKING:
	from p4a_dev.model.main_screen import MainScreenModel


class MainScreenController:
	"""The `MainScreenController` class represents a controller implementation.

	Coordinates work of the view with the model.
	The controller implements the strategy pattern. The controller connects to
	the view to control its actions.
	"""

	def __init__(self: 'MainScreenController', model: 'MainScreenModel') -> None:
		self.model: 'MainScreenModel' = model
		self._view = MainScreenView(controller=self, model=self.model)

	@property
	def view(self: 'MainScreenController') -> MainScreenView:
		return self._view
