from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from aiofiles import open as async_open
else:
	def _throw_plug_async_open(p, m):
		raise ModuleNotFoundError

try:
	from aiofiles import open as async_open
except ImportError:
	async_open = _throw_plug_async_open
