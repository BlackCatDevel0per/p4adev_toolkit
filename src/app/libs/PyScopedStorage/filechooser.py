from __future__ import annotations

from typing import TYPE_CHECKING

from plyer import filechooser
from plyer.utils import platform

if platform == 'android':
	from .android_objects import Intent, mActivity

if TYPE_CHECKING:
	from typing import Any


def pyss_resolve_uri(uri):
	_uri = uri
	is_uri_list = False
	if isinstance(uri, list):
		is_uri_list = True
		_uri = uri[0]

	# TODO: More tests..
	ret = _uri.buildUpon().appendPath('document').appendPath(_uri.getLastPathSegment())
	if is_uri_list:
		_uri[0] = ret
		del uri  ##
		return _uri

	return ret


if platform == 'android':
	# We're processing uris using `PyScopedStorage.tools.make_scoped_file` & we don't need this method
	filechooser._resolve_uri = pyss_resolve_uri  # noqa: SLF001

	orig_on_activity_result = filechooser._on_activity_result  # noqa: SLF001


def pyss_open_dir(**kwargs: dict[str, Any]) -> None:
	# set up selection handler
	# startActivityForResult is async
	# onActivityResult is sync
	filechooser._handle_selection = kwargs.pop(  # noqa: SLF001
		'on_selection', filechooser._handle_selection,  # noqa: SLF001
	)

	intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)

	# TODO: Handle persistent req

	mActivity.startActivityForResult(intent, filechooser.select_code)

	del intent


def pyss_on_activity_result(self, request_code, result_code, data):
	orig_on_activity_result(request_code, result_code, data)

	# TODO: Ignore on file calls..?
	resolver = mActivity.getContentResolver()
	resolver.getPersustablePermission(
		self.selection,
		Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
		| Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION,
	)


def pyss_file_selection_dialog(**kwargs):
	mode = kwargs.pop('mode', None)
	if mode == 'open':
		filechooser._open_file(**kwargs)  # noqa: SLF001

	if mode == 'dir':
		pyss_open_dir(**kwargs)


if platform == 'android':
	filechooser._file_selection_dialog = pyss_file_selection_dialog  # noqa: SLF001
	filechooser._on_activity_result = pyss_on_activity_result  # noqa: SLF001
