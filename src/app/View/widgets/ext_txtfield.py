from __future__ import annotations

from typing import TYPE_CHECKING

from kivy.properties import ObjectProperty
from kivymd.uix.textfield import MDTextField

if TYPE_CHECKING:
	from collections.abc import Callable


class MDExtendedTextField(MDTextField):

	validator: 'Callable[str, [bool]]' = ObjectProperty()


	def _get_has_error(self: 'MDExtendedTextField') -> bool:
		"""Return `False` or `True` depending on the state of the text field.

		For example when the allowed character limit has been exceeded or when
		the :attr:`~MDTextField.required` parameter is set to `True`.
		"""
		# TODO: Check it one on init & make some kind of debounced antiflood..
		if self.validator and self.validator != "phone":
			if isinstance(self.validator, str):
				return {
					"date": self.is_date_valid,
					"email": self.is_email_valid,
					"time": self.is_time_valid,
				}[self.validator](self.text)

			return self.validator(self.text)

		if self.max_text_length and len(self.text) > self.max_text_length \
			or all((self.required, len(self.text) == 0)):
				has_error = True
		else:
			has_error = False

		return has_error
