# from ipykernel import kernelapp
from os import environ as os_environ

from p4a_dev.app.launch import run
from plyer.utils import platform

# TODO: C/Compiled entry point

# NOTE: Use this part only for debug purposes (in prod comment these lines)

# TODO: Publish tools to PyPi..

if platform == 'android' or os_environ.get('DEBUG_ACECSS_APP') is not None:
    # Just for debug
    import logging
    import multiprocessing
    from socket import AF_INET, SOCK_DGRAM, socket

    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer


    def get_ip():
        s = socket(AF_INET, SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP


    # Sync stuff (use like InstantRun in AStudio) using watchdog-ftp-sync
    # or access by any ftp client

    # TODO: Write ftp logs to different place..
    ftpl = logging.getLogger('pyftpdlib')


    def run_ftp_server():
        authorizer = DummyAuthorizer()
        authorizer.add_user('android', 'android', '.', perm='elradfmw')

        handler = FTPHandler
        handler.authorizer = authorizer

        ip, port = '0.0.0.0', 2121
        server = FTPServer((ip, port), handler)
        server.serve_forever()

        # TODO: Toast on any updates..

        ftpl.warning(f'FTP server started on ip {get_ip()} port {port}')


    # TODO: On app quit/stop correctly destroy process..
    # Access using your device ip (you can get it from device options "About phone")
    ftp_process = multiprocessing.Process(target=run_ftp_server)
    ftp_process.start()

    from p4a_dev.libs.dev.dev_ipykernel import main as run_ipyk_thread
    run_ipyk_thread()

if __name__ == '__main__':
    run()
