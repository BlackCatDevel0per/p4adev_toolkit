import os

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import OptionProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors, palette
from kivymd.uix.behaviors import (
	CircularRippleBehavior,
	CommonElevationBehavior,
	SpecificBackgroundColorBehavior,
)
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import BaseDialog

Factory.register('MDTabsBase', module='kivymd.uix.tab')

with open(
	os.path.join(os.path.dirname(__file__), 'themepicker.kv'),
	encoding='utf-8',
) as kv_file:
	Builder.load_string(kv_file.read())


class RoundButton(CircularRippleBehavior, ButtonBehavior, AnchorLayout):
	pass


class ColorSelector(MDIconButton):
	color_name = OptionProperty('Indigo', options=palette)

	def rgb_hex(self, col):
		return get_color_from_hex(colors[col][self.theme_cls.accent_hue])


class MDThemePicker(
	BaseDialog,
	CommonElevationBehavior,
	SpecificBackgroundColorBehavior,
):
	def on_open(self):
		super().on_open()

		self.on_tab_switch(None, self.ids.theme_tab, None, None)

	def on_tab_switch(
		self, ins_tabs, ins_tab, ins_tab_label, tab_text
	):
		if ins_tab.text == 'Theme':
			if self.ids.primary_box.children:
				return

			for name_palette in palette:
				self.ids.primary_box.add_widget(
					Factory.PrimaryColorSelector(color_name=name_palette)
				)

		elif ins_tab.text == 'Accent':
			if self.ids.accent_box.children:
				return

			for name_palette in palette:
				self.ids.accent_box.add_widget(
					Factory.AccentColorSelector(color_name=name_palette)
				)

