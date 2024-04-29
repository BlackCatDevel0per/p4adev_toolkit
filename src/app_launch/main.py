from os import environ as os_environ

from app.entry.launch import run
from plyer.utils import platform

# TODO: C/Compiled entry point

# NOTE: Use this part only for debug purposes (in prod comment these lines)
os_environ['DEBUG_ACCESS_APP'] = '1'
if platform == 'android' and os_environ.get('DEBUG_ACCESS_APP') is not None:
    from p4adev_tools import ftp_server_proc, ipython_kernel_thread

    ftp_server_proc()
    ipython_kernel_thread()

if __name__ == '__main__':
    run()
