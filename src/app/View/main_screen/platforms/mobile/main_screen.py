from __future__ import annotations

from typing import TYPE_CHECKING

from app.View.base_screen import BaseScreenView

if TYPE_CHECKING:
	...


# TODO: Full screen mode & hide status bar & more comfartable read functions..


class MainScreenView(BaseScreenView):

	def startup(self: 'MainScreenView') -> None:
		# self.manager_screens.current = 'settings_screen'
		...


	def model_is_changed(self: 'MainScreenView') -> None:
		"""Call whenever any change has occurred in the data model.

		The view in this method tracks these changes and updates the UI
		according to these changes.
		"""
