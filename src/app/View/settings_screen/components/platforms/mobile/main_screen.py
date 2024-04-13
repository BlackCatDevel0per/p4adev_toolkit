from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from app.libs.PyScopedStorage.filechooser import filechooser
from app.View.base_screen import BaseScreenView
from kivy.logger import Logger
from kivy.properties import StringProperty
from kivymd.toast import toast
from kivymd.uix.relativelayout import MDRelativeLayout
from plyer.utils import platform

if TYPE_CHECKING:
	from typing import Callable


# TODO: Full screen mode & hide status bar & more comfartable read functions..


class SecretTextFieldRound(MDRelativeLayout):
	text = StringProperty()
	hint_text = StringProperty()


class SettingsScreenView(BaseScreenView):

	def startup(self: 'SettingsScreenView') -> None:
		...


	def _validate_app_client_id(self: 'SettingsScreenView', text: str) -> bool:
		return not text.isnumeric()


	def _validate_app_client_secret(self: 'SettingsScreenView', text: str) -> bool:
		# TODO
		# return re.finditer(, ,)
		return not bool(text)


	def set_docs_dir_conf(self: 'SettingsScreenView', uri: str) -> None:
		self.app.config.set('app', 'docs_dir', uri)

		self.app.config.write()

		toast('Download path set!')


	def set_scdir_callback(self: 'SettingsScreenView', sel: 'list[android.net.Uri]') -> None:
		if not sel:
			return

		uri = sel[0]

		if platform != 'android':
			self.set_docs_dir_conf(Path(uri))
			return

		Logger.warning(f'ACCESS URI: {uri.toString()}')

		dir_full_path = uri.toString()

		self.set_docs_dir_conf(dir_full_path)


	def set_scdir(self: 'SettingsScreenView') -> None:
		filechooser.choose_dir(
			# on_selection=lambda s: Logger.warning(f'result: {s}'),
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
