from __future__ import annotations

from typing import TYPE_CHECKING

from kivy.utils import platform

from app.bases.abc import AppBaseABCLike

if platform == 'android':
	from android import mActivity
	context: 'jni[android.content.Context]' = mActivity.getApplicationContext()
	from jnius import autoclass
else:
	import sys
	from multiprocessing import Process
	from subprocess import Popen

if TYPE_CHECKING:
	from typing import Any


class AppServices(AppBaseABCLike):

	def on_app_init(self: 'AppServices', **kwargs: 'Any') -> None:
		self.bind_to({'start_services': 'on_start'})


	def _start_service(
		self: 'AppServices',
		name: str,
		method: str = 'proc',
		module: 'str | None' = None,
		import_kw: 'dict[str, Any]' = {'fromlist': ['']},  # noqa: B006
	) -> 'Service | Process':
		if platform == 'android':
			sn: str = f'{self.app_site}.Service{name}'
			service = autoclass(sn)
			service.start(mActivity, '')
			return service

		if module is None:
			msg = 'Missing module arg for non-android platform..'
			raise TypeError(msg)

		if method == 'proc':
			m = __import__(module, **import_kw)
			process = Process(target=m.main)
			process.start()
		elif method == 'subproc':
			# FIXME: Soooo crutchy..
			module = 'src' + '/' + module
			process = Popen([sys.executable, f"{module.replace('.', '/')}.py"])

		return process


	# TODO: Kill procs on exit..


	def start_services(self: 'AppServices') -> None:
		# IPYkernel for jupyter console connect
		# NOTE: Don't forget to enable yours services from `app/services` in spec file!

		# self.dev_ipy_service = self._start_service(
		# 	'Devipykernel',
		# 	'subproc',
		# 	'app.services.dev_ipykernel',
		# )
		...
