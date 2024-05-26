from __future__ import annotations

from functools import partial
from time import perf_counter
from typing import TYPE_CHECKING

from kivy.clock import Clock

from app.utility.logger import Loggable
from app.utility.utils import defprop

if TYPE_CHECKING:
	from collections.abc import Callable
	from typing import Any, Literal

	from kivy.clock import ClockEvent


class ClockTimer(Loggable):

	# Sets on start
	start_time = defprop(priv_name='_start_time', set_once=True)
	has_started = defprop(priv_name='_has_started', set_once=True)
	# Changes by "main event" (default '-1' - if hasn't been call yet)
	last_call_time = defprop(priv_name='_last_call_time')
	# TODO: More flex configure prop..
	# Changes by "vals update event"
	apr_next_call_time = defprop(priv_name='_apr_next_call_time')
	# Changes by "vals update event"
	expiration_time = defprop(lambda self: self._expiration_time)


	@property
	def time_sec(self: 'ClockTimer') -> float:
		return self._time_sec


	@time_sec.setter
	def time_sec(self: 'ClockTimer', value: 'int | float') -> None:
		self.stop()
		self._time_sec = value
		self._expiration_time = value


	def __init__(
		self: 'ClockTimer',
		callback: 'Callable[[Any], None]',
		event_type: "Literal['interval'] | Literal['once']" = 'once',
		time_sec: 'int | float' = 0,
		timer_update_interval_sec: 'int | float' = 1,
		log_preprefix: str = '',
	) -> None:
		self.event: 'ClockEvent'
		self._has_started: bool = False
		self.__event_type = event_type
		self.__timer_update_interval_sec = timer_update_interval_sec
		self._callback = callback
		self._start_time: float
		self._time_sec = time_sec  # less changes
		self._apr_next_call_time: float = perf_counter() + self._time_sec
		self._last_call_time: float = -1
		self._expiration_time = self._time_sec  # diff between last & next call

		self._log_preprefix: str = log_preprefix


	def __post_init__(self: 'ClockTimer') -> None:
		if self._log_preprefix:
			self._p_log_prefix = f'{self._log_preprefix}: ClockTimer'
		else:
			self._p_log_prefix = 'ClockTimer'

		super().__post_init__()


	def stop(self: 'ClockTimer') -> None:
		if not hasattr(self, 'event'):
			return
		self.event.cancel()


	def __start_main_event(self: 'ClockTimer') -> None:
		# TODO: Use partial..
		self.log.debug(
			'%s: [%s] Starting "main event"..',
			self.__class__.__name__,
			self._callback,
		)

		# main task
		def prop_update_wrapper(timer: ClockTimer, dt) -> None:
			timer.last_call_time = perf_counter()
			self._callback(dt)

		if self.__event_type == 'interval':
			self.event = Clock.schedule_interval(partial(prop_update_wrapper, self), self.time_sec)
		elif self.__event_type == 'once':
			self.event = Clock.schedule_once(partial(prop_update_wrapper, self), self.time_sec)
		else:
			raise TypeError


	def __start_vals_update_event(self: 'ClockTimer') -> None:
		self.log.debug(
			'%s: [%s] Starting "vals update event"..',
			self.__class__.__name__,
			self._callback,
		)

		# update vals helper task
		def expiration_prop_update(timer: ClockTimer, event: 'ClockEvent', dt) -> None:
			##
			print(
				timer.apr_next_call_time, '-', perf_counter(),
				'==', max(timer.apr_next_call_time - perf_counter(), 0),
			)
			# NOTE: Never get event instance from timer directly!
			is_event_pending: bool = event.next is not None or event.prev is not None
			# if main event not end (to avoid value change by two events on restart)
			if is_event_pending:
				timer._expiration_time = max(timer.apr_next_call_time - perf_counter(), 0)  # noqa: SLF001
				# recalc next call time if event is intervally
				if self.__event_type == 'interval' and timer.expiration_time <= 0:
					self.log.debug('%s: self vals reset', self.__class__.__name__)
					timer.apr_next_call_time = timer.last_call_time + self.time_sec
			# "update vals event" kill if event is end
			elif not is_event_pending:
				self.log.debug(
					'%s: %s - event end, stopping this update event..',
					self.__class__.__name__, self._callback,
				)
				timer._update_event.cancel()  # noqa: SLF001

		# update vals before begin
		if not self._has_started:
			# set start time if it's first time start
			self.start_time = perf_counter()
			self.has_started = True
		if self.last_call_time != -1:
			self.apr_next_call_time = self.last_call_time + self.time_sec
		else:
			self.apr_next_call_time = perf_counter() + self.time_sec
		# TODO: Sub-callback for external stuff (for example save value to disk beside `on_pause` event)
		self._update_event: 'ClockEvent' = Clock.schedule_interval(
			partial(expiration_prop_update, self, self.event),
			self.__timer_update_interval_sec,
		)


	def start(self: 'ClockTimer') -> None:
		self.__start_main_event()
		self.__start_vals_update_event()



	def restart(self: 'ClockTimer', time_sec: 'int | float | None' = None) -> None:
		"""Stop pending event with optionally given time."""
		if time_sec is None:
			time_sec = self.time_sec

		self.log.debug(
			'%s: Reset timer (cancel event & start new with the same callback)',
			self.__class__.__name__,
		)
		self.stop()
		self.time_sec = time_sec
		self.start()
