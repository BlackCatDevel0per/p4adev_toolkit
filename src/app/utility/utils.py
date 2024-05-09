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


def UniteMetas(*args: 'type', name: str = 'UnitedMetas') -> 'type':  # noqa: N802
	"""Unite metaclassesfrom args to avoid metaclass conflicts.

	To see what's was united use: `UnitedMetas._metas`

	See: https://stackoverflow.com/a/28727066/22622061
	"""
	# aka: class UnitedMetas(type(MDScreen), type(Loggable)):
	return type(name, tuple(type(cls) for cls in args), {'_metas': args})


class PostInitableMeta(type):
	"""Just automatically call `__post_init__` method of the class instance after `__init__`."""

	def __call__(cls: 'type', *args: 'Any', **kwargs: 'Any') -> object:
		"""Make class instance and call `__post_init__`."""
		# NOTE: If you use Singleton, it will still work properly
		obj = type.__call__(cls, *args, **kwargs)
		# Avoid re-call `__post_init__` if object will use something like singleton..
		# to allow force recall just set `obj._post_init_allow_recall = True` in your objects
		if (
			getattr(obj, '_post_init_allow_recall', False)
			or
			not getattr(obj, '_post_init_called', False)
		):
			obj.__post_init__()
			obj._post_init_called = True  # noqa: SLF001

		return obj
