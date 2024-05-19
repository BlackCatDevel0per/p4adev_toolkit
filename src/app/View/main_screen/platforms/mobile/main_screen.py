from __future__ import annotations

from typing import TYPE_CHECKING

from app.View.base_screen import BaseScreenView
from app.View.widgets.textinput import MDTextInput
from kivy.factory import Factory

if TYPE_CHECKING:
	from app.Controller.main_screen import MainScreenController
	from app.Model.main_screen import MainScreenModel


# TODO: Full screen mode & hide status bar & more comfartable read functions..


class MainScreenView(BaseScreenView):

	controller: 'MainScreenController'
	model: 'MainScreenModel'


	def __post_init__(self: 'MainScreenView') -> None:
		"""Stuff after init."""
		# Logger's post-init
		super().__post_init__()

		# TODO: Widget with List of dynamic Buttons
		self._read_items = Factory.HighlightedBorderWidget()

		# ?? ..
		# print(tf.uid)
		# Builder.unbind_widget(tf.uid)

		# FIXME: Cursor goes over widget.. (if no scroll layout)
		# TODO: Make special metaclass for this stuff.. (properties)
		# to get object by usually ref
		self._write_txtfield = MDTextInput(
			size_hint_y=None,
		)


	def startup(self: 'MainScreenView') -> None:
		# self.manager_screens.current = 'settings_screen'
		# from app.View.widgets.about_dialog import AboutDialog
		# AboutDialog().open()

		# self.ids.rw_checkboxes.ids.write.chbx_do_press()

		...


	@property
	def read_items(self: 'MainScreenView') -> '':
		return self._read_items


	@property
	def write_txtfield(self: 'MainScreenView') -> 'MDTextInput':
		return self._write_txtfield


	def model_is_changed(self: 'MainScreenView') -> None:
		"""Call whenever any change has occurred in the data model.

		The view in this method tracks these changes and updates the UI
		according to these changes.
		"""
