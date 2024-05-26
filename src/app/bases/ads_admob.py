from __future__ import annotations

from os import environ as os_env
from time import perf_counter
from typing import TYPE_CHECKING

import kivmob as kmob
from kivy.logger import Logger
from kivymd.toast import toast
from plyer.utils import platform

from app import APP_CONF_PATH
from app.bases.abc import AppBaseABCLike
from app.utility.clock_timer import ClockTimer
from app.utility.logger import Loggable

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


def _ad_timer_save(amount: int) -> None:
	with open(f'{APP_CONF_PATH}/.lat', 'w') as f:
		f.write(str(perf_counter() + amount))


def _ad_timer_get() -> float:
	try:
		with open(f'{APP_CONF_PATH}/.lat') as f:
			sec: float = float(f.read()) - perf_counter()
			# if somebody will change the value manually XD
			if sec < 0:
				raise ValueError
			return sec
	except (ValueError, FileNotFoundError):
		_ad_timer_save(0)
		return 0


class AdsAdmob(AppBaseABCLike):

	def on_app_init(self: 'AdsAdmob') -> None:
		self._ads: kmob.KivMob = kmob.KivMob(ADMOB_APP_ID)

		self.__adfree_rh: ADFreeRewardHandler = ADFreeRewardHandler(self._ads)
		self._ads.set_rewarded_ad_listener(self.__adfree_rh)
		self.__adfree_rh.load_video()

		self.bind_to({'_show_ads': 'on_build'})


	def on_pause(self: 'AdsAdmob') -> bool:
		# toast(f'{self.app_site} app pause')
		_ad_timer_save(self.__adfree_rh.amount)

		return True


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
		# TODO: Mb better use it with request (move & call cls method directly)
		if self.__adfree_rh.is_timer_expired:
			self.ads.show_banner()


	def _add_main_banner(self: 'AdsAdmob') -> None:
		"""Start screen banner."""
		self.ads.new_banner(ADMOB_MAIN_BANNER_ID, top_pos=False)
		self.ads.request_banner()


class ADFreeRewardHandler(kmob.RewardedListenerInterface, Loggable):

	_p_log_prefix: str = 'ADFree Reward Handler'

	def __init__(self: 'ADFreeRewardHandler', ads: kmob.KivMob) -> None:
		# FIXME: Mb listener can already have instance access..?
		self.__ads: AdsAdmob = ads
		self.__reward: str = ''

		# TODO: Separate this stuff from handler instance..
		def show_ad_banner_again(dt) -> None:
			# if we got multiple reward
			msg: str = 'Showing ad banner again..'
			toast(msg)
			self.log.debug(msg)
			self.ads.show_banner()

		resume_time_sec: int = int(_ad_timer_get())
		self.log.debug('Got resume time %i', resume_time_sec)

		# self resume trigger (until adfree time is not expired)
		self.__show_ad_banner_again_clock_timer: 'ClockTimer' = \
			ClockTimer(
				show_ad_banner_again,
				time_sec=resume_time_sec,
				timer_update_interval_sec=1 * 60,
				# timer_update_interval_sec=60,
				log_preprefix='Ads',
			)


	def __post_init__(self: 'ADFreeRewardHandler') -> None:
		super().__post_init__()

		# resume
		if not self.is_timer_expired:
			self.log.debug(
				'Ads: resume timer from %i mins',
				round(self.__show_ad_banner_again_clock_timer.time_sec / 60, 3),
			)
			self.__show_ad_banner_again_clock_timer.start()
		else:
			self.log.debug(
				'Ads: timer is %i, nothing to resume..',
				self.__show_ad_banner_again_clock_timer.time_sec,
			)

		# # [FOR TESTS ONLY] Uncomment on desktop
		# self.on_rewarded('adfree-time', 3)


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
		"""Amount of estimated remaining time (usually to use in gui)."""
		return self.__show_ad_banner_again_clock_timer.expiration_time


	@amount.setter
	def amount(self: 'ADFreeRewardHandler', value: int) -> None:
		if value <= 0:
			return
		max_limit = 35 * 60  # NOTE: Set here your multiply limit
		self.__show_ad_banner_again_clock_timer.restart(min(value, max_limit))
		_ad_timer_save(self.amount)

		self.ads.hide_banner()

		# TODO: More control reward..


	@property
	def is_timer_expired(self: 'ADFreeRewardHandler') -> bool:
		return self.amount <= 0


	def load_video(self: 'ADFreeRewardHandler') -> None:
		self.ads.load_rewarded_ad(ADMOB_ADMOB_MAIN4OFF_REWARD_ID)


	def on_rewarded_video_ad_started(self: 'ADFreeRewardHandler') -> None:
		"""External call method."""
		self.load_video()


	def on_rewarded(self: 'ADFreeRewardHandler', name: str, amount_mins: int) -> None:
		"""External call method."""
		# TODO: Access check..
		self.reward = name
		self.amount += amount_mins * 60

		toast(f'ADFree time increased up to {self.amount // 60} (add {amount_mins}) mins')


	def on_rewarded_video_ad_left_application(self: 'ADFreeRewardHandler') -> None:
		"""External call method if user hasn't fully viewed the ad."""
		toast('No reward..')
