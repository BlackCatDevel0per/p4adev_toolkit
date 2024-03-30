"""Installer CLI."""

import os.path
import sys
import sysconfig
from typing import Dict, Optional, Sequence

import installer
from installer.__main__ import _get_main_parser
from installer.destinations import SchemeDictionaryDestination
from installer.sources import WheelFile
from installer.utils import get_launcher_kind

sysconfig._INSTALL_SCHEMES['android_py_bundle'] = {
    'stdlib': '{installed_base}',
    'platstdlib': '{platbase}',
    'purelib': '{base}',
    'platlib': '{platbase}',
    'include': '{installed_base}/include/python{py_version_short}{abiflags}',
    'scripts': '{base}/bin',
    'data': '{base}',
}


def _get_scheme_dict(
    distribution_name: str, prefix: Optional[str] = None
) -> Dict[str, str]:
    """Calculate the scheme dictionary for the current Python environment."""
    vars = {}
    if prefix is None:
        installed_base = sysconfig.get_config_var("base")
        assert installed_base
    else:
        vars["base"] = vars["platbase"] = installed_base = prefix

    scheme_dict = sysconfig.get_paths(scheme='android_py_bundle', vars=vars)

    # calculate 'headers' path, not currently in sysconfig - see
    # https://bugs.python.org/issue44445. This is based on what distutils does.
    # TODO: figure out original vs normalised distribution names
    scheme_dict["headers"] = os.path.join(
        sysconfig.get_path("include", scheme='android_py_bundle', vars={"installed_base": installed_base}),
        distribution_name,
    )

    # print(scheme_dict)

    return scheme_dict


def _main(cli_args: Sequence[str], program: Optional[str] = None) -> None:
    """Process arguments and perform the install."""
    parser = _get_main_parser()
    if program:
        parser.prog = program
    args = parser.parse_args(cli_args)

    bytecode_levels = args.compile_bytecode
    if args.no_compile_bytecode:
        bytecode_levels = []
    elif not bytecode_levels:
        bytecode_levels = [0, 1]

    # TODO: Add `*.tar.gz` support..

    with WheelFile.open(args.wheel) as source:
        destination = SchemeDictionaryDestination(
            scheme_dict=_get_scheme_dict(source.distribution, prefix=args.prefix),
            interpreter=sys.executable,
            script_kind=get_launcher_kind(),
            bytecode_optimization_levels=bytecode_levels,
            destdir=args.destdir,
        )

        # TODO: Do it properly..
        try:
            installer.install(source, destination, {})
        except FileExistsError:
            print('[WARN]: Looks like package already installed..')


if __name__ == "__main__":  # pragma: no cover
    _main(sys.argv[1:], "bundle_installer.py")
