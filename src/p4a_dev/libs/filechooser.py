from os import fdopen as os_fdopen
from typing import TYPE_CHECKING

try:
	from aiofiles import open as async_open
except ImportError:
	def async_open(p, m):
		raise ModuleNotFoundError

from plyer import filechooser
from plyer.utils import platform

if platform == 'android':
	from android import mActivity
	from plyer.platforms.android.filechooser import DocumentsContract, Intent

	ContentResolver = mActivity.getContentResolver()

if TYPE_CHECKING:
	from io import TextIOWrapper

	from aiofile import BinaryFileWrapper, TextFileWrapper


def make_scoped_file(
	access_uri: 'android.net.Uri',
	name: str,
	mode: str = 'w',
	mime: str = '*/*',
) -> int:
	# TODO: Optionally return file uri
	file_uri: 'android.net.Uri' = DocumentsContract.createDocument(
		ContentResolver,
		access_uri,
		mime, name,
	)

	ret = get_io_wrap_from_fd(file_uri, mode)
	del file_uri

	return ret


def make_scoped_file_sync(
	access_uri: 'android.net.Uri',
	name: str,
	mode: str = 'w',
	mime: str = '*/*',
) -> 'TextIOWrapper':
	return os_fdopen(make_scoped_file(access_uri, name, mode, mime), mode)


def make_scoped_file_async(
	access_uri: 'android.net.Uri',
	name: str,
	mode: str = 'w',
	mime: str = '*/*',
) -> 'TextFileWrapper | BinaryFileWrapper':
	return async_open(make_scoped_file(access_uri, name, mode, mime), mode)


mksf_sync = make_scoped_file_sync
mksf_async = make_scoped_file_async

# We're processing uris using `get_io_wrap_from_fd` & we don't need this method
filechooser._resolve_uri = lambda val: val


def _open_dir(**kwargs) -> None:
	# set up selection handler
	# startActivityForResult is async
	# onActivityResult is sync
	filechooser._handle_selection = kwargs.pop(
		'on_selection', filechooser._handle_selection,
	)

	intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)

	intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
	intent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
	# TODO: Handle persistent req
	intent.addFlags(Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION)

	mActivity.startActivityForResult(intent, filechooser.select_code)


	del intent


def _file_selection_dialog(**kwargs):
	mode = kwargs.pop('mode', None)
	if mode == 'open':
		filechooser._open_file(**kwargs)

	if mode == 'dir':
		_open_dir(**kwargs)


if platform == 'android':
	filechooser._file_selection_dialog = _file_selection_dialog


def get_io_wrap_from_fd(
	content_uri: 'android.net.Uri',
	mode: str = 'r',
) -> int:
	"""
	Note for open modes: https://developer.android.com/reference/android/content/ContentResolver#openFileDescriptor(android.net.Uri,%20java.lang.String,%20android.os.CancellationSignal)
	"""

	# TODO: Object with using uri directly....
	# TODO: CancellationSignal..

	if mode == 'rb':
		jp_mode = 'r'
	elif mode == 'wb':
		jp_mode = 'w'
	else:
		jp_mode = mode

	fdo: 'android.os.ParcelFileDescriptor' = ContentResolver.openFileDescriptor(
		content_uri,
		jp_mode,
	)
	fd: 'int' = fdo.detachFd()

	return fd
