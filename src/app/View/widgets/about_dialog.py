from typing import TYPE_CHECKING

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDIcon

from app.utility.logger import Loggable
from app.utility.utils import UniteMetas
from app.View.widgets.single_ins import SingleInstance

if TYPE_CHECKING:
	from typing import Any

	from kivymd.uix.card import MDCard
	from kivymd.uix.label import MDLabel


class AboutDialog(SingleInstance, Loggable, MDDialog, metaclass=UniteMetas(Loggable, MDDialog)):

	title = 'Info'
	markup = True
	text = (
		'Template from:'
		' '
		'[u][ref=https://github.com/BlackCatDevel0per/p4adev_toolkit]p4adev_toolkit[/ref][/u]'
	)

	icon = 'information-slab-circle'

	_p_log_prefix = 'Widget'

	def __init__(self: 'AboutDialog', *args: 'Any', **kwargs: 'Any') -> None:
		# TODO: Check if theme changes correctly..
		if 'buttons' not in kwargs:
			kwargs['buttons'] = [
				MDFlatButton(
					text='OK',
					# FIXME: Dismiss softer.. (after press animation)
					on_press=lambda btn: self.dismiss(),
				),
			]

		super().__init__(*args, **kwargs)

		label_text: 'MDLabel' = self.ids.text

		label_text.markup = self.markup

		if 'on_text_ref_press' in kwargs:
			label_text.on_ref_press = kwargs.pop('on_text_ref_press')
		else:
			label_text.on_ref_press = self.on_text_ref_press


		# TODO: Better handle errors with widgets dicts..
		dcont: 'MDCard' = self.ids.container
		label_title: 'MDLabel' = self.ids.title

		dcont.remove_widget(label_title)

		label_title_with_icon: 'MDBoxLayout' = MDBoxLayout(
			# ??
			# height=label_title.height,
			# size_hint_y=label_title.size_hint_y,
		)

		spacer_box: 'MDBoxLayout' = MDBoxLayout(
			size_hint_y=None,
			size_hint_x=0.03,
			height=MDBoxLayout.minimum_height.defaultvalue,  # self.minimum_height in kv
		)

		# Add icon before title label with spacer at the end
		# TODO: Mb better make it as self setter-properties to easier update ui..
		icon = MDIcon(
			icon=self.icon,
		)

		label_title_with_icon.add_widget(icon)
		label_title_with_icon.add_widget(spacer_box)
		label_title_with_icon.add_widget(label_title)

		# New spacer between future title and existent text
		dcont.add_widget(
			MDBoxLayout(
				# size_hint_y=3,
			),
			index=-1,
		)

		# On old label_title pos
		dcont.add_widget(label_title_with_icon, index=-1)


	def on_text_ref_press(self: 'AboutDialog', ref: str) -> None:
		self.log.info('Press ref: %s', ref)
