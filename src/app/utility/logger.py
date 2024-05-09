from __future__ import annotations

from logging import DEBUG, INFO, getLogger
from os import environ as os_env
from typing import TYPE_CHECKING

from app.utility.utils import PostInitableMeta

if TYPE_CHECKING:
	from logging import Logger
	# from typing import Final


CURRENT_LEVEL: int = INFO
if any((os_env.get('DEBUG_ACCESS_APP'), os_env.get('DEBUG_LOG_APP'))):
	CURRENT_LEVEL = DEBUG

# TODO: Fully overwrite kivy logging format..
# TODO: More configuration and use rich handler optionally..
# NOTE: Change 'KIVY_LOG_MODE' env var to `PYTHON` if you want handle logs fully by your self
# basicConfig(
# 	format='[%(levelname)s] - %(module)s %(message)s',
# 	level=CURRENT_LEVEL,
# )


class Loggable(metaclass=PostInitableMeta):

	_p_log_prefix: str = ''

	def __post_init__(self: 'Loggable') -> None:
		# aka `app.utility.logger.Loggable`
		self._p_log_name: str = f'{self.__module__}.{self.__class__.__name__}'
		self.log: 'Logger' = getLogger(self._p_log_name)
		self.log.setLevel(DEBUG)
		self.log.debug('[%s] Post-Init `%s`', self._log_prefix, self._log_name)


	@property
	def _log_prefix(self: 'Loggable') -> str:
		return self._p_log_prefix


	@property
	def _log_name(self: 'Loggable') -> str:
		# TODO: Make singlonized property..
		return self._p_log_name
