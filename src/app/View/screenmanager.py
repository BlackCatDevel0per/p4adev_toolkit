from typing import TYPE_CHECKING

from kivymd.uix.screenmanager import MDScreenManager

if TYPE_CHECKING:
	from kivymd.uix.transition.transition import MDTransitionBase


class AppScreenManager(MDScreenManager):

	transition: 'MDTransitionBase'

	def check_transition(self: 'AppScreenManager', *args) -> None:
		"""Set the default type transition."""
		from kivymd.uix.transition.transition import MDTransitionBase

		if issubclass(self.transition.__class__, MDTransitionBase):
			return

		# TODO: Use `MDSharedAxisTransition`
		from app.View.widgets.transition import MDSharedAxisTransition

		self.transition = MDSharedAxisTransition(
			duration=0.65,
			transition_axis='y',
		)
