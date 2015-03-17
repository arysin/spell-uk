include ../../encodings.inc
reverse_verbs = ../../bin/verb_reverse.pl


affixfile = uk_affix.dat
src_affixfiles = uk.REP uk.aff.ADJ uk.aff.NOUN uk.aff.VERB uk.aff.VERB_REV uk.aff.DIEPR uk.aff.DIEPR_REV uk.aff.PREFIX

CLEANFILES = $(affixfile) uk.aff.VERB_REV

alt_suff_cmd=sed -r '/:alt/ s/^\#//' | sed -r "s/SFX l Y 54/SFX l Y 56/"

all: $(affixfile) uk_affix.tag


$(affixfile): $(src_affixfiles) Makefile
	cat $(src_affixfiles) | sed 's/[\t ]*#.*$$//g; s/	/ /g; s/ \+/ /g; /^ *$$/d' > $@

uk_affix.tag: $(src_affixfiles) Makefile
	cat $(src_affixfiles) | $(alt_suff_cmd) | grep -Ev "^#|^REP" | sed 's/	/ /g; s/ \+/ /g; /^ *$$/d' > $@

uk.aff.VERB_REV: uk.aff.VERB $(reverse_verbs)
	$(reverse_verbs) < uk.aff.VERB > uk.aff.VERB_REV

uk.aff.DIEPR_REV: uk.aff.DIEPR $(reverse_verbs)
	$(reverse_verbs) < uk.aff.DIEPR > uk.aff.DIEPR_REV

clean:
	rm -f $(CLEANFILES) 


.PHONY: all clean 
