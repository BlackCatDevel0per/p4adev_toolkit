from __future__ import annotations

from typing import TYPE_CHECKING

from app.View.base_screen import BaseScreenView

if TYPE_CHECKING:
	from app.Controller.main_screen import MainScreenController
	from app.Model.main_screen import MainScreenModel


# TODO: Full screen mode & hide status bar & more comfartable read functions..


class MainScreenView(BaseScreenView):

	controller: 'MainScreenController'
	model: 'MainScreenModel'

	def startup(self: 'MainScreenView') -> None:
		# self.manager_screens.current = 'settings_screen'
		# from app.View.widgets.about_dialog import AboutDialog
		# AboutDialog().open()
		...


	def model_is_changed(self: 'MainScreenView') -> None:
		"""Call whenever any change has occurred in the data model.

		The view in this method tracks these changes and updates the UI
		according to these changes.
		"""
