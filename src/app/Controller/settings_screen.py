from __future__ import annotations

from typing import TYPE_CHECKING

from plyer.utils import platform
from PyScopedStorage.filechooser import filechooser

from app.Controller.base_controller import BaseScreenController
from app.utility.utils import StrCall
from app.View.settings_screen import MainScreenView

if TYPE_CHECKING:
	from typing import Any


class MainScreenController(BaseScreenController):
	"""The `MainScreenController` class represents a controller implementation.

	Coordinates work of the view with the model.
	The controller implements the strategy pattern. The controller connects to
	the view to control its actions.
	"""

	def __init__(self: 'MainScreenController', *args: 'Any', **kwargs: 'Any') -> None:
		super().__init__(*args, **kwargs)

		self._view = MainScreenView(controller=self, model=self.model)


	def _validate_app_client_id(self: 'MainScreenController', text: str) -> bool:
		return not text.isnumeric()


	def _validate_app_client_secret(self: 'MainScreenController', text: str) -> bool:
		# TODO
		# return re.finditer(, ,)
		return not bool(text)


	def set_docs_path_callback(self: 'MainScreenController', sel: 'list[android.net.Uri]') -> None:
		if not sel:
			return

		uri_or_path: 'android.net.Uri | str' = sel[0]

		if platform != 'android':
			self.log.debug('FS: Access path: `%s`', uri_or_path)
			assert isinstance(uri_or_path, str)  # linter plug
			self.model.docs_path = uri_or_path  # TODO: Solve normally -_-
			self.model.notify_observers('settings_screen')
			return

		self.log.debug('FS: Access SS Uri: %s', StrCall(uri_or_path.toString))

		uri_full_path: str = uri_or_path.toString()

		self.model.docs_path = uri_full_path
		self.model.notify_observers('settings_screen')


	def set_docs_path(self: 'MainScreenController') -> None:
		filechooser.choose_dir(
			# on_selection=lambda s: self.log.warning(f'result: {s}'),
			on_selection=self.set_docs_path_callback,
		)
