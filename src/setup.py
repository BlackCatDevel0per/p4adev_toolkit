"""Crutchy~ Cythonization of app sources to avoid decompiling pyc files of yours private sources."""
# TODO: Use mypycify!

import glob
from pathlib import Path

from setuptools import Extension, setup

# TODO: Versioning..
##
SRC = 'app'

BASENAME = SRC.split('/')[-1]

# TODO: MORE TESTS ON REAL DEVICES!!!
# TODO: Skip compiling if debug..
# TODO: Do something with dir sub-packages.. (better than just __init__.py -> __init__.so)

extensions = []

for py in glob.glob(f'{SRC}/**/*.py', recursive=True):
	pyp = Path(py)
	extensions.append(
		Extension(
			'.'.join(
				[*list(pyp.parts[:-1]), pyp.parts[-1].split('.')[0]],  ##
			),
			[py],
		),
	)

# from rich import print
# print(extensions)

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

	##setup_requires=['cython<=0.29.37'],
)
