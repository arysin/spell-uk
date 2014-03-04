include ../../encodings.inc
include dictionaries.mk.inc


spcr	   =	tr -s ' ' '\n'
LC_ALL	   =	LC_ALL=$(LOCALE)
sort	   =	$(LC_ALL) sort

dict	   = 	$(INDICT)
dictionary =	uk_words.out

CLEANFILES =	uk_words.out *.tmp *.old *.bak


all:	uk_words.out


uk_words.out: $(dict)
	cat $(SPACED) | sed -r "s/ [^ ]+ [a-z].*$$//g" | $(LC_ALL) grep -vE '^[#[:space:]]' | $(spcr) > spaced.tmp
	cat $(TAGGED) | $(LC_ALL) grep -vE "^ *#|^ *$$" | awk -F " " '{ print $$1}' | sort -u >> spaced.tmp
	cat $(NOTSPACED) spaced.tmp | grep -vE "[-]$$" | sed -r "s/[<>]//" | $(sort) > $@
	rm -f spaced.tmp

uk_words.tag: $(dict) tags.lst
	cat $(SPACED) | grep -vE " [^ ]+ [a-z].*$$" | $(LC_ALL) grep -vE "^[#[:space:]]" | $(spcr) > spaced.tmp
	cat $(SPACED) | grep -E " [^ ]+ [a-z].*$$" | $(LC_ALL) grep -vE "^[#[:space:]]" >> spaced.tmp
	cat $(TAGGED) | $(LC_ALL) grep -vE "^ *#|^ *$$" | awk -F " " '{ if ($$2 != "" && $$3 == "") print $$1,$$1,$$2; else print $$0; }' | sort -u >> spaced.tmp
	grep "/" twisters.lst | sed -r "s/ .*$$//" | awk '{ print $$0 " :bad" }' >> spaced.tmp
	cat verify.lst >> spaced.tmp
	cat $(NOTSPACED) spaced.tmp tags.lst | sed -r "s/-$$//" | sed -r "s/^[А-ЯІЇЄҐ]{2,}$$/\0 \0 noun:nv/" | $(sort) > $@
	rm -f spaced.tmp

wc:     uk_words.out
#	echo `cat uk_words.out | wc -l` + `grep -E "W|Z|A.*B|I.*J|K.*L|M.*N|Y|X" uk_words.out | wc -l` | bc
	sed -r "s/[WZYXOP]|A.*B|I.*J|K.*L|M.*N/\n/g" uk_words.out | wc -l

sort:
	@for ff in $(SORTED) ; do \
	    (mv -f $$ff $$ff.old && \
	    $(sort) < $$ff.old | uniq > $$ff && \
	    rm -f $$ff.old) ; \
	done

# helper targets

stat:	uk_words.out
	grep "/" uk_words.out | LC_ALL=uk_UA.UTF-8 sed "s/^.*\([а-я'][а-я]\/[A-Za-z]\).*$$/\1/" | sort | uniq -c > uk_words2.stat
	$(LC_ALL) grep -E "[а-я']{4,}/" uk_words.out | $(LC_ALL) sed "s/^.*\([а-я'][а-я'][а-я]\/[A-Za-z]\).*$$/\1/" | sort | uniq -c > uk_words3.stat
	$(LC_ALL) grep -E "[а-я']{4,}/" uk_words.out | $(LC_ALL) sed "s/^.*\([а-я'][а-я'][а-я]\/[A-Za-z]\+\)$$/\1/" | sort | uniq -c > uk_words3f.stat


bad:	all
	-rm -f uk_words.bad
	-$(LC_ALL) grep -E "[EF].*[CD]|[CD].*[EF]" uk_words.out > uk_words.bad
	-$(LC_ALL) grep -E "[AB].*[IJ]|[IJ].*[AB]" uk_words.out >> uk_words.bad

dups:	all
	-rm -f uk_words.dups
	-sed "s/[/A-Z]*//gi" uk_words.out | $(LC_ALL) sort | uniq -d > uk_words.dups
	-sed "s/[/A-Z]*//gi" uk_words.out | $(LC_ALL) sed "s/[еє]/.e./ig" | $(LC_ALL) sort | uniq -d > uk_words.dups_e
	-sed "s/[/A-Z]*//gi" uk_words.out | $(LC_ALL) sed "s/[гґ]/.г./ig" | $(LC_ALL) sort | uniq -d > uk_words.dups_g
	-sed "s/[/A-Z]*//gi" uk_words.out | $(LC_ALL) sed "s/[иі]/.и./ig" | $(LC_ALL) sort | uniq -d > uk_words.dups_y

adj:	all
	-rm -f uk_words.adj
	-grep "аючий" uk_words.out > uk_words.adj


clean:
	rm -f $(CLEANFILES)

.PHONY: clean all sort
