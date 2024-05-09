# TODO: Find another workarounds to not write abcs XD
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	# old `Type` used to avoid compiled app errors like:
	# TypeError: Expected type, got NoInheritMeta
	from typing import Any, Dict, Tuple, Type  # noqa: UP035


class NoInheritMeta(type):
	"""Just not inhetirate classes, but linter will still think it's inhetirated.

	Why? Because I don't like long inheritance chain &
	in some places where I don't want to use composition with delegation.
	"""

	def __new__(
		cls: 'Type',  # FIXME: Annotate it right..
		name: str, bases: 'Tuple[type, ...]', dct: 'Dict[str, Any]',
	) -> 'Type':
		# TODO: Generate methods using bases, but without code - on `NotImplementedError`
		if name.endswith('ABCLike'):
			return type.__new__(cls, name, (), dct)

		return type.__new__(cls, name, bases, dct)
