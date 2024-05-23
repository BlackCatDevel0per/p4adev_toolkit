from __future__ import annotations

from os import environ as os_env
from typing import TYPE_CHECKING

import kivmob as kmob
from kivy.logger import Logger
from kivymd.toast import toast
from plyer.utils import platform

from app.bases.abc import AppBaseABCLike

if TYPE_CHECKING:
	from typing import Final

ADMOB_APP_ID: str
ADMOB_MAIN_BANNER_ID: str
ADMOB_ADMOB_MAIN4OFF_REWARD_ID: str

if platform == 'android':
	from android import mActivity

	# Fix activity add view error
	kmob.activity = mActivity

	context = mActivity.getApplicationContext()
	pm = context.getPackageManager()
	app_info_bundle = pm.getApplicationInfo(context.getPackageName(), pm.GET_META_DATA)
	get_app_info = lambda s: app_info_bundle.metaData.getString(s)  # noqa: E731

	ADMOB_APP_ID = get_app_info('com.google.android.gms.ads.APPLICATION_ID')
	ADMOB_MAIN_BANNER_ID = get_app_info('admob_main-banner')
	ADMOB_ADMOB_MAIN4OFF_REWARD_ID = get_app_info('admob_main4off-reward')

	if ADMOB_APP_ID is None or ADMOB_MAIN_BANNER_ID is None:
		raise ValueError

	is_debug: 'Final[bool]' = os_env.get('DEBUG_ACCESS_APP') is not None

	if is_debug:
		# Warning if use admob test ids
		if ADMOB_APP_ID != kmob.TestIds.APP \
			and ADMOB_MAIN_BANNER_ID != kmob.TestIds.BANNER:
			Logger.warning('Ads - Google Admob: Using test ids - cause app is in debug mode!')
		else:
			# TODO: Big Warning..
			pass
else:
	ADMOB_APP_ID = \
		ADMOB_ADMOB_MAIN4OFF_REWARD_ID = \
		ADMOB_MAIN_BANNER_ID = ''


class AdsAdmob(AppBaseABCLike):

	def on_app_init(self: 'AdsAdmob') -> None:
		self._ads = kmob.KivMob(ADMOB_APP_ID)

		self.__adfree_rh = ADFreeRewardHandler(self._ads)
		self._ads.set_rewarded_ad_listener(self.__adfree_rh)
		self.__adfree_rh.load_video()

		self.bind_to({'_show_ads': 'on_build'})


	@property
	def ads(self: 'AdsAdmob') -> kmob.KivMob:
		return self._ads


	def _show_ads(self: 'AdsAdmob') -> None:
		"""AdMob Ads."""
		# WARNING: If you use incorrect device id not equal from `adb logcat -s Ads` ads will not show
		# and device id can change..
		# TODO: Dynamic get from logs.. or at least give it to user..
		# self.ads.add_test_device('S0ME1ID1FROM1CATLOG')

		self._add_main_banner()


	def _add_main_banner(self: 'AdsAdmob') -> None:
		"""Start screen banner."""
		self.ads.new_banner(ADMOB_MAIN_BANNER_ID, top_pos=False)
		self.ads.request_banner()
		self.ads.show_banner()


class ADFreeRewardHandler(kmob.RewardedListenerInterface):

	def __init__(self: 'ADFreeRewardHandler', ads: kmob.KivMob) -> None:
		# FIXME: Mb listener can already have instance access..?
		self.__ads: AdsAdmob = ads
		self.__reward: str = ''
		self.__amount: int = 0

	@property
	def ads(self: 'ADFreeRewardHandler') -> kmob.KivMob:
		return self.__ads


	@property
	def reward(self: 'ADFreeRewardHandler') -> str:
		return self.__reward


	@reward.setter
	def reward(self: 'ADFreeRewardHandler', value: str) -> None:
		self.__reward = value


	@property
	def amount(self: 'ADFreeRewardHandler') -> int:
		return self.__amount


	@amount.setter
	def amount(self: 'ADFreeRewardHandler', value: int) -> None:
		max_limit = 35  # NOTE: Set here your multiply limit
		self.__amount = max(self.__amount + value, max_limit)

		self.ads.hide_banner()
		# TODO: Add timer..
		# TODO: Show banner again on timer end
		# TODO: More control reward..


	def load_video(self: 'ADFreeRewardHandler') -> None:
		self.ads.load_rewarded_ad(ADMOB_ADMOB_MAIN4OFF_REWARD_ID)


	def on_rewarded_video_ad_started(self: 'ADFreeRewardHandler') -> None:
		"""External call method."""
		self.load_video()


	def on_rewarded(self: 'ADFreeRewardHandler', name: str, amount: int) -> None:
		"""External call method."""
		# TODO: Access check..
		self.reward = name
		self.amount += amount
		toast(f'ADFree time increased up to {self.amount} mins')


	def on_rewarded_video_ad_left_application(self: 'ADFreeRewardHandler') -> None:
		"""External call method if user hasn't fully viewed the ad."""
		toast('No reward..')
