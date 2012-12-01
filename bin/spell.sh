#!/bin/sh

SORT="count"

for i in $*
do
	case $i in
    	--sort=a)
		SORT="alpha"
		;;
    	--no-ru)
                IGNORE_RU="1"
		;;
	--no-diepr)
                IGNORE_DIEPR="|[аяую][щч](ий|ого|ому|им|а|ої|ій|ою|і|их|им|ими)"
	        ;;
	--no-ia)
                IGNORE_IA="|іял|[рд]ія|тер$|магнет|хемі"
	        ;;
    	--no-badmix)
		NO_BAD_MIX="1"
		;;
        *)
                FILE=$i
		;;
  	esac
done


if [ "$FILE" == "" ]; then
    echo "No file specified"
    echo "Usage: $0 [--sort=a] [--no-ru] [--no-diepr] [--no-ia] [--no-badmix] filename"
    exit 
fi

function sortt() {
    if [ $SORT == "alpha" ]; then
	echo "Сортуємо за абеткою" >&2
        sort | uniq
    else
	echo "Сортуємо за кількістю" >&2
        sort | uniq -c | sort -nr | awk '{print $2}'
    fi
}

function filter_ru() {
    FILE=$1
    grep -v "[-']" $FILE | hunspell -d ru_RU -G > $FILE.rus.txt
    if command -v pgrep.py 2>&1> /dev/null; then
        pgrep.py $FILE.rus.txt $FILE > $FILE.norus.txt
    elif [ -f $(basename $0)/pgrep.py ]; then
        $(basename $0)/pgrep.py $FILE.rus.txt $FILE > $FILE.norus.txt
    else
        echo "Увага: вживаємо grep для фільтрування рос. слів, може призвести до вичерпання пам'яті" >&2
        grep -vxf $FILE.rus.txt $FILE > $FILE.norus.txt
    fi
}


#BASE_IGNORE="[ґҐ]|^[А-ЯІЇЄҐ]"
BASE_IGNORE="[ґҐ]"
IGNORE="($BASE_IGNORE$IGNORE_DIEPR)"

# 

export LC_ALL=uk_UA.UTF-8

if [ "$NO_BAD_MIX" != "1" ]; then
    cat $FILE | grep -E "[а-яіїєґё][a-z]|[a-z][а-яіїєґё]" | sed -r "s/([а-яіїєґё][a-z]|[a-z][а-яіїєґё])/_\1_/g" > $FILE.bad_mix.txt
fi

cat $FILE | tr '\n' '@' | sed -r "s/-@ *//g" | tr '@' '\n' |\
sed "s/[а-яіїєґ]+\.//gi" | sed -r "s/́//g" | sed -r "s/([’ʼ‘\`]|\\')/'/g" |\
hunspell -d uk_UA -l |\
grep -iE "^[а-щьюяїєґ'-]{4,}$" | grep -vE "^['-]|['-]$" |\
grep -vE "$IGNORE" | sortt > $FILE.spelled

if [ "$IGNORE_RU" == "1" ]; then
    filter_ru $FILE.spelled
fi

# hunspell does not handle long strings (>5K utf-8 chars) well - need to split
#sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" |\
