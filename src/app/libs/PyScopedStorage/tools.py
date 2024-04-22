from __future__ import annotations

from os import fdopen as os_fdopen
from typing import TYPE_CHECKING

from plyer.utils import platform

if platform == 'android':
	from .android_objects import ContentResolver, DocumentsContract

from .io import async_open
from .utils import get_fd_from_android_uri

if TYPE_CHECKING:
	from io import BufferedReader, BufferedWriter, TextIOWrapper

	from aiofiles.threadpool.binary import AsyncBufferedIOBase, AsyncBufferedReader
	from aiofiles.threadpool.text import AsyncTextIOWrapper


def make_scoped_file(
	access_uri: 'android.net.Uri',
	name: str,
	mode: str = 'w',
	mime: str = '*/*',
) -> int:
	"""Make file using access (usually directory) android uri and return the file descriptor."""
	# TODO: Optionally return file uri
	file_uri = dc_make_doc(
		access_uri,
		name, mime,
	)

	ret = get_fd_from_android_uri(file_uri, mode)
	del file_uri

	return ret


def dc_make_doc(
	access_uri: 'android.net.Uri',
	name: str,
	mime: str = '*/*',
) -> 'android.net.Uri':
	"""Make file using access (usually directory) android uri and return the file uri."""
	# TODO: Optionally return file uri
	# TODO: Raise error if file exists..
	return DocumentsContract.createDocument(
		ContentResolver,
		access_uri,
		mime, name,
	)


def make_scoped_file_sync(
	access_uri: 'android.net.Uri',
	name: str,
	mode: str = 'w',
	mime: str = '*/*',
) -> TextIOWrapper | BufferedReader | BufferedWriter:
	return os_fdopen(make_scoped_file(access_uri, name, mode, mime), mode)


def make_scoped_file_async(
	access_uri: 'android.net.Uri',
	name: str,
	mode: str = 'w',
	mime: str = '*/*',
) -> AsyncTextIOWrapper | AsyncBufferedReader | AsyncBufferedIOBase:
	return async_open(make_scoped_file(access_uri, name, mode, mime), mode)


mksf_sync = make_scoped_file_sync
mksf_async = make_scoped_file_async
