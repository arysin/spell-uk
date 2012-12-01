#!/bin/sh

MYDIR=/usr/share/myspell/dicts
MYSPELLDIR=/usr/share/myspell
OOODIR=/usr/share/dict/ooo

[ -d $MYDIR ] && echo $MYDIR && exit 0
[ -d $MYSPELLDIR ] && echo $MYSPELLDIR && exit 0
[ -d $OOODIR ] && echo $OOODIR && exit 0

echo $OOODIR

exit 0
