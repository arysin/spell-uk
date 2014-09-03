DICT_BASE=../../src/Dictionary
AFF_BASE=../../src/Affix
DICT_SRC=$(DICT_BASE)/twisters.lst $(DICT_BASE)/verify.lst $(DICT_BASE)/rare.lst

all:    uk_invert.dic uk_invert.aff

uk_invert.aff:	$(AFF_BASE)/uk_affix.dat
	make -C $(AFF_BASE)
	cat myspell.header $(AFF_BASE)/uk_affix.dat > uk_invert.aff
	
uk_invert.dic:	$(DICT_SRC)
	cat $(DICT_SRC) | grep -v "#" | wc -l > uk_invert.dic
	cat $(DICT_SRC) | sed -r "s/ .*$$//" | sort >> uk_invert.dic
