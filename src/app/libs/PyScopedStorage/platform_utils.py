from __future__ import annotations

from typing import TYPE_CHECKING

from plyer.utils import platform

if TYPE_CHECKING:
	from collections.abc import Callable
	from typing import Any, Dict, TypeVar  # noqa: UP035

	pr_decorated_func = Callable[[], Dict[str, Any]]  # noqa: UP006
	DF = TypeVar('DF', bound=pr_decorated_func)


# TODO: Move this to another lib..


def platform_run(plat: str) -> Callable[[DF], None]:
	"""Little workaround to avoid platform check code duplicating.

	Usage:
	.. code-block:: python

		@platform_run('android')
		def _():
			from android import mActivity

			return locals()
	"""
	def wrapper(func: DF) -> None:
		if platform != plat:
			return
		# Update function's globals using returned locals
		locs = func()
		func.__globals__.update(locs)

	return wrapper
