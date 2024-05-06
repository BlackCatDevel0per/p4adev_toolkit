from __future__ import annotations

from typing import TYPE_CHECKING

from kivy.utils import platform

from app.bases.abc import AppBaseABCLike

if platform == 'android':
    from android import mActivity

    # TODO: Find or make stubs for java android api used from pyjnius.. or better make mypy plugin..
    from jnius import autoclass

if TYPE_CHECKING:
    # NOTE: Type annotations from typing block are still quoted because
    # cython will raise errors in functions & methods annotations.. (but still ok for vars)
    from typing import Any


class AppTweaks(AppBaseABCLike):

    def on_app_init(self: 'AppTweaks', **kwargs: 'Any') -> None:
        self.bind_to({'android_set_handle_native_autorotate': 'on_start'})


    def android_set_handle_native_autorotate(self: 'AppTweaks') -> None:
        # Set startup orientation because value from manifest is ignored..
        # (depends on the system auto-rotate option)
        if platform != 'android':
            return

        ActivityInfo = autoclass('android.content.pm.ActivityInfo')

        mActivity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_FULL_USER)

        del ActivityInfo
