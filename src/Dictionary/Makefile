include ../../encodings.inc
include dictionaries.mk.inc


spcr	   =	tr -s ' ' '\n'
LC_ALL	   =	LC_ALL=$(LOCALE)
sort	   =	$(LC_ALL) sort

dict	   = 	$(INDICT)
dictionary =	uk_words.out

CLEANFILES =	uk_words.out *.tmp *.old *.bak *.tag
BAD_FLAG_RE="([IJ].*[OP]|[AB].*[QR]|/[^AIKM].*0|/[^AIKM].*[OQ])"
BAD_TAGS_RE="(nontran|:[а-яіїєґ]|/.* [a-z]|[OPQR].*:perf|[W0123].*:imperf)"

all:	uk_words.out


uk_words.out: $(dict) Makefile
	cat $(SPACED) | sed -r "s/ [^ ]+ [a-z].*$$//g" | $(LC_ALL) grep -vE '^[#[:space:]]' | $(spcr) > spaced.tmp
	cat $(TAGGED) | $(LC_ALL) grep -vE "^ *#|^ *$$" | awk -F " " '{ print $$1}' | sort -u >> spaced.tmp
	cat $(NOTSPACED) spaced.tmp | grep -vE "[-]$$" | sed -r "s/[<>]//g" | $(sort) > $@
	rm -f spaced.tmp
	@(grep -E $(BAD_FLAG_RE) $@ && echo "ERROR: Bad flag combinations exist!" && /bin/false) || /bin/true

uk_words.tag: $(dict) tags.lst Makefile
	../../bin/tag/mk_tagged_wordlist.py $(dict) tags.lst twisters.lst verify.lst rare.lst | $(sort) > $@
	@(grep -E $(BAD_TAGS_RE) $@ | grep -v "imperf:perf" && echo "ERROR: Bad tags exist!" && /bin/false) || /bin/true

wc:     uk_words.out
#	echo `cat uk_words.out | wc -l` + `grep -E "W|Z|A.*B|I.*J|K.*L|M.*N|Y|X" uk_words.out | wc -l` | bc
	sed -r "s/[ZYXWOPQR]|A.*B|I.*J|K.*L|M.*N/\n/g" uk_words.out | wc -l

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
