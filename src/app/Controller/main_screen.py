from __future__ import annotations

from typing import TYPE_CHECKING

from app.Controller.base_controller import BaseController
from app.View.main_screen import MainScreenView

if TYPE_CHECKING:
	from typing import Any

	from kivymd.uix.anchorlayout import MDAnchorLayout
	from kivymd.uix.selectioncontrol import MDCheckbox

	from app.Model.main_screen import MainScreenModel


class MainScreenController(BaseController):
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


	def selection_on_read_active(
		self: 'MainScreenController',
		checkbox: 'MDCheckbox', value: bool,
	) -> None:
		# TODO: Add attrs to model
		layout: 'MDAnchorLayout' = self.view.ids.layout_write_txtfield

		if checkbox.group != 'select_rw':
			self.log.warning(
				'Widget SM: Callback was called by incorrect widget `%s`, '
				'must be `SelectMode`.{read,write}_checkbox',
				checkbox,
			)

		if value:
			# Clear layout widgets
			layout.clear_widgets()
		else:
			# Back add widget to layout
			if layout.children:
				self.log.warning(
					'Widget SM: Widget `%s` has children: `%s` '
					'(this mean checkbox was activated twice for some reasons..)',
					layout,
					layout.children,
				)
				return
			layout.add_widget(self.view.write_txtfield)
