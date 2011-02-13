#!/bin/sh

#grep "/" uk_words.lst | sed -r -f tofsa.sed > uk_words.lst1

adj_tags=(m:v_naz m:v_rod:v_zna m:v_dav m:v_oru m:v_mis f:v_naz f:v_rod f:v_dav:v_mis f:v_zna f:v_oru n:v_naz p:v_naz p:v_rod:v_mis p:v_oru)

echo "" > www.out
for word in `grep "/V$" uk_words.lst | head -n 10`; do
  i=0
  echo "1" > www.tmp
  echo $word >> www.tmp
  word_=${word%%/*}

  echo -n "doing $word_ ..." 
  incls=`unmunch www.tmp ../../dist/myspell-uk-1.6.0/uk_UA.aff 2>> www.err`
  for pos in $incls; do
    echo $pos $word_ "adj:${adj_tags[i]}" >> www.out 
    ((i=i+1))
  done
done
