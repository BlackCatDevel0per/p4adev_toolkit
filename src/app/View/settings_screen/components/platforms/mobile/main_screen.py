from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from app.libs.filechooser import filechooser
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

	def startup(self) -> None:
		...


	def _validate_app_client_id(self, text: str) -> bool:
		return not text.isnumeric()


	def _validate_app_client_secret(self, text: str) -> bool:
		# TODO
		# return re.finditer(, ,)
		return not bool(text)


	def set_dload_path_conf(self, path: 'str | Path') -> None:
		self.app.config.set('app', 'dload_path', str(path))

		self.app.config.write()

		toast('Download path set!')


	def set_download_path_callback(self, sel: 'list[android.net.Uri]') -> None:
		if not sel:
			return

		uri = sel[0]

		if platform != 'android':
			self.set_dload_path_conf(Path(uri))
			return

		Logger.warning(f'ACCESS URI: {uri.toString()}')

		# uri_path: str = uri.getPath()

		# # FIXME: Use alternative variant to get dir path..
		# dir_path = uri_path.split(':')[1]

		# dir_full_path = Path(primary_external_storage_path(), dir_path)
		# dir_full_path = Path('/sdcard/', dir_path)
		dir_full_path = uri.toString()

		self.set_dload_path_conf(Path(dir_full_path))


	def set_download_path(self) -> None:
		filechooser.choose_dir(
			# on_selection=lambda s: Logger.warning(f'result: {s}'),
			on_selection=self.set_download_path_callback,
		)


	# TODO: Move into the model
	def save_settings(self, btn) -> None:
		...


	def model_is_changed(self) -> None:
		"""Call whenever any change has occurred in the data model.

		The view in this method tracks these changes and updates the UI
		according to these changes.
		"""


MainScreenView = SettingsScreenView
