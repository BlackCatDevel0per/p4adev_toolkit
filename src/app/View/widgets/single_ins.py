from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from typing import Any

# TODO: Disable optionally..


class SingleInstance:

	_ins = None

	def __new__(cls: 'type[SingleInstance]', *args: 'Any', **kwargs: 'Any') -> 'SingleInstance':
		if not isinstance(cls._ins, cls):
			cls._ins = super().__new__(cls, *args, **kwargs)

		return cls._ins
