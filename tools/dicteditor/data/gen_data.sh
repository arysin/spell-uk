#!/bin/sh
grep -E "[^a-zA-Z0]{4}/" ../../../src/Dictionary/uk_words.out | sed -r "s/^.*(....\/.).*$/\1/" | sort | uniq -c > uk_words3.stat
