from __future__ import annotations

from os import environ as os_env
from typing import TYPE_CHECKING

import kivmob as kmob
from kivy.logger import Logger
from plyer.utils import platform

from app.bases.abc import AppBaseABCLike

if TYPE_CHECKING:
	from typing import Final

admob_app_id: str
admob_main_banner_id: str

if platform == 'android':
	from android import mActivity

	# Fix activity add view error
	kmob.activity = mActivity

	context = mActivity.getApplicationContext()
	pm = context.getPackageManager()
	app_info_bundle = pm.getApplicationInfo(context.getPackageName(), pm.GET_META_DATA)
	get_app_info = lambda s: app_info_bundle.metaData.getString(s)  # noqa: E731

	admob_app_id = get_app_info('com.google.android.gms.ads.APPLICATION_ID')
	admob_main_banner_id = get_app_info('admob_main-banner')

	if admob_app_id is None or admob_main_banner_id is None:
		raise ValueError

	is_debug: 'Final[bool]' = os_env.get('DEBUG_ACCESS_APP') is not None

	if is_debug:
		# Warning if use admob test ids
		if admob_app_id != kmob.TestIds.APP \
			and admob_main_banner_id != kmob.TestIds.BANNER:
			Logger.warning('Ads - Google Admob: Using test ids - cause app is in debug mode!')
		else:
			# TODO: Big Warning..
			pass
else:
	admob_app_id = ''
	admob_main_banner_id = ''


class AdsAdmob(AppBaseABCLike):

	@property
	def ads(self: 'AdsAdmob') -> kmob.KivMob:
		return self._ads

	def on_app_init(self: 'AdsAdmob') -> None:
		self._ads = kmob.KivMob(admob_app_id)

		self.bind_to({'_show_ads': 'on_build'})


	def _show_ads(self: 'AdsAdmob') -> None:
		"""AdMob Ads."""
		# WARNING: If you use incorrect device id not equal from `adb logcat -s Ads` ads will not show
		# and device id can change..
		# TODO: Dynamic get from logs.. or at least give it to user..
		# self.ads.add_test_device('S0ME1ID1FROM1CATLOG')

		self._add_main_banner()


	def _add_main_banner(self: 'AdsAdmob') -> None:
		"""Start screen banner."""
		self.ads.new_banner(admob_main_banner_id, top_pos=False)
		self.ads.request_banner()
		self.ads.show_banner()


	def _show_interstitial_banner(self: 'AdsAdmob') -> None:
		"""Start screen banner."""
		# TODO: Add interstitial ad to turn off other ads to half hour
