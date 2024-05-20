from __future__ import annotations

from typing import TYPE_CHECKING

from kivymd2_widgets.pickers import MDThemePicker

from app.bases.abc import AppBaseABCLike

if TYPE_CHECKING:
	from typing import Any


class AppStyle(AppBaseABCLike):

	def on_app_init(self: 'AppStyle', **kwargs: 'Any') -> None:
		self.bind_to({'set_accent_style': 'on_build'})


	def set_accent_style(self: 'AppStyle') -> None:
		self.theme_cls.theme_style_switch_animation = True

		self.theme_cls.primary_palette = self.config.get('theme', 'palette')
		self.theme_cls.accent_palette = self.config.get('theme', 'accent')
		self.theme_cls.theme_style = self.config.get('theme', 'style')

		self.config.write()


	def save_accent_style(self: 'AppStyle') -> None:
		self.config.set('theme', 'palette', self.theme_cls.primary_palette)
		self.config.set('theme', 'accent', self.theme_cls.accent_palette)
		self.config.set('theme', 'style', self.theme_cls.theme_style)

		self.config.write()


	def switch_accent_style(self: 'AppStyle') -> None:
		if not hasattr(self, 'theme_picker'):
			# TODO: Remove on screen change to save memory..
			# & with some singleton widgets do the same..
			self.theme_picker = MDThemePicker()
			self.theme_picker.on_dismiss = self.save_accent_style

		self.theme_picker.open()
