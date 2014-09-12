#!/bin/sh

SORT="count"
DICT="uk_UA"
LIMIT=100000

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
                IGNORE_IA="|іял|[рд]ія|тер$|хемі"
	        ;;
    	--no-badmix)
		NO_BAD_MIX="1"
		;;
    	--split-caps)
		SPLIT_CAPS="1"
		;;
    	--filter-dict=*)
		FILTER_DICT=${i:14}
		;;
	--dict=*)
	        DICT=${i:7}
	        ;;
	-*)
	        echo "Невідомий аргумент «$i»"
		echo "$0 [--sort={a,n}] [--no-ru] [--no-diepr] [--no-ia] [--no-badmix] [--split-caps] <ім’я файлу>"
		exit
		;;
        *)
                FILE=$i
		;;
  	esac
done


if [ "$FILE" == "" ]; then
    echo "No file specified"
    echo "Usage: $0 [--sort=a] [--no-ru] [--no-diepr] [--no-ia] [--no-twisters] [--no-badmix] filename"
    exit 
fi

function sortt() {
    if [ $SORT == "alpha" ]; then
	echo "Сортуємо за абеткою" >&2
        sort | uniq
    else
	echo "Сортуємо за кількістю" >&2
        sort | uniq -c | sort -nr | head -n $LIMIT | awk '{print $2}'
    fi
}

function filter_ru() {
    echo "Відфільтровуємо російські слова" >&2
    
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

function filter_1() {
    if [ "$FILTER_DICT" != "" ]; then
        echo "Відфільтровуємо слова-покручі" >&2
        tee ${FILE}.withtwisters.txt | hunspell -l -d $FILTER_DICT
    else
        cat
    fi
}


BASE_IGNORE="[ґҐ]"
IGNORE="($BASE_IGNORE$IGNORE_DIEPR)"

# 

export LC_ALL=uk_UA.UTF-8

if [ "$NO_BAD_MIX" != "1" ]; then
    echo "Генеруємо список мішанини з латиниці та кирилиці" >&2
    cat $FILE | grep -E "[а-яіїєґё][a-z]|[a-z][а-яіїєґё]" | sed -r "s/([а-яіїєґё][a-z]|[a-z][а-яіїєґё])/_\1_/g" > $FILE.bad_mix.txt
fi

echo "Перевіряємо правопис словником $DICT" >&2

cat $FILE | grep -vE "[а-яіїєґё][a-z]|[a-z][а-яіїєґё]" |\
sed "s/[а-яіїєґ]+\.//gi" | sed -r "s/́//g" | sed -r "s/([’ʼ‘\`]|\\\')/'/g" |\
hunspell -d $DICT -l |\
grep -iE "^[а-щьюяїєґ'-]{4,}$" | grep -vE "^['-]|['-]$" |\
grep -vE "$IGNORE" | filter_1 | sortt > $FILE.spelled

OUTFILE=$FILE.spelled

if [ "$IGNORE_RU" == "1" ]; then
    filter_ru $FILE.spelled
    OUTFILE=$FILE.norus.txt
fi

if [ "$SPLIT_CAPS" == "1" ]; then
    grep "^[А-ЯІЇЄҐ]" $OUTFILE > $OUTFILE.caps
    grep "^[^А-ЯІЇЄҐ]" $OUTFILE > $OUTFILE.nocaps
fi

if [ "$FILTER_DICT" != "" ]; then
    echo "Створюємо список слів-покручів" >&2
    hunspell -G -d $FILTER_DICT ${FILE}.withtwisters.txt
fi

# hunspell does not handle long strings (>5K utf-8 chars) well - need to split
#sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" |\
