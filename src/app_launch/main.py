from __future__ import annotations

from os import environ as os_env
from typing import TYPE_CHECKING

from app.entry.launch import run
from plyer.utils import platform

if TYPE_CHECKING:
    from typing import Final

# TODO: C/Compiled entry point

# NOTE: Use this part only for debug purposes (in prod at least comment this line)
os_env['DEBUG_ACCESS_APP'] = '1'

is_debug: 'Final[bool]' = os_env.get('DEBUG_ACCESS_APP') is not None


# TODO: Move main stuff into the app.bases..


def main() -> None:
    """Wrap to run debug helpers before app."""
    if not is_debug:
        run()
        return

    if platform == 'android':
        from p4adev_tools import ftp_server_proc, ipython_kernel_thread

        # TODO: Optionally toast info..
        ftp_server_proc()
        ipython_kernel_thread()

    if platform != 'android':
        # Set mobile-like resolution for easier tests
        from kivy.core.window import Window
        Window.size = (480, 800)

    run()


if __name__ == '__main__':
    main()
