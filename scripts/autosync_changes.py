# TODO: Some fixes & publish to PyPi..

from __future__ import annotations

import json
import threading
import time
from collections import deque
from datetime import datetime as dt
from ftplib import FTP
from os import sep as os_sep
from pathlib import Path
from typing import TYPE_CHECKING

import regex as re
from cachetools import TTLCache
from ftputil import FTPHost

# from rich import print as rprint
from watchdog.events import (
	DirCreatedEvent,
	DirDeletedEvent,
	DirModifiedEvent,  # Unused
	DirMovedEvent,
	FileCreatedEvent,
	FileDeletedEvent,
	FileModifiedEvent,
	FileMovedEvent,
	FileSystemEvent,
	FileSystemEventHandler,
)
from watchdog.observers import Observer

println = print
from rich import print

if TYPE_CHECKING:
	from collections.abc import Callable, Iterable, Sequence
	from typing import Any, Final, TypedDict



# TODO: Queue? (for large files to cancel sending if modified - optionally)
# TODO: Startup checks..
# TODO: Dynamic reload this file
# TODO: Immutable string..?
CURRENT_PATH = Path.cwd()

# TODO: More cli..
SYNC_CONFIG: Final[Path] = Path(CURRENT_PATH, 'sync_config.json')

# TODO: Pydantic check..
SC: dict[str, str | dict[str, str | int]] = {}

# TODO: Update config..
if SYNC_CONFIG.exists():
	with open(SYNC_CONFIG) as sc:
		SC = json.load(sc)

_SC_CS: dict[str, str | int] = SC['connection_settings']

# TODO: Do something with non-relative paths..
PROJECT_PATH: Final[Path] = Path(SC.get('PROJECT_PATH') or CURRENT_PATH).resolve()

print(PROJECT_PATH)


class FTPSession(FTP):

	def __init__(self, host, user, passwd, port):
		"""Act like ftplib.FTP's constructor but connect to another port."""

		super().__init__()  ##
		self.connect(host, port)
		self.login(user, passwd)

##
REMOTE_HOST: Final[Callable[[], [FTPHost]]] = lambda: FTPHost(  # noqa: E731
	host=_SC_CS['host'], port=_SC_CS['port'],
	user=_SC_CS['user'],
	passwd=_SC_CS['passwd'],
	session_factory=FTPSession,
)


class FileSystemEventHandlerWithThrottling(FileSystemEventHandler):
	def __init__(
		self: FileSystemEventHandlerWithThrottling,
		*args: Any,
		ttl_kwargs: dict[str, Any] = {'maxsize': 10_000, 'ttl': 1},
		events2ttl: FileSystemEvent | tuple[FileSystemEvent, ...] = (FileSystemEvent),
		**kwargs: Any,
	) -> None:
		super().__init__(*args, **kwargs)

		self.throttled_events: TTLCache = TTLCache(**ttl_kwargs)
		self.event_types2ttl = events2ttl


	def dispatch(self: FileSystemEventHandlerWithThrottling, event: FileSystemEvent) -> None:
		if isinstance(event, self.event_types2ttl) and event in self.throttled_events:
			# TODO: Logging..
			# FIXME: Time..
			# print(
			# 	'Skipped event '
			# 	f'[{round(time.perf_counter() - self.throttled_events[event], 8)} sec.]: '
			# 	f'{event}'
			# )
			return

		super().dispatch(event)

		# FIXME: Better use list..
		self.throttled_events[event] = time.perf_counter()


class CreModEvent(FileCreatedEvent, FileModifiedEvent, DirCreatedEvent):
	"""File/Dir Create/Modify events exclude `DirModifiedEvent`."""

	event_type = 'file(created|modified)|dir(created)'
	is_directory = False


