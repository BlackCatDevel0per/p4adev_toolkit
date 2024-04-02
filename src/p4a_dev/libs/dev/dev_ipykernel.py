from __future__ import annotations

from os import getpid as os_getpid
from os import environ as os_environ
from os import makedirs as mkdirs
from packaging import version
from threading import current_thread as get_current_thread

from ipykernel import __version__ as ipyk_v

# TODO: Fork & update imports..
from background_zmq_ipython import IPythonBackgroundKernelWrapper, OurIPythonKernel
from traceback import format_exc
from pathlib import Path
from plyer.utils import platform

# TODO: Make base class for services..

# from jnius import autoclass

# PythonService = autoclass('org.kivy.android.PythonService')
# PythonService.mService.setAutoRestartService(True)


class IPyWrapper(IPythonBackgroundKernelWrapper):

    _update_conf: 'Callable[[traitlets.config.loader.Config], None] | None' = None
    _post_init_callback: 'Callable[[IPyWrapper], None] | None' = None


    def _create_kernel(self):
        """
        Creates the kernel.
        This should be done in the background thread.
        """
        from traitlets.config.loader import Config
        assert get_current_thread() is self.thread
        # Creating the kernel will also initialize the shell (ZMQInteractiveShell) on the first call.
        # The shell will have the history manager (HistoryManager).
        # HistoryManager/HistoryAccessor will init the Sqlite DB. It will be closed via atexit,
        # so we want to allow the access from a different thread at that point.
        # Also see here: https://github.com/ipython/ipython/issues/680
        config = Config()
        config.InteractiveShell.banner2 = self._banner
        config.HistoryAccessor.connection_options = dict(check_same_thread=False)

        if self._update_conf is not None:
            self._logger.info('Running update_conf..')
            self._update_conf(config)

        kernel = OurIPythonKernel(
            session=self._session,
            **(dict(shell_stream=self._shell_stream, control_stream=self._control_stream)
               if version.parse(ipyk_v) >= version.parse('6.0')
               else dict(shell_streams=[self._shell_stream, self._control_stream])),
            iopub_socket=self._iopub_socket,
            log=self._logger,
            user_ns=self.user_ns,
            config=config)
        with self._condition:
            self._kernel = kernel
            self._condition.notify_all()


    def _start_kernel(self):
        """
        Starts the kernel itself.
        This must run in the background thread.
        """
        assert get_current_thread() is self.thread

        self._create_session()
        self._create_sockets()
        self._write_connection_file()

        self._setup_streams()
        self._create_kernel()

        self._logger.info(
            "IPython: Start kernel now. pid: %i, thread: %r",
            os_getpid(), get_current_thread())
        if self._redirect_stdio:
            import atexit
            self._init_io()
            atexit.register(self._reset_io)

        if self._post_init_callback is not None:
            self._logger.info('Running post_init_callback..')
            self._post_init_callback(self)

        self._kernel.start()


    def _create_sockets(self):
        import zmq
        import socket
        from ipykernel.heartbeat import Heartbeat

        context = zmq.Context()  # or existing? zmq.Context.instance()

        shell_socket = context.socket(zmq.ROUTER)
        iopub_socket = context.socket(zmq.PUB)
        control_socket = context.socket(zmq.ROUTER)

        if not hasattr(self, '_connection_info'):            
            self._logger.info('Setting connection info..')

            if self._allowed_remote_connections:
                ip = socket.gethostbyname(socket.gethostname())
            else:
                ip = '127.0.0.1'

            transport = "tcp"
            addr = "%s://%s" % (transport, ip)

            shell_port = shell_socket.bind_to_random_port(addr)
            iopub_port = iopub_socket.bind_to_random_port(addr)
            control_port = control_socket.bind_to_random_port(addr)

            hb_port = 0

            self._connection_info: dict = {
                'ip': ip,
                'shell_port': shell_port,
                'iopub_port': iopub_port,
                'control_port': control_port,
                'hb_port': hb_port,
            }
        else:
            self._logger.info("Using user's conf..")

            cn_info = self._connection_info
            transport = cn_info['transport']
            ip = cn_info['ip']
            addr = "%s://%s" % (transport, ip)

            self.shell_context = shell_socket.bind(f"{addr}:{cn_info['shell_port']}")
            self.iopub_context = iopub_socket.bind(f"{addr}:{cn_info['iopub_port']}")
            self.control_context = control_socket.bind(f"{addr}:{cn_info['control_port']}")

            hb_port = cn_info['hb_port']

            self._session.key = cn_info.pop('key').encode()

        # heartbeat doesn't share context, because it mustn't be blocked
        # by the GIL, which is accessed by libzmq when freeing zero-copy messages
        hb_ctx = zmq.Context()
        heartbeat = Heartbeat(hb_ctx, (transport, ip, hb_port))
        #self._logger.info('hb_port: %s', heartbeat.port)
        heartbeat.start()

        self._shell_socket = shell_socket
        self._control_socket = control_socket
        self._iopub_socket = iopub_socket


def init_ipython_kernel(**kwargs):
    cn_info: dict = kwargs.pop('cn_info', None)
    picbck: 'Callable[[IPyWrapper], None] | None' = kwargs.pop('post_init_callback', None)
    update_conf: 'Callable[[traitlets.config.loader.Config], None] | None' = kwargs.pop('update_conf', None)

    kernel_wrapper = IPyWrapper(**kwargs)

    kernel_wrapper._connection_info = cn_info
    kernel_wrapper._post_init_callback = picbck
    kernel_wrapper._update_conf = update_conf

    kernel_wrapper.start()
    return kernel_wrapper


ipy_conf: dict = {
    "shell_port": 12345,
    "iopub_port": 12346,
    "stdin_port": 12347,
    "control_port": 12348,
    "hb_port": 12349,
    "ip": "0.0.0.0",
    "key": "6a913be8-0e00-43d7-b0c5-1842c29d88b5",
    "transport": "tcp",
    "signature_scheme": "hmac-sha256"
}

kernel_wrapper = None


def update_conf(conf: 'traitlets.config.loader') -> None:
    # To fix autocompletion
    conf.IPCompleter.use_jedi = False

    # or also you can update it on post-init
    # ins._kernel.shell.Completer.use_jedi = False


def main():
    sn = '[IPykernel]'
    print(f'{sn} Preparing..')

    # TODO: IP test..

    kfn: str = 'ipython_kernel.json'
    file_kfp: 'str | Path' = Path(Path(__file__).parent, kfn)

    print(f'{sn} Starting..')
    try:
        # Force disable debugpy for a while..
        import ipykernel.debugger as ipydbg
        ipydbg._is_debugpy_available = False

        if platform == 'android':
            # Set to app dir near `.kivy` dir
            dir_aipyp = os_environ['IPYTHONDIR'] = os_environ['ANDROID_ARGUMENT'] + '/' + '.ipython'
            file_kfp = Path(dir_aipyp, kfn)

            mkdirs(dir_aipyp, exist_ok=True)

            del dir_aipyp

        global kernel_wrapper

        kernel_wrapper = init_ipython_kernel(
            connection_filename=str(file_kfp),
            connection_fn_with_pid=False,
            allow_remote_connections=True,
            cn_info=ipy_conf,

            update_conf=update_conf,
            # post_init_callback=update_conf,
        )

    except Exception:
        e = format_exc()
        print(f'Error occurred: `{e}`')


if __name__ == '__main__':
    main()

    from time import sleep

    while True:
        sleep(333)
