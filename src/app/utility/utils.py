from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from collections.abc import Callable
	from typing import Any


# NOTE: Lol looks like coroutine..
class StrCall:
	"""Call callable from arg on `str()` or formatting (usable for logging stuff).

	Example:
	-------
	.. code-block:: python
		from functools import patrial
		from pathlib import Path

		logger.info('%s', StrCall(partial(Path, 'some/path/or/other/arg')))

	"""

	def __init__(self: 'StrCall', call: 'Callable[[], str | Any]') -> None:
		self.call = call

	def __str__(self: 'StrCall') -> str:
		return str(self.call())


class PostInitableMeta(type):
	"""Just automatically call `__post_init__` method of the class instance after `__init__`."""

	def __call__(cls: type, *args: 'Any', **kwargs: 'Any') -> object:
		"""Make class instance and call `__post_init__`."""
		obj = type.__call__(cls, *args, **kwargs)
		obj.__post_init__()
		return obj