class FTPEventQueue(deque):

	def _del_ops(self: FTPEventQueue, items: Sequence[FileSystemEvent]) -> None:
		if not items:
			return

		for item in items:
			self.remove(item)


	def _filter_ops_before_delete(
		self: FTPEventQueue, item: FileDeletedEvent | DirDeletedEvent,
	) -> tuple[list[FileSystemEvent], bool]:
		its = []

		# If file will not exist
		is_deleted_before: bool = False
		is_moved_before: bool = False

		for it in self:
			# Mov->Del
			if it.dest_path == item.src_path:
				its.append(it)

			if it.src_path != item.src_path:
				continue

			#####..
			if isinstance(it, (FileMovedEvent, DirMovedEvent)):
				its.append(it)
				is_moved_before = True
				continue

			##
			if isinstance(it, (FileDeletedEvent, DirDeletedEvent)):
				is_deleted_before = True

			its.append(it)

		if is_moved_before:
			return its, False

		return its, not its or is_deleted_before
		##return its, is_deleted_before or not is_moved_before


	def _find_reverse_moved_op(
		self: FTPEventQueue, item: FileMovedEvent | DirMovedEvent,
	) -> FileMovedEvent:
		rev_moved_event: FileMovedEvent | DirMovedEvent | None = None

		for it in self:
			# type and is_rev
			if isinstance(it, (FileMovedEvent, DirMovedEvent)) and it.src_path == item.dest_path:
				rev_moved_event = it

		return rev_moved_event


	def _checks4put(self: FTPEventQueue, item: FileSystemEvent) -> None:
		# My lazy optimizations.. (LETO - Lazy Execute Time Optimizations)

		# TODO: Dirs proc in the other method..

		# NOTE: All ops is with single item

		# Unite Created & Modified events, because for upload operation it's no sense..
		# 2.
		# TODO: Handle dir modifications?? (because can be changed dir perms.. Mb handle using another ways..)
		if isinstance(item, (FileCreatedEvent, FileModifiedEvent, DirCreatedEvent)):
			# TODO: Mb just reuse object instead of re-creating if it will be destination of that object life-cycle..
			item_ = CreModEvent(
				src_path=item.src_path,
				dest_path=item.dest_path,  # TODO: Remove?

				is_synthetic=item.is_synthetic,  # TODO: Remove??
			)

			item_.is_directory = item.is_directory

			item = item_

			del item_

			####
			# TODO: More avoid ops duplications..

			if item in self:
				return

		# 1. Clean all if file will deleted
		# Any+Del -> Del
		# Make+Del | Mod+Del | Make+Any+Del -> Nothing
		elif isinstance(item, (FileDeletedEvent, DirDeletedEvent)):
			# TODO: Cut to "frames"

			obd, add_item = self._filter_ops_before_delete(item)

			# print(self)
			# print(f'DROP {obd}: ADD {add_item} | ITEM {item}')
			# print(self)
			# print('tg')

			self._del_ops(obd)

			if not add_item:
				return

		# 3. Handling short-cycling movements
		elif isinstance(item, (FileMovedEvent, DirMovedEvent)):
			# (move is rename too)
			# Move+BackMove -> Nothing
			it = self._find_reverse_moved_op(item)

			# print(self)
			# print(f'DROP {(it,)}: ITEM {item}')

			if it:
				self._del_ops((it,))
				return


		## TODO: Del+Make is/-> Modify

		# More Move events handle & mb -Copy- Handle..

		# By default
		super().append(item)


	def append(self: FTPEventQueue, item: FileSystemEvent) -> None:
		# print('Add item: ', item)
		self._checks4put(item)

# TODO: Handle "complex" cycling movements..

