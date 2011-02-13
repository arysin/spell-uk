include ../../encodings.inc
reverse_verbs = ../../bin/verb_reverse.pl


affixfile = uk_affix.dat
src_affixfiles = uk.REP uk.aff.ADJ uk.aff.NOUN uk.aff.VERB uk.aff.VERB_REV uk.aff.PREFIX

CLEANFILES = $(affixfile) uk.aff.VERB_REV


all: $(affixfile)


$(affixfile): $(src_affixfiles)
	cat $(src_affixfiles) | sed 's/#.*$$//g; s/	/ /g; s/ \+/ /g; /^ *$$/d' > $@

uk.aff.VERB_REV: uk.aff.VERB
	$(reverse_verbs) < uk.aff.VERB > uk.aff.VERB_REV

clean:
	rm -f $(CLEANFILES) 


.PHONY: all clean 
