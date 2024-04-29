from __future__ import annotations

from typing import TYPE_CHECKING

from plyer.utils import platform

if TYPE_CHECKING:
	from collections.abc import Callable
	from typing import Any, Final, TypeVar

	local_scope = dict[str, Any]
	pr_decorated_func = Callable[[], local_scope]
	DF = TypeVar('DF', bound=pr_decorated_func)


# TODO: Move this to another lib..


class platform_run:
	"""Little workaround to avoid platform check code duplicating.

	Usage:
	.. code-block:: python

		@platform_run('android')
		def _():
			from android import mActivity

			return locals()
	"""

	def __init__(self: platform_run, plat: str) -> None:
		self.plat: Final[str] = plat


	def __call__(self: platform_run, func: DF) -> None:
		if platform != self.plat:
			return

		# Update function's globals using returned locals
		locs = func()
		func.__globals__.update(locs)