# TODO: Move into unit tests & another project (because there's mess..)
"""
# # Test 1 (ops before file remove)
# qfp = 'test.txt'

# ## If created with some ops after & will deleted
# q = FTPEventQueue()
# # q = deque()
# q.append(FileDeletedEvent(src_path=qfp))
# q.append(CreModEvent(src_path=qfp))
# q.append(CreModEvent(src_path=qfp))
# q.append(FileDeletedEvent(src_path=qfp))
# q.append(CreModEvent(src_path=qfp))

# # q.append(FileDeletedEvent(src_path='not_' + qfp))

# # q.append(FileCreatedEvent(src_path='not_' + qfp))
# # q.append(FileDeletedEvent(src_path='not_' + qfp))

# print(q)
# exit()

# ## If some ops & will deleted
# q = FTPEventQueue()
# q.append(FileModifiedEvent(src_path=qfp))
# q.append(FileDeletedEvent(src_path=qfp))
# q.append(FileCreatedEvent(src_path='not_' + qfp))

# print(q)
# exit()

# ## If some ops & will deleted
# q = FTPEventQueue()
# ##
# q.append(FileDeletedEvent(src_path=qfp))
# q.append(CreModEvent(src_path=qfp))
# q.append(FileDeletedEvent(src_path=qfp))
# q.append(FileCreatedEvent(src_path='not_' + qfp))

# print(q)
# exit()

# # If will moved
# q = FTPEventQueue()
# q.append(FileMovedEvent(src_path=qfp, dest_path=qfp + '1'))
# q.append(FileMovedEvent(src_path=qfp + '1', dest_path=qfp))

# q.append(FileCreatedEvent(src_path='not_' + qfp))
# q.append(FileModifiedEvent(src_path='not_' + qfp))
# q.append(FileModifiedEvent(src_path='not_' + qfp))
# q.append(FileModifiedEvent(src_path='not_' + qfp))

# q.append(FileDeletedEvent(src_path='_' + qfp))
# q.append(FileCreatedEvent(src_path='_' + qfp))
# q.append(FileDeletedEvent(src_path='_' + qfp))

# print(q)
# exit()

# q = FTPEventQueue()

# # q.append(FileCreatedEvent(src_path='4913'))
# # q.append(FileModifiedEvent(src_path='4913'))
# # q.append(FileDeletedEvent(src_path='4913'))

# q.append(FileMovedEvent(src_path='blah', dest_path='blah~'))
# # q.append(FileMovedEvent(src_path='blah~', dest_path='blah'))##won't be.. but also handled..

# # q.append(FileCreatedEvent(src_path='blah'))
# # q.append(FileModifiedEvent(src_path='blah'))

# q.append(FileDeletedEvent(src_path='blah~'))


# print(q)
# exit()
"""


