from __future__ import annotations

from typing import TYPE_CHECKING

from kivy.animation import AnimationTransition
from kivy.graphics import PopMatrix, PushMatrix, Scale
from kivy.metrics import dp
from kivy.properties import BooleanProperty, NumericProperty, OptionProperty
from kivymd.uix.transition.transition import MDTransitionBase

if TYPE_CHECKING:
	from kivymd.uix.screenmanager import MDScreenManager


# Copied from 2.0.1.dev0
class MDSharedAxisTransition(MDTransitionBase):
	"""Android default screen transition.

	.. versionadded:: 2.0.0
	"""

	transition_axis = OptionProperty('x', options=['x', 'y', 'z'])
	"""
	Axis of the transition. Available values "x", "y", and "z".

	.. image:: https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/kivymddoc/transition_axis.gif
		:align: center

	:attr:`transition_axis` is an :class:`~kivy.properties.OptionProperty`
	and defaults to `"x"`.
	"""

	duration = NumericProperty(0.15)
	"""
	Duration in seconds of the transition. Android recommends these intervals:

	.. list-table:: Android transition values (in seconds)
		:align: left
		:header-rows: 1

		* - Name
		  - value
		* - small_1 
		  - 0.075
		* - small_2 
		  - 0.15
		* - medium_1
		  - 0.2
		* - medium_2
		  - 0.25
		* - large_1 
		  - 0.3
		* - large_2
		  - 0.35

	:attr:`duration` is a :class:`~kivy.properties.NumericProperty` and
	defaults to 0.15 (= 150ms).
	"""

	slide_distance = NumericProperty(dp(15))
	"""
	Distance to which it slides left, right, bottom or up depending on axis.

	:attr:`slide_distance` is a :class:`~kivy.properties.NumericProperty` and
	defaults to `dp(15)`.
	"""

	opposite = BooleanProperty(defaultvalue=False)
	"""
	Decides Transition direction.

	:attr:`opposite` is a :class:`~kivy.properties.BooleanProperty` and
	defaults to `False`.
	"""

	_s_map: dict[int, Scale] = {}  # scale instruction map
	_slide_diff = 0

	def start(self: 'MDSharedAxisTransition', manager: 'MDScreenManager') -> None:
		# Transition internal working (for developer only):
		# x:
		#    First half: screen_out opacity 1 ->  0, pos_x: 0 -> - slide distance
		#    Second half: screen_in opacity 0 -> 1, pos_x: slide distance -> 0
		# y:
		#    First half: screen_out opacity 1 ->  0, pos_y: 0 -> - slide distance
		#    Second half: screen_in opacity 0 -> 1, pos_y: slide distance -> 0
		# z:
		#   First half: screen_out opacity 1 -> 0, scale: 1 -> relative subtracted area
		#   Second half: screen_in opacity 0 -> 1, scale: relative subtracted area -> 1

		# Save hash of the objects
		self.ih = hash(self.screen_in)
		self.oh = hash(self.screen_out)

		if self.transition_axis == 'z':
			if self.ih not in self._s_map:
				# Save scale instructions.
				with self.screen_in.canvas.before:
					PushMatrix()
					self._s_map[self.ih] = Scale()
				with self.screen_in.canvas.after:
					PopMatrix()
				with self.screen_out.canvas.before:
					PushMatrix()
					self._s_map[self.oh] = Scale()
				with self.screen_out.canvas.after:
					PopMatrix()

			self._s_map[self.oh].origin = [
				(manager.pos[0] + manager.width) / 2,
				(manager.pos[1] + manager.height) / 2,
			]
			self._s_map[self.ih].origin = self._s_map[self.oh].origin
			# Relative subtracted area.
			self._slide_diff = (manager.width - self.slide_distance) * (
				manager.height - self.slide_distance
			) / (manager.width * manager.height) - 1
		elif self.transition_axis in ['x', 'y']:
			# Slide distance with opposite logic.
			self._slide_diff = (
				(1 if self.opposite else -1) * self.slide_distance * 2
			)

		super().start(manager)

	def on_progress(self: 'MDSharedAxisTransition', progress: 'float | int') -> None:
		# This code could be simplyfied with setattr, but it's slow.
		progress = AnimationTransition.out_cubic(progress)
		progress_i = progress - 1
		progress_d = progress * 2
		# First half.
		if progress <= 0.5:
			# Screen out animation.
			if self.transition_axis == 'z':
				self._s_map[self.oh].xyz = (
					*[1 + self._slide_diff * progress_d] * 2,
					1,
				)
			elif self.transition_axis == 'x':
				self.screen_out.pos = [
					self.manager.pos[0] + self._slide_diff * progress,
					self.manager.pos[1],
				]
			else:
				self.screen_out.pos = [
					self.manager.pos[0],
					self.manager.pos[1] - self._slide_diff * progress,
				]
			self.screen_out.opacity = 1 - progress_d
			self.screen_in.opacity = 0

			return

		# Second half.
		if self.transition_axis == 'z':
			self._s_map[self.ih].xyz = (
				*[1 - self._slide_diff * progress_i * 2] * 2,
				1,
			)
		elif self.transition_axis == 'x':
			self.screen_in.pos = [
				self.manager.pos[0] + self._slide_diff * progress_i,
				self.manager.pos[1],
			]
		else:
			self.screen_in.pos = [
				self.manager.pos[0],
				self.manager.pos[1] - self._slide_diff * progress_i,
			]
		self.screen_in.opacity = progress_d - 1
		self.screen_out.opacity = 0

	def on_complete(self: 'MDSharedAxisTransition') -> None:
		self.screen_in.pos = self.manager.pos
		self.screen_out.pos = self.manager.pos
		if self.oh in self._s_map:
			self._s_map[self.oh].xyz = (1, 1, 1)

		if self.ih in self._s_map:
			self._s_map[self.ih].xyz = (1, 1, 1)

		super().on_complete()
