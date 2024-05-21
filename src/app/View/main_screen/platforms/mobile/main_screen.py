from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

from app.View.base_screen import BaseScreenView
from app.View.widgets.textinput import MDTextInput
from kivy.factory import Factory

if TYPE_CHECKING:
	from app.Controller.main_screen import MainScreenController
	from app.Model.main_screen import MainScreenModel
	from kivymd.uix.boxlayout import MDBoxLayout
	from kivymd.uix.scrollview import MDScrollView


# TODO: Full screen mode & hide status bar & more comfartable read functions..


class MainScreenView(BaseScreenView):

	controller: 'MainScreenController'
	model: 'MainScreenModel'


	def __post_init__(self: 'MainScreenView') -> None:
		"""Stuff after init."""
		# Logger's post-init
		super().__post_init__()

		self._read_items: 'MDBoxLayout' = Factory.DynamicWidgetItems()
		self._read_items.make_widget = Factory.EditItem

		# FIXME: Cursor goes over (outside) widget.. (if no scroll layout)
		# TODO: Make special metaclass for this stuff.. (properties)
		# to get object by usually ref
		self._write_txtin: MDTextInput = MDTextInput(
			size_hint_y=None,
			radius=(0, 0, 0, 0),
		)

		# FIXME: Move into the method..

		rwc: 'MDScrollView' = self.ids.layout_rw_container
		# initial size before scroll is 100, that's because we just add 33%
		rwc.height = int(rwc.height + ((rwc.height / 100) * 33))
		self._write_txtin.bind(minimum_height=partial(self._update_height, rwc))
		del rwc

		# TODO: How to declaratively unbind already bind property in imperative kv code?
		# self._write_txtin.unbind(size_hint_y=self._write_txtin.setter('size_hint_y'))

		# TODO: Find ways to load widgets to factory before some other stuff..

		# ?? ..
		# print(tf.uid)
		# Builder.unbind_widget(tf.uid)


	def startup(self: 'MainScreenView') -> None:
		# self.manager_screens.current = 'settings_screen'
		# from app.View.widgets.about_dialog import AboutDialog
		# AboutDialog().open()

		# self.ids.rw_checkboxes.ids.write.chbx_do_press()

		...


	# TODO: Use kivy properties here..?


	@property
	def read_items(self: 'MainScreenView') -> 'MDBoxLayout':  # -> <base on>
		return self._read_items


	@property
	def write_txtin(self: 'MainScreenView') -> MDTextInput:
		return self._write_txtin


	def _update_height(
		self: 'MainScreenView',
		sv: 'MDScrollView', widget: MDTextInput, height: int,
	) -> None:
		widget.height = max(sv.height, height)


	def model_is_changed(self: 'MainScreenView') -> None:
		"""Call whenever any change has occurred in the data model.

		The view in this method tracks these changes and updates the UI
		according to these changes.
		"""