class FTPTransactionsExecutor:
	def __init__(
		self: FTPTransactionsExecutor,
		wd_handler: AutoSyncHandler,
		deq: FTPEventQueue, interval: int | float = 5,
	) -> None:
		self.wd_handler: AutoSyncHandler = wd_handler
		self._ev_deq: FTPEventQueue = deq
		self._interval: int | float = interval
		self._running: bool = False


	def bind_path(
		self: FTPTransactionsExecutor,
		ev_local_path: Path, ev_remote_path: Path,
	) -> Path:
		"""Get bound path from local and remote-bind from config."""
		if not self.wd_handler.paths_bind:
			return ev_remote_path

		for local, remote in self.wd_handler.paths_bind.items():
			if local in ev_local_path.parents:
				# TODO: Mb optionally exclude `local` key from `remote` for easier syntax?
				ev_remote_path = Path(os_sep, remote, ev_remote_path)

				##break

		return ev_remote_path


	def get_bound_paths(
		self: FTPTransactionsExecutor,
		event: FileCreatedEvent | FileModifiedEvent | DirCreatedEvent,
	) -> tuple[Path, Path]:
		# TODO: More work with local bound paths..
		ev_local_path: Path = Path(event.src_path)
		ev_remote_path: Path = Path(os_sep, event.src_path).relative_to(self.wd_handler.root_path)

		ev_remote_path = self.bind_path(ev_local_path, ev_remote_path)

		return ev_local_path, ev_remote_path


	def get_bound_move_paths(
		self: FTPTransactionsExecutor,
		event: FileMovedEvent | DirMovedEvent,
	) -> tuple[tuple[Path, Path], tuple[Path, Path]]:
		##os_sep

		ev_local_path_from: Path = Path(event.src_path)
		ev_remote_path_from: Path = Path(os_sep, event.src_path).relative_to(self.wd_handler.root_path)
		ev_remote_path_from = self.bind_path(ev_local_path_from, ev_remote_path_from)

		ev_local_path_to: Path = Path(event.dest_path)
		ev_remote_path_to: Path = Path(os_sep, event.dest_path).relative_to(self.wd_handler.root_path)
		ev_remote_path_to = self.bind_path(ev_local_path_to, ev_remote_path_to)

		return (ev_local_path_from, ev_local_path_to), (ev_remote_path_from, ev_remote_path_to)


	def on_file_cremoded(
		self: FTPTransactionsExecutor,
		host: FTPHost,
		event: FileCreatedEvent | FileModifiedEvent,
	) -> None:
		# TODO: Exceptions handle..
		local_path, remote_path = self.get_bound_paths(event)

		println(f'STOR [{local_path!s}] -> [{remote_path!s}]')

		# TODO: Use upload_if_newer..
		host.upload(local_path, remote_path)


	def on_file_moved(
		self: FTPTransactionsExecutor,
		host: FTPHost,
		event: FileCreatedEvent | FileModifiedEvent,
	) -> None:
		local_paths, remote_paths = self.get_bound_move_paths(event)
		local_move_from, local_move_to = local_paths
		remote_move_from, remote_move_to = remote_paths

		println(f'LMOVE [{local_move_from!s}] -> [{local_move_to!s}]')
		println('<->')
		println(f'MOVE [{remote_move_from!s}] -> [{remote_move_to!s}]')

		host.rename(remote_move_from, remote_move_to)


	def on_file_deleted(
		self: FTPTransactionsExecutor,
		host: FTPHost,
		event: DirCreatedEvent,
	) -> None:
		local_path, remote_path = self.get_bound_paths(event)

		println(f'DELE [{local_path!s}] <-> [{remote_path!s}]')

		host.remove(remote_path)


	def on_dir_created(
		self: FTPTransactionsExecutor,
		host: FTPHost,
		event: DirCreatedEvent,
	) -> None:
		local_path, remote_path = self.get_bound_paths(event)

		println(f'MKD [{local_path!s}] -> [{remote_path!s}]')

		host.makedirs(remote_path)


	def on_dir_moved(
		self: FTPTransactionsExecutor,
		host: FTPHost,
		event: FileCreatedEvent | FileModifiedEvent,
	) -> None:
		local_paths, remote_paths = self.get_bound_move_paths(event)
		local_move_from, local_move_to = local_paths
		remote_move_from, remote_move_to = remote_paths

		println(f'LDMOVE [{local_move_from!s}] -> [{local_move_to!s}]')
		println('<->')
		println(f'DMOVE [{remote_move_from!s}] -> [{remote_move_to!s}]')

		host.rename(remote_move_from, remote_move_to)


	def on_dir_deleted(
		self: FTPTransactionsExecutor,
		host: FTPHost,
		event: DirCreatedEvent,
	) -> None:
		local_path, remote_path = self.get_bound_paths(event)

		println(f'RMD [{local_path!s}] <-> [{remote_path!s}]')

		host.rmdir(remote_path)


	def proc_dir_event(
		self: FTPTransactionsExecutor,
		host: FTPHost,
		event: CreModEvent | DirDeletedEvent | DirMovedEvent,
	) -> None:
		# TODO: Better wrap methods..
		if isinstance(event, CreModEvent):
			self.on_dir_created(host, event)

		elif isinstance(event, DirDeletedEvent):
			self.on_dir_deleted(host, event)

		elif isinstance(event, DirMovedEvent):
			self.on_dir_moved(host, event)

		else:
			raise TypeError

		println('FileEvent(s) Complete!')


	def proc_file_event(
		self: FTPTransactionsExecutor,
		host: FTPHost,
		event: CreModEvent | FileDeletedEvent | FileMovedEvent,
	) -> None:
		if isinstance(event, CreModEvent):
			self.on_file_cremoded(host, event)

		elif isinstance(event, FileDeletedEvent):
			self.on_file_deleted(host, event)

		elif isinstance(event, FileMovedEvent):
			self.on_file_moved(host, event)

		else:
			raise TypeError

		println('FileEvent(s) Complete!')


	def start(self: FTPTransactionsExecutor) -> None:
		self._running = True

		while self._running:
			time.sleep(self._interval)

			if not self._ev_deq:
				continue

			try:
				with REMOTE_HOST() as rh:
					while self._ev_deq:
						# TODO: Lock while jobs pending or wait (do nothing) while events handling by ftp client..
						event = self._ev_deq.popleft()

						# TODO: Move into the method..
						# FIXME: Rename to multiple count..
						if not event.is_directory:
							self.proc_file_event(rh, event)
						else:
							self.proc_dir_event(rh, event)
			except Exception as e:
				# print('{e} with event {ev}'.format(e=e, ev=event))
				print('{e} with event'.format(e=e))#, ev=event))


	def stop(self: FTPTransactionsExecutor) -> None:
		self._running = False


