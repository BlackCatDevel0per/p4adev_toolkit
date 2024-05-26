from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from collections.abc import Callable
	from typing import Any, Type  # noqa: UP035


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

	def __call__(cls: 'Type', *args: 'Any', **kwargs: 'Any') -> object:
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


# TODO: Move it into another lib..
class defprop(property):

	def __init__(
		self: 'defprop',
		obj: 'Any' = None, priv_name: str = '',
		fdel=None, doc=None, *, set_once: bool = False,
	) -> None:
		self._is_set: bool = False

		fset: 'Callable[[Any, Any], None] | None'
		if priv_name:
			if obj is not None:
				def fget(ins: 'Any'):
					return obj
			else:
				def fget(ins: 'Any'):
					return getattr(ins, priv_name)

			if set_once:
				def fset(ins: 'Any', val) -> None:
					if self._is_set:
						msg = 'This attribute can only be set once.'
						raise AttributeError(msg)
					self._is_set = True
					setattr(ins, priv_name, val)
			else:
				def fset(ins: 'Any', val: 'Any') -> None:
					setattr(ins, priv_name, val)
		else:
			fget = obj
			fset = None

		super().__init__(fget=fget, fset=fset, fdel=fdel, doc=doc)
