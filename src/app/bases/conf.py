from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from app import APP_CONF_PATH
from app.bases.abc import AppBaseABCLike

if TYPE_CHECKING:
	from kivy.config import ConfigParser


class AppConf(AppBaseABCLike):

	def get_application_config(
		self: 'AppConf',
		default_path: str = str(
			Path(
				APP_CONF_PATH,
				'config.ini',
			),
		),
	) -> str:
		"""Set default config path."""
		return default_path


	def build_config(self: 'AppConf', config: 'ConfigParser') -> None:
		# TODO: Use TypedDict with Literal(s).. (for easier lint)
		config.setdefaults(
			'theme',
			{
				'palette': 'Teal',
				'accent': 'Green',
				'style': 'Dark',
			},
		)

		config.setdefaults(
			'app',
			{
				'docs_path': '',
			},
		)
