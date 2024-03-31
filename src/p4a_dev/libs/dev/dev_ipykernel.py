from __future__ import annotations

from time import sleep
import json
from background_zmq_ipython import IPythonBackgroundKernelWrapper
from traceback import format_exc
from pathlib import Path

# TODO: Make base class for services..

# from jnius import autoclass

# PythonService = autoclass('org.kivy.android.PythonService')
# PythonService.mService.setAutoRestartService(True)


class IPyWrapper(IPythonBackgroundKernelWrapper):

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

            self._connection_info = dict(
                ip=ip,
                shell_port=shell_port, iopub_port=iopub_port, control_port=control_port, hb_port=hb_port)
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

    kernel_wrapper = IPyWrapper(**kwargs)
    
    kernel_wrapper._connection_info = cn_info
    
    kernel_wrapper.start()
    return kernel_wrapper


def main():
    sn = '[IPykernel]'
    print(f'{sn} Preparing..')

    # TODO: IP test..
    # TODO: Solve ipyk temp dirs issues..

    ipy_conf: dict = {
        "shell_port": 12345,
        "iopub_port": 12346,
        "stdin_port": 12347,
        "control_port": 12348,
        "hb_port": 12349,
        "ip": "0.0.0.0",
        #"ip": "127.0.0.1",
        "key": "6a913be8-0e00-43d7-b0c5-1842c29d88b5",
        "transport": "tcp",
        "signature_scheme": "hmac-sha256"
    }


    kfn = Path(Path(__file__).parent, 'ipython_kernel.json')

    print(f'{sn} Starting..')
    try:
        # Force disable debugpy for a while..
        import ipykernel.debugger as ipydbg
        ipydbg._is_debugpy_available = False
        
        init_ipython_kernel(
            connection_filename=str(kfn),
            connection_fn_with_pid=False,
            allow_remote_connections=True,
            cn_info=ipy_conf,
        )

        # while True:
        #     sleep(333)

    except Exception:
        e = format_exc()
        print(f'Error occurred: `{e}`')


if __name__ == '__main__':
    main()

# TODO: Clear sys.argv..

