from __future__ import annotations

# from pathlib import Path

# Exclude helpers (filename, relative path, dirname)
exclude_kvs_default: tuple[str, ...] = (
	# default
	'kivymd',
	'.buildozer',
	'.venv',
	'venv',

	'__MACOS',
	'__MACOSX',
	'style.kv',
)

# Exclude helpers (filename, relative path, dirname)
exclude_kvs: tuple[str, ...] = (
	# app
	'View/main_screen/platforms/mobile/ui/main_navbar.kv',
	'View/widgets/ui',

	# default
	*exclude_kvs_default,
)

force_include_kvs: tuple[str, ...] = (
	'View/widgets/ui/override',
    'View/widgets/ui/extensions',

    'View/widgets/ui/textinput.kv',
)

unload_kvs: tuple[str, ...] = (
	# str(Path(uix_path, 'some', 'style.kv')),
)
