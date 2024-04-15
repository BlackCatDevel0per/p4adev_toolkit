from __future__ import annotations

from typing import TYPE_CHECKING

from plyer.utils import platform

if TYPE_CHECKING:
	from collections.abc import Callable
	from typing import Any

	pr_decorated_func = Callable[[], dict[str, Any]]

# TODO: Move this to another lib..


def platform_run(plat: str) -> Callable[[pr_decorated_func], None]:
	"""Little workaround to avoid platform check code duplicating.

	Usage:
	.. code-block:: python

		@platform_run('android')
		def _():
			from android import mActivity

			return locals()
	"""
	def wrapper(func: pr_decorated_func) -> None:
		if platform != plat:
			return
		# Update function's globals using returned locals
		locs = func()
		func.__globals__.update(locs)

	return wrapper
