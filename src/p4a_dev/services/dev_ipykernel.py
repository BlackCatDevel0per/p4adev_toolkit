import json
import sys
from pathlib import Path

# from threading import Thread
from ipykernel import kernelapp

# from jnius import autoclass

# PythonService = autoclass('org.kivy.android.PythonService')
# PythonService.mService.setAutoRestartService(True)

def main():
    ipy_conf: dict = {
        "shell_port": 12345,
        "iopub_port": 12346,
        "stdin_port": 12347,
        "control_port": 12348,
        "hb_port": 12349,
        "ip": "127.0.0.1",
        "key": "6a913be8-0e00-43d7-b0c5-1842c29d88b5",
        "transport": "tcp",
        "signature_scheme": "hmac-sha256"
    }


    kfn = Path(Path(__file__).parent, 'ipython_kernel.json')
    with open(kfn, 'w') as kf:
        json.dump(ipy_conf, kf)

    sys.argv.append('-f')
    sys.argv.append(str(kfn))

    # app = kernelapp.IPKernelApp.instance()
    # app.initialize()
    # app.start()

    kernelapp.launch_new_instance()

if __name__ == '__main__':
    main()

# TODO: Clear sys.argv..
