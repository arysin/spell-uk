#!/bin/sh

if [ "$1" = "-r" ]; then
RU="|ется|ски|cкой|цкий|ецк|ее|ие|ии|ния|ется|ются|ющем|еющий"
shift
else
RU=""
fi

#EXCEPT="(ґ|іял|[рд]ія|тер$|ости$|[А-ЯІЇЄҐ]|магнет|хемі$RU)"
EXCEPT="([ґҐ]|іял|[рд]ія|тер$|магнет|хемі$RU|^[А-ЯІЇЄҐ])"

export LC_ALL=uk_UA.UTF-8

if [ "$1" = "-nbm" ]; then
    shift
    FILE="$1"
else
    FILE="$1"
    cat $FILE | grep -E "[а-яіїєґё][a-z]|[a-z][а-яіїєґё]" | sed -r "s/([а-яіїєґё][a-z]|[a-z][а-яіїєґё])/_\1_/g" > bad_mix.lst
fi

cat $FILE | tr '\n' '@' | sed -r "s/-@ *//g" | tr '@' '\n' |\
sed "s/[а-яіїєґ]+\.//gi" | sed -r "s/́//g" | sed -r "s/([’ʼ\`]|\\')/'/g" |\
hunspell -d uk_UA -l |\
grep -iE "^[а-щьюяїєґ'-]{4,}$" | grep -vE "^['-]|['-]$" |\
grep -vE "$EXCEPT" | sort | uniq
# uniq -c | sort -nr 
#| awk '{print $2}' 
#|sort

# hunspell does not handle long strings (>5K utf-8 chars) well - need to split
#sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" |\
