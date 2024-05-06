from __future__ import annotations

from os import environ as os_env
from typing import TYPE_CHECKING

from app.bases.abc import AppBaseABCLike

if TYPE_CHECKING:
	# NOTE: Type annotations from typing block are still quoted because
	# cython will raise errors in functions & methods annotations.. (but still ok for vars)
	from typing import Any, Final


class AppDebug(AppBaseABCLike):

	def on_app_init(self: 'AppDebug', **kwargs: 'Any') -> None:
		self.bind_to({'up_debug_access': 'on_start'})


	def up_debug_access(self: 'AppDebug') -> None:
		"""Run debug helpers on app start."""
		# ex. `com.bcdev.p4a_bdev` - we're interested in `bdev` suffix
		if self.app_site.endswith('bdev'):
			# NOTE: Use this part only for debug purposes (in prod at least comment this line)
			os_env['DEBUG_ACCESS_APP'] = '1'

		is_debug: 'Final[bool]' = os_env.get('DEBUG_ACCESS_APP') is not None

		if not is_debug:
			return

		# if platform != 'android':
		#     return

		from p4adev_tools import ftp_server_proc, ipython_kernel_thread

		# TODO: Optionally toast info..
		ftp_server_proc()
		# TODO: Solve graphics calls issues for non-android platforms.. (as option)
		# NOTE: Reccoment to use `from kivy.clock import mainthread`
		ipython_kernel_thread()
