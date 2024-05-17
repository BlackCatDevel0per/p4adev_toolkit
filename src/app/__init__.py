from os import environ as os_env
from os import makedirs as mkdirs
from pathlib import Path
from typing import TYPE_CHECKING

from plyer.utils import platform

if TYPE_CHECKING:
	from typing import Final

module_dir: str = str(Path(__file__).parent)

# TODO: Ways to export/import settings from app
# Set conf path near app path
_app_path: str
if platform == 'android':
	os_env['ANDROID_APP_CONF_PATH'] = os_env['ANDROID_PRIVATE'] + '/' + 'app_conf'
	_app_path = os_env['ANDROID_APP_CONF_PATH']
else:
	_app_path = str(Path.cwd())

mkdirs(_app_path, exist_ok=True)

APP_CONF_PATH: 'Final[str]' = _app_path
