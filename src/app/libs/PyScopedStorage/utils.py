from __future__ import annotations

from typing import TYPE_CHECKING

from plyer.utils import platform

if platform == 'android':
	from .android_objects import ContentResolver, Uri

if TYPE_CHECKING:
	from pyslet.rfc2396 import URI


def get_fd_from_android_uri(
	content_uri: 'android.net.Uri',
	mode: str = 'r',
) -> int:
	"""Open and detach android java file descriptor for	directly access in python.

	Note for open modes:
	https://developer.android.com/reference/android/content/ContentResolver#openFileDescriptor(android.net.Uri,%20java.lang.String,%20android.os.CancellationSignal)
	"""
	# TODO: CancellationSignal..

	# Stuff around modes to correctly use in the java descriptor
	if mode == 'rb':
		jp_mode = 'r'
	elif mode == 'wb':
		jp_mode = 'w'
	else:
		jp_mode = mode

	fd_obj: 'android.os.ParcelFileDescriptor' = ContentResolver.openFileDescriptor(
		content_uri,
		jp_mode,
	)
	fd: int = fd_obj.detachFd()

	return fd


def get_fd_from_uri(
	uri: URI,
	mode: str = 'r',
) -> int:
	android_uri: 'android.net.Uri' = Uri.parse(str(uri))
	return get_fd_from_android_uri(android_uri, mode)


def get_fd_from_struri(
	struri: str,
	mode: str = 'r',
) -> int:
	android_uri: 'android.net.Uri' = Uri.parse(struri)
	return get_fd_from_android_uri(android_uri, mode)
