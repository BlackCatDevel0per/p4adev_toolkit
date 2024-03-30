export PYTHONOPTIMIZE=2
##

# Additionally use ccache because it's looks like buildozer's tools/deps doesn't fully use it in current time..
export LD=lld
export CC="ccache clang"
export CXX="ccache clang++"
export AR="ccache llvm-ar"
export AS="ccache llvm-as"
export RANLIB=llvm-ranlib

# export LD=lld
# export CC="clang"
# export CXX="clang++"
# export AR="llvm-ar"
# export AS="llvm-as"
# export RANLIB=llvm-ranlib

# export LD="ld"
# export CC="gcc"
# export CXX="g++"
# export AR="gcc-ar"
# export AS="gcc-as"
# export RANLIB=gcc-ranlib

export USE_CCACHE=1

# Buggy~ (patching fails..)
# TODO: Use prebuild & automatically copy (& mb will work..)
# export DEF_P4A_DIR=$HOME/.buildozer/cache/recipes
# mkdir -p $DEF_P4A_DIR

# recipes=(
# 	python3
# 	hostpython3
# 	kivy
# 	pyjnius
# 	android
# 	six
# 	setuptools
# 	libffi
# 	jpeg
# 	sdl2
# 	sdl2_ttf
# 	sdl2_image
# 	sdl2_mixer

# )

# for recipe in "${recipes[@]}"
# do
# 	export "P4A_${recipe}_DIR"=$DEF_P4A_DIR
# done

# TODO: Cache cleaning options
# TODO: Optionally recheck remote changes..
# TODO: Manage recipes build order..
# TODO: Exclude some packages on post-build..

# To cache clean use: `rm -rf ~/.buildozer/cache/*` or for git `rm -rf ~/.buildozer/cache/git/*` & etc.
# See cache with `tree -L 2 ~/.buildozer/cache`
export USE_GIT_CACHING=1
export USE_P4A_RECIPES_CACHING=1

# export PATH=.:$PATH
# source ./git_cache.sh

poetry run python -c "import sys, pprint; pprint.pprint(sys.path)"
# poetry run python -c "from shutil import which;print(which('git'))"

# TODO: Skip downloading by patching buildozer's a bit legacy download method..
##export PYTHONPATH=$PWD:.
# cd ..
# python -c "import sys, pprint; pprint.pprint(sys.path)"
# python -c "from urllib.request import urlopen;print(urlopen)"
# cd -

# exit

start_sound=/usr/share/sounds/freedesktop/stereo/message-new-instant.oga
complete_sound=/usr/share/sounds/freedesktop/stereo/complete.oga

ls >/dev/null 2>&1 && paplay $start_sound

# Crutchy cythonize main app lib
# NOTE: WARNING!
cd src
find . -name '*.c' -delete

poetry run python setup.py sdist
rm -rf *.egg-info dist build

cd ..

poetry run python -m buildozer -v android $1

# FIXME: Use it as option (to avoid stopping multiple builds..)
# Kill gradle daemon after build
pkill -f '.*GradleDaemon.*'

# Optionally play sound on complete
ls >/dev/null 2>&1 && paplay $complete_sound

