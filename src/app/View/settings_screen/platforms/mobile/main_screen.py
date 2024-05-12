from __future__ import annotations

from typing import TYPE_CHECKING

from app.utility.utils import StrCall
from app.View.base_screen import BaseScreenView
from kivymd.toast import toast
from plyer.utils import platform
from PyScopedStorage.filechooser import filechooser

if TYPE_CHECKING:
	from typing import Callable


# TODO: Full screen mode & hide status bar & more comfartable read functions..


class SettingsScreenView(BaseScreenView):

	def startup(self: 'SettingsScreenView') -> None:
		...


	def _validate_app_client_id(self: 'SettingsScreenView', text: str) -> bool:
		return not text.isnumeric()


	def _validate_app_client_secret(self: 'SettingsScreenView', text: str) -> bool:
		# TODO
		# return re.finditer(, ,)
		return not bool(text)


	def set_docs_path_conf(self: 'SettingsScreenView', uri: str) -> None:
		self.app.config.set('app', 'docs_path', uri)

		self.app.config.write()

		toast('Docs path set!')


	def set_scdir_callback(self: 'SettingsScreenView', sel: 'list[android.net.Uri]') -> None:
		if not sel:
			return

		uri_or_path: 'android.net.Uri | str' = sel[0]

		if platform != 'android':
			self.log.debug('Access path: `%s`', uri_or_path)
			assert isinstance(uri_or_path, str)  # linter plug
			self.set_docs_path_conf(uri_or_path)  # TODO: Solve normally -_-
			return

		self.log.debug('Access SS Uri: %s', StrCall(uri_or_path.toString))

		dir_full_path: str = uri_or_path.toString()

		self.set_docs_path_conf(dir_full_path)


	def set_scdir(self: 'SettingsScreenView') -> None:
		filechooser.choose_dir(
			# on_selection=lambda s: self.log.warning(f'result: {s}'),
			on_selection=self.set_scdir_callback,
		)


	# TODO: Move into the model
	def save_settings(self: 'SettingsScreenView', btn) -> None:
		...


	def model_is_changed(self: 'SettingsScreenView') -> None:
		"""Call whenever any change has occurred in the data model.

		The view in this method tracks these changes and updates the UI
		according to these changes.
		"""


MainScreenView = SettingsScreenView