class AutoSyncHandler(FileSystemEventHandlerWithThrottling):
	def __init__(
		self: AutoSyncHandler,
		*args: Any,
		root_path: Path = Path(),
		filters: dict[str, list[str]] = {'include': ['*'], 'exclude': []},  # TODO: TypedDict
		paths_bind: dict[str, str],
		convert2full_paths: bool = True,
		executor_interval: int | float = 10,
		**kwargs: Any,
	) -> None:
		super().__init__(*args, **kwargs)

		self.root_path: Final[Path] = root_path
		# TODO: Lists of path..?
		self.paths_bind: Final[dict[Path, Path]] = {}
		if convert2full_paths:
			for k, v in paths_bind.items():
				k_ = Path(self.root_path, k)
				v_ = Path(v)

				self.paths_bind[k_] = v_

		print(paths_bind)

		self.ftp_transfer_queue = FTPEventQueue()
		# TODO: Mb better use asyncio..
		self.ftp_transactions_executor = FTPTransactionsExecutor(
			wd_handler=self,
			deq=self.ftp_transfer_queue,
			interval=executor_interval,
		)
		# TODO: Better logging..

		self.filters: Final[dict[str, list]] = filters


	def add_event(self: AutoSyncHandler, event: FileCreatedEvent) -> None:
		self.ftp_transfer_queue.append(event)


	def on_created(self: AutoSyncHandler, event: FileCreatedEvent | DirCreatedEvent) -> None:
		self.add_event(event)


	def on_modified(self: AutoSyncHandler, event: FileModifiedEvent | DirModifiedEvent) -> None:
		if event.is_directory:
			return

		self.add_event(event)


	def on_moved(self: AutoSyncHandler, event: FileMovedEvent | DirMovedEvent) -> None:
		# TODO: Mb group events by basic ops?

		self.add_event(event)


	def on_deleted(self: AutoSyncHandler, event: FileDeletedEvent | DirDeletedEvent) -> None:
		self.add_event(event)


if __name__ == "__main__":
	ex_interval = 12

	event_handler = AutoSyncHandler(
		root_path=PROJECT_PATH,
		filters=SC['filters'],
		paths_bind=SC['paths_bind'],
		executor_interval=ex_interval,
	)

	observer = Observer()
	observer.schedule(event_handler, PROJECT_PATH, recursive=True)
	observer.start()

	ftp_executor_thread = threading.Thread(
		target=event_handler.ftp_transactions_executor.start,
	)
	ftp_executor_thread.start()

	print('Project AutoSync started!')

	try:
		# outed = False
		while True:
			time.sleep(ex_interval - ((ex_interval / 100) * 30))

			if not event_handler.ftp_transfer_queue:
				continue

			# TODO: Better logging..
			print(dt.utcnow(), event_handler.ftp_transfer_queue, sep=' ')

	except KeyboardInterrupt:
		observer.stop()
		observer.join()

		event_handler.ftp_transactions_executor.stop()
		ftp_executor_thread.join()

