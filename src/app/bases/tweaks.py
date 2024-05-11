from __future__ import annotations

from typing import TYPE_CHECKING

from kivy.core.window import Window
from plyer.utils import platform

from app.bases.abc import AppBaseABCLike

if platform == 'android':
	from android import mActivity

	# TODO: Find or make stubs for java android api used from pyjnius.. or better make mypy plugin..
	from jnius import autoclass

if TYPE_CHECKING:
	# NOTE: Type annotations from typing block are still quoted because
	# cython will raise errors in functions & methods annotations.. (but still ok for vars)
	from typing import Any

	from app.View.base_screen import BaseScreenView


class AppTweaks(AppBaseABCLike):

	def __init__(self: 'AppTweaks', *args: 'Any', **kwargs: 'Any') -> None:
		super().__init__(*args, **kwargs)

		Window.bind(on_keyboard=self.handle_esc_or_back)


	def on_app_init(self: 'AppTweaks', **kwargs: 'Any') -> None:
		self.bind_to(
			{
				'android_set_handle_native_autorotate': 'on_start',
				'set_mobilelike_resolution': 'on_start',
			},
		)


	def android_set_handle_native_autorotate(self: 'AppTweaks') -> None:
		# Set startup orientation because value from manifest is ignored..
		# (depends on the system auto-rotate option)
		if platform != 'android':
			return

		ActivityInfo = autoclass('android.content.pm.ActivityInfo')

		mActivity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_FULL_USER)


	def handle_esc_or_back(
		self: 'AppTweaks', window, key: int,
		scancode, codepoint, modifier,
	) -> bool:
		"""Handle back button press or esc."""
		print(window, key, scancode, codepoint, modifier)
		current_screen: 'BaseScreenView' = self.manager_screens.current_screen
		if key == 27 and current_screen.name != 'main_screen':
			# FIXME: Use `self.manager_screens.screens` instead..
			self.manager_screens.current = current_screen.parent_screen_name
			# key event consumed by app
			return True

		# key event passed to OS
		return False


	def set_mobilelike_resolution(self: 'AppTweaks') -> None:
		"""Set mobile-like resolution for easier tests."""
		if platform == 'android':
			return

		Window.size = (480, 800)
