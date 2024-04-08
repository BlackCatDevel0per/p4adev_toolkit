"""Crutchy~ Cythonization of app sources to avoid decompiling pyc files of yours private sources."""

from pathlib import Path

from setuptools import Extension, setup

# TODO: Versioning..
##
SRC = 'app'

BASENAME = SRC.split('/')[-1]

# TODO: Do it better.. (Use setuptools recursive search)
# TODO: MORE TESTS ON REAL DEVICES!!!
# TODO: Skip compiling if debug..
# TODO: Do something with dir sub-packages.. (better than just __init__.py -> __init__.so)
extensions = [
	Extension(f'{BASENAME}.entry.launch', [f'{SRC}/entry/launch.py']),
	Extension(f'{BASENAME}.View.base_screen', [f'{SRC}/View/base_screen.py']),
	Extension(f'{BASENAME}.View.screens', [f'{SRC}/View/screens.py']),

	Extension(
		f'{BASENAME}.View.main_screen.main_screen',
		[f'{SRC}/View/main_screen/main_screen.py'],
	),

	Extension(
		f'{BASENAME}.View.settings_screen.main_screen',
		[f'{SRC}/View/settings_screen/main_screen.py'],
	),

	Extension(
		f'{BASENAME}.View.main_screen.components.platforms.mobile.main_screen',
		[f'{SRC}/View/main_screen/components/platforms/mobile/main_screen.py'],
	),

	Extension(
		f'{BASENAME}.View.settings_screen.components.platforms.mobile.main_screen',
		[f'{SRC}/View/settings_screen/components/platforms/mobile/main_screen.py'],
	),

	Extension(f'{BASENAME}.utility.observer', [f'{SRC}/utility/observer.py']),

	Extension(f'{BASENAME}.libs.__init__', [f'{SRC}/libs/__init__.py']),
	Extension(f'{BASENAME}.libs.filechooser', [f'{SRC}/libs/filechooser.py']),
	Extension(f'{BASENAME}.libs.ssl_conf', [f'{SRC}/libs/ssl_conf.py']),

	Extension(f'{BASENAME}.libs.dev.__init__', [f'{SRC}/libs/dev/__init__.py']),
	Extension(f'{BASENAME}.libs.dev.dev_ipykernel', [f'{SRC}/libs/dev/dev_ipykernel.py']),

	Extension(f'{BASENAME}.Model.base_model', [f'{SRC}/Model/base_model.py']),
	Extension(f'{BASENAME}.Model.main_screen', [f'{SRC}/Model/main_screen.py']),
	Extension(f'{BASENAME}.Model.settings_screen', [f'{SRC}/Model/settings_screen.py']),

	Extension(f'{BASENAME}.Controller.main_screen', [f'{SRC}/Controller/main_screen.py']),
	Extension(f'{BASENAME}.Controller.settings_screen', [f'{SRC}/Controller/settings_screen.py']),
]

# Replace '.py' to '.c' if packaging 'c' files (code generated by Cython)
for ext in extensions:
	for i, s in enumerate(ext.sources):
		sp = Path(s)

		##
		s = f'{sp.parent}/{sp.stem}.c'
		# TODO: Make it optionally using env var..
		# You should cythonize python code to C before build this package & app
		# (sources are generated via build script..)
		if sp.exists() and not Path(s).exists():
			continue
		ext.sources[i] = s

		print('Cythonized source:', ext.sources[i])

try:
	from Cython.Build import cythonize
	# from Cython.Build import build_ext, cythonize
except ImportError:
	def cythonize(*args, **kwargs):
		return extensions


setup(
	name=BASENAME,
	ext_modules=cythonize(
		extensions,
		# exclude=[f'{SRC}/main.py'],
		compiler_directives={
			'language_level': 3,
		},
	),
	include_package_data=True,
	# package_data={'': ['*.kv']},
	packages=[
		SRC,
		# NOTE: Use source files just as entry points!
		#'app.services',  # TODO: Make it private too..
		# 'app.View.main_screen.components.platforms.mobile',  # just ignore..
	],
	#extra_compile_args=['-O3'],
	##libraries=['m'],

	# cmdclass={'build_ext': build_ext},

    # setup_requires=['cython>=0.29.37'],
)
