from __future__ import annotations

from plyer.utils import platform

if platform != 'android':
	msg = "Can't access android api"
	raise AttributeError(msg)

from android import mActivity
from jnius import autoclass
from plyer.platforms.android.filechooser import DocumentsContract, Intent  # noqa: F401

ContentResolver = mActivity.getContentResolver()
Uri = autoclass('android.net.Uri')
