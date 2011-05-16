#!/bin/sh

EXCEPT="(ґ|іял|[рд]ія|тер$|ости$|[А-ЯІЇЄҐ]|магнет|хемі)"

export LC_ALL=uk_UA.UTF-8
sed "s/[а-яіїєґ]+\.//gi" | sed -r "s/́//g" | sed -r "s/[’\`]/'/g" |\
hunspell -d uk_UA -l |\
grep -iE "^[а-щьюяїєґ'-]{4,}$" | grep -vE "^['-]|['-]$" |\
grep -vEi "ется|ски|cкой|цкий|ецк|ее|ие|ии|ния|ется|ются|ющем|еющий" |\
grep -vE "$EXCEPT" |\
sort | uniq -c | sort -nr | awk '{print $2}'

# hunspell does not handle long strings (>5K utf-8 chars) well - need to split
sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" | sed -r "s/^.{5000}[^ ]*/\0\n/" |\
