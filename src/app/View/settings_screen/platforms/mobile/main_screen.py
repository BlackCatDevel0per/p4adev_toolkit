from __future__ import annotations

from typing import TYPE_CHECKING

from app.View.base_screen import BaseScreenView

if TYPE_CHECKING:
	...


# TODO: Full screen mode & hide status bar..


class SettingsScreenView(BaseScreenView):

	def startup(self: 'SettingsScreenView') -> None:
		...


	def model_is_changed(self: 'SettingsScreenView') -> None:
		"""Call whenever any change has occurred in the data model.

		The view in this method tracks these changes and updates the UI
		according to these changes.
		"""
		# Update label of `set_docs` action
		self.ids.main_bl_startup_tools_set_docs_path_tool.\
			label_text = self.app.config.get('app', 'docs_path')


MainScreenView = SettingsScreenView
