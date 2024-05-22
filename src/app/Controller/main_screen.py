from __future__ import annotations

from typing import TYPE_CHECKING

from kivymd.toast import toast

from app.Controller.base_controller import BaseScreenController
from app.View.main_screen import MainScreenView

if TYPE_CHECKING:
	from typing import Any

	from kivy.uix.layout import Layout
	from kivy.uix.widget import Widget
	from kivymd.uix.anchorlayout import MDAnchorLayout
	from kivymd.uix.selectioncontrol import MDCheckbox

	from app.Controller.settings_screen import MainScreenController as SettingsScreenController
	from app.Model.main_screen import MainScreenModel


class MainScreenController(BaseScreenController):
	"""The `MainScreenController` class represents a controller implementation.

	Coordinates work of the view with the model.
	The controller implements the strategy pattern. The controller connects to
	the view to control its actions.
	"""

	view: 'MainScreenView'
	model: 'MainScreenModel'


	def __init__(self: 'MainScreenController', *args: 'Any', **kwargs: 'Any') -> None:
		super().__init__(*args, **kwargs)
		# TODO: Set view automatically too..
		self._view = MainScreenView(controller=self, model=self.model)


	def __post_init__(self: 'MainScreenController') -> None:
		super().__post_init__()

		read_selection: 'MDCheckbox' = self.view.ids.rw_checkboxes.\
			read_selection.ids.selection_checkbox
		self.selection_on_read_active(read_selection, read_selection.active)


	def layout_set_widget_on_chbx(
		self: 'MainScreenController',
		layout: 'Layout',
		widget: 'Widget',
		checkbox: 'MDCheckbox', chbx_group: str, *, value: bool,
	) -> None:
		if checkbox.group != chbx_group:
			self.log.warning(
				'Widget SM: Callback was called by incorrect widget `%s`, '
				'must be `SelectMode`.{read,write}_checkbox',
				checkbox,
			)

		if value:
			# Back add widget to layout
			if layout.children:
				self.log.warning(
					'Widget SM: Widget `%s` has children: `%s` '
					'(this mean checkbox was activated twice for some reasons..)',
					layout,
					layout.children,
				)
				return
			layout.add_widget(widget)
		# NOTE: If you have more than 2 checkboxes, please avoid multiple clear calls
		else:
			# Clear layout widgets
			layout.clear_widgets()


	def rw_layout_set_widget_on_chbx(
		self: 'MainScreenController',
		widget: 'Widget',
		checkbox: 'MDCheckbox', value: bool,
	) -> None:
		layout: 'MDAnchorLayout' = self.view.ids.layout_rw_container
		self.layout_set_widget_on_chbx(
			layout, widget,
			checkbox, chbx_group='select_rw', value=value,
		)


	def selection_on_read_active(
		self: 'MainScreenController',
		checkbox: 'MDCheckbox', value: bool,
	) -> None:
		self.rw_layout_set_widget_on_chbx(self.view.read_items, checkbox, value)


	def selection_on_write_active(
		self: 'MainScreenController',
		checkbox: 'MDCheckbox', value: bool,
	) -> None:
		self.rw_layout_set_widget_on_chbx(self.view.write_txtin, checkbox, value)


	def action_execute(self: 'MainScreenController') -> None:
		if not self.model.docs_path:
			# FIXME: It's sync..
			toast('Please first set docs path!')
			stngs_c: 'SettingsScreenController' = self._find_controller('settings_screen')
			stngs_c.set_docs_path()
			return

		# TODO..
		print(self.model.docs_path)

		for edit_item in self.view.read_items:
			print(edit_item, edit_item.text, edit_item.active)
