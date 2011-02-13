#!/bin/sh

OOODIR=/usr/share/dict/ooo
MYDIR=/usr/share/myspell/dicts

[ -d $OOODIR ] && echo $OOODIR && exit 0
[ -d $MYDIR ] && echo $MYDIR && exit 0

echo $OOODIR

exit 0
