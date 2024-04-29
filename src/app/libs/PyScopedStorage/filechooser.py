from __future__ import annotations

from typing import TYPE_CHECKING

from plyer import filechooser
from plyer.utils import platform

if platform == 'android':
	from functools import partial

	from android import activity

	from .android_objects import Intent, mActivity

if TYPE_CHECKING:
	from typing import Any

	from .android_objects import Uri


# TODO: Just extend class..

# FIXME: Look at mypy docs & annotate more better..
def pyss_resolve_uri(uri: list[Uri] | Uri) -> list[Uri] | Uri:
	"""Append a few paths to dir uri.

	For correctly work with `PyScopedStorage.tools.mksf_{sync,async}`.
	"""
	filechooser.selection_raw = uri
	_uri: Uri = uri
	is_uri_list = False
	if isinstance(uri, list):
		is_uri_list = True
		_uri = uri[0]

	# TODO: More tests..
	# NOTE: More use `pyslet.rfc2396.URI` in your python code
	ret = _uri.buildUpon().appendPath('document').appendPath(_uri.getLastPathSegment())
	if is_uri_list:
		assert not isinstance(_uri, list)  # linter plug
		_uri[0] = ret
		return _uri

	return ret


def pyss_open_dir(**kwargs: dict[str, Any]) -> None:
	filechooser._handle_selection = kwargs.pop(  # noqa: SLF001
		'on_selection', filechooser._handle_selection,  # noqa: SLF001
	)

	intent: 'android.content.Intent' = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)

	# TODO: Handle persistent req

	mActivity.startActivityForResult(intent, filechooser.select_code)

	del intent


def pyss_on_activity_result(self, request_code: int, result_code: int, data: Intent) -> None:
	sel = self.selection_raw if not isinstance(self.selection_raw, list) else self.selection_raw[0]
	# FIXME: Clean `self.selection_raw`
	# TODO: Ignore on file calls..?
	resolver: 'android.content.ContentResolver' = mActivity.getContentResolver()
	resolver.takePersistableUriPermission(
		sel,
		# TODO: Make flags as option..
		Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION,
	)

	del resolver


def pyss_file_selection_dialog(**kwargs: dict[str, Any]) -> None:
	"""Open selection dialog with dir select support."""
	mode = kwargs.pop('mode', None)
	if mode == 'open':
		filechooser._open_file(**kwargs)  # noqa: SLF001

	if mode == 'dir':
		pyss_open_dir(**kwargs)


if platform == 'android':
	# We're processing uris using `PyScopedStorage.tools.make_scoped_file` & we don't need this method
	filechooser._resolve_uri = pyss_resolve_uri  # noqa: SLF001

	# Override filechooser instance method to handle directory choose
	filechooser._file_selection_dialog = pyss_file_selection_dialog  # noqa: SLF001
	# Bind take persistent uri permission to dir selection
	# (you can get it using ContentResolver's method `getPersistedUriPermissions`)
	activity.bind(on_activity_result=partial(pyss_on_activity_result, filechooser))

	# NOTE: activity.bind binds on object pointer itself, not on the name
	# (hold it in the head if you use class methods or etc.)
