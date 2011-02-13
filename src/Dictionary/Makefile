include ../../encodings.inc
include dictionaries.mk.inc


spcr	   =	tr -s ' ' '\n'
LC_ALL	   =	LC_ALL=$(LOCALE)
sort	   =	$(LC_ALL) sort

dict	   = 	$(INDICT)
dictionary =	uk_words.lst

CLEANFILES =	uk_words.lst *.tmp *.old *.bak


all:	uk_words.lst


uk_words.lst: $(dict)
	cat $(SPACED) | $(LC_ALL) grep -vE "^[#[:space:]]" | $(spcr) > spaced.tmp
	cat $(NOTSPACED) spaced.tmp | $(sort) > $@
	rm -f spaced.tmp


sort:
	@for ff in $(SORTED) ; do \
	    (mv -f $$ff $$ff.old && \
	    $(sort) < $$ff.old | uniq > $$ff && \
	    rm -f $$ff.old) ; \
	done

# helper targets

stat:	uk_words.lst
	grep "/" uk_words.lst | LC_ALL=uk_UA.UTF-8 sed "s/^.*\([а-я'][а-я]\/[A-Za-z]\).*$$/\1/" | sort | uniq -c > uk_words2.stat
	$(LC_ALL) grep -E "[а-я']{4,}/" uk_words.lst | $(LC_ALL) sed "s/^.*\([а-я'][а-я'][а-я]\/[A-Za-z]\).*$$/\1/" | sort | uniq -c > uk_words3.stat
	$(LC_ALL) grep -E "[а-я']{4,}/" uk_words.lst | $(LC_ALL) sed "s/^.*\([а-я'][а-я'][а-я]\/[A-Za-z]\+\)$$/\1/" | sort | uniq -c > uk_words3f.stat


bad:	all
	-rm -f uk_words.bad
	-$(LC_ALL) grep -E "[EF].*[CD]|[CD].*[EF]" uk_words.lst > uk_words.bad
	-$(LC_ALL) grep -E "[AB].*[IJ]|[IJ].*[AB]" uk_words.lst >> uk_words.bad

dups:	all
	-rm -f uk_words.dups
	-sed "s/[/A-Z]*//gi" uk_words.lst | $(LC_ALL) sort | uniq -d > uk_words.dups
	-sed "s/[/A-Z]*//gi" uk_words.lst | $(LC_ALL) sed "s/[еє]/.e./ig" | $(LC_ALL) sort | uniq -d > uk_words.dups_e
	-sed "s/[/A-Z]*//gi" uk_words.lst | $(LC_ALL) sed "s/[гґ]/.г./ig" | $(LC_ALL) sort | uniq -d > uk_words.dups_g
	-sed "s/[/A-Z]*//gi" uk_words.lst | $(LC_ALL) sed "s/[иі]/.и./ig" | $(LC_ALL) sort | uniq -d > uk_words.dups_y

adj:	all
	-rm -f uk_words.adj
	-grep "аючий" uk_words.lst > uk_words.adj


clean:
	rm -f $(CLEANFILES)

.PHONY: clean all sort
