from __future__ import annotations

from typing import TYPE_CHECKING

from plyer.utils import platform

from app.bases.abc import AppBaseABCLike

if platform == 'android':
	# TODO: Add pyjnius to deps..
	from android import mActivity
	from android.broadcast import BroadcastReceiver
	from jnius import autoclass

	ConnectivityManager = autoclass('android.net.ConnectivityManager')

	Context = mActivity.getApplicationContext()
	cm = mActivity.getSystemService(Context.CONNECTIVITY_SERVICE)


if TYPE_CHECKING:
	from typing import Any


class AppBroadcast(AppBaseABCLike):

	def on_app_init(self: 'AppBroadcast', **kwargs: 'Any') -> None:
		self.bind_to({'set_network_state_broadcast': 'on_start'})

		self.br_network_state = None


	def set_network_state_broadcast(self: 'AppBroadcast') -> None:
		# TODO: Make helper method `only_android_platform` for all this stuff..
		if platform != 'android':
			self.log.debug('br: Platform is not Android, skip receiver reg..')
			return

		if self.br_network_state is not None:
			return

		self.log.debug('br: Registering network state check receiver..')

		self.br_network_state = BroadcastReceiver(
			self.br_on_net_state,
			actions=[ConnectivityManager.CONNECTIVITY_ACTION],
		)

		self.log.debug('br: Starting network state check receiver..')

		self.br_network_state.start()


	@property
	def _br_net_conn_available(self: 'AppBroadcast') -> bool:
		# NOTE: Only Android property!
		net_info = cm.getActiveNetworkInfo()
		return net_info is not None and net_info.isConnected()


	def br_on_net_state(
		self: 'AppBroadcast',
		context: 'jni[...]',
		intent: 'jni[...]',
	) -> None:
		if self._br_net_conn_available:
			self.br_on_net_available()
		else:
			self.br_on_net_unavailable()


	def br_on_net_available(self: 'AppBroadcast') -> None:
		self.log.info('App: Network/Internet connection available')
		self.binds_run('on_net_state_on')


	def br_on_net_unavailable(self: 'AppBroadcast') -> None:
		self.log.info('App: Network/Internet connection unavailable..')
		self.binds_run('on_net_state_off')
