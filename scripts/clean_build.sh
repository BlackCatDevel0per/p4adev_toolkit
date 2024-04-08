# TODO: Mb add sleep for cancel on some accidents..?
# TODO: More options..
rm -rf bin .buildozer

MAIN_SCRIPT=$(dirname $(readlink -f $0))

source $MAIN_SCRIPT/build.sh $@

