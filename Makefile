dictdir=`aspell config dict-dir`
datadir=`aspell config data-dir`

VERSION=$(shell cat ./VERSION)

#ISPELLDIR = /usr/lib/ispell
ISPELLDIR = $(shell ispell -d stupidd 2>&1 | sed "s/^[^/]*(\/.*\/)stupidd.*$/\1/")
#MYSPELLDIR = /usr/share/dict/ooo
#MYSPELLDIR = /usr/share/myspell/dicts
MYSPELLDIR=`bin/find_myspell_dir.sh`

DIST = dist

ASPELL_DIST = $(DIST)/aspell-uk-$(VERSION)
ASPELL_DOC_DIR = /usr/share/doc/aspell-uk-$(VERSION)

ISPELL_DIST = $(DIST)/ispell-uk-$(VERSION)
ISPELL_DOC_DIR = /usr/share/doc/ispell-uk-$(VERSION)

MYSPELL_DIST = $(DIST)/myspell-uk-$(VERSION)
MYSPELL_DICT_LST = $(PREFIX)$(MYSPELLDIR)/dictionary.lst
MYSPELL_DOC_DIR = /usr/share/doc/ispell-uk_UA-$(VERSION)

XPI_DIST = $(DIST)/mozilla-xpi-uk-$(VERSION)
OXT_DIST = $(DIST)/openoffice.org-uk-$(VERSION)

UPDATE_VERSION=sed -r "s/@VERSION@/$(VERSION)/g"


#TODO: created this dirs only for particular target
$(shell mkdir -p $(ASPELL_DIST))
$(shell mkdir -p $(ISPELL_DIST))
$(shell mkdir -p $(MYSPELL_DIST))
$(shell mkdir -p $(XPI_DIST)/dictionaries)
$(shell mkdir -p $(OXT_DIST))

KOI8U_SET = src/aspell/koi8-u-nl.cset
KOI8U_MAP = src/aspell/koi8-u-nl.cmap

wordlist_src = src/Dictionary/uk_words.lst
affixfile_src = src/Affix/uk_affix.dat

CLEANFILES = uk.rws uk.cwl uk.cwl.gz uk_words.lst uk_affix.dat *.bak uk.dat
CLEANFILES += uk.aff uk.dic tmp.header
CLEANFILES += ukrainian.aff ukrainian.hash uk_words.enc uk_words.enc.cnt uk_words.enc.stat ukrainian
CLEANFILES += aspell-uk-*.tgz myspell_uk_UA-*.zip ispell-uk-*.tgz
CLEANFILES += spell*.tgz dist/*.oxt

CLEANDIRS = aspell-uk-* ispell-uk-* dist/*spell* dist/*mozilla* dist/*office*

iconv	= iconv

include encodings.inc

default:	aspell

all: 		aspell myspell mozilla-xpi ooo

packages:	aspell-rpm myspell-rpm myspell-zip mozilla-xpi ooo

install:	install-aspell

install-all:	install-aspell install-myspell

#
# aspell rules
# 
#aspell:		$(ASPELL_DIST)/uk.rws $(ASPELL_DIST)/uk_affix.dat $(ASPELL_DIST)/uk.dat uk.multi ukrainian.alias $(ASPELL_DIST)/ukrainian.kbd
aspell:		$(ASPELL_DIST)/uk.rws $(ASPELL_DIST)/uk.dat src/aspell/uk.multi src/aspell/ukrainian.alias $(ASPELL_DIST)/ukrainian.kbd
	cp -u src/aspell/uk.multi src/aspell/ukrainian.alias $(ASPELL_DIST)

$(ASPELL_DIST)/uk_repl.dat:
	cp -u src/aspell/uk_repl.dat $(ASPELL_DIST)

$(affixfile_src):
	$(MAKE) -C src/Affix

$(wordlist_src):
	$(MAKE) -C src/Dictionary


aspell-tar:	$(DIST)/aspell-uk-$(VERSION).tgz

$(DIST)/aspell-uk-$(VERSION).tgz: aspell
	mkdir -p $(ASPELL_DIST)/doc $(ASPELL_DIST)/misc
	cp -u README Copyright $(ASPELL_DIST)
	cp -u README.uk COPYING.* TODO $(ASPELL_DIST)/doc
	cp -u src/aspell/aspell.net/misc/*.txt $(ASPELL_DIST)/misc
	tar cCvfz $(DIST) --owner=root --group=root $@ aspell-uk-$(VERSION)

aspell-rpm:	srctar
	bin/make_rpm.sh aspell-uk $(VERSION)

install-aspell-dict: aspell
	install -m 0755 -d  $(PREFIX)$(datadir) $(PREFIX)$(dictdir)
	install -m 0644  $(ASPELL_DIST)/$(KOI8U_SET) $(ASPELL_DIST)/$(KOI8U_MAP) $(PREFIX)$(dictdir)
	install -m 0644  $(ASPELL_DIST)/uk.dat $(PREFIX)$(datadir)
	install -m 0644  $(ASPELL_DIST)/uk.rws $(ASPELL_DIST)/uk.multi $(ASPELL_DIST)/uk_affix.dat $(ASPELL_DIST)/ukrainian.alias $(ASPELL_DIST)/ukrainian.kbd $(PREFIX)$(dictdir)

install-aspell: install-aspell-dict
	install -m 0755 -d  $(PREFIX)$(ASPELL_DOC_DIR)
	install -m 0644	README README.uk Copyright COPYING.* TODO $(PREFIX)$(ASPELL_DOC_DIR)

# dependecies for aspell
uk.cwl:		$(wordlist_src)
	$(iconv) -f $(SOURCE_ENC) -t $(ASPELL_ENC) < $(wordlist_src) | LC_COLLATE=C sort | LC_COLLATE=C word-list-compress c > uk.cwl


uk.cwl.gz:	uk.cwl
	gzip -9 < uk.cwl > uk.cwl.gz

$(ASPELL_DIST)/uk.rws:	$(affixfile_src) $(wordlist_src) $(ASPELL_DIST)/uk_affix.dat $(ASPELL_DIST)/uk.dat $(KOI8U_SET) $(KOI8U_MAP)
	cp -u $(KOI8U_SET) $(KOI8U_MAP) $(ASPELL_DIST)
	cat $(wordlist_src) | $(iconv) -f $(SOURCE_ENC) -t $(ASPELL_ENC) | \
	    aspell --local-data-dir=$(ASPELL_DIST) --lang=uk create master ./$@

$(ASPELL_DIST)/uk_affix.dat:	$(affixfile_src) encodings.inc
	$(iconv) -f $(SOURCE_ENC) -t $(ASPELL_ENC) < $(affixfile_src) > $@

#$(ASPELL_DIST)/uk_words.lst:	$(wordlist_src) encodings.inc
#	$(iconv) -f $(SOURCE_ENC) -t $(ASPELL_ENC) < $(wordlist_src) > $@

$(ASPELL_DIST)/uk.dat:		src/aspell/uk.dat.templ encodings.inc
	sed "s/^data-encoding.*$$/data-encoding   $(ASPELL_ENC_NAME)/" < src/aspell/uk.dat.templ > $@

# *.kbd file should be always in UTF-8
$(ASPELL_DIST)/ukrainian.kbd:	src/aspell/ukrainian.kbd
	cp -u $< $@

# official aspell.net package

aspell.net:
	wget ftp://ftp.gnu.org/gnu/aspell/aspell-lang-20040810.tar.bz2
	aspell-lang-20040810/aspell-lang

#
# myspell rules
#
myspell: 	$(MYSPELL_DIST)/uk_UA.aff $(MYSPELL_DIST)/uk_UA.dic

install-myspell-dict:	myspell
	install -m 0755 -d  $(PREFIX)$(MYSPELLDIR)
	install -m 0644	$(MYSPELL_DIST)/uk_UA.aff $(MYSPELL_DIST)/uk_UA.dic $(PREFIX)$(MYSPELLDIR)

install-myspell:	install-myspell-dict
	install -m 0755 -d  $(PREFIX)$(MYSPELL_DOC_DIR)
	install -m 0644	src/myspell/README* $(PREFIX)$(MYSPELL_DOC_DIR)
	if [[ ! -f "$(MYSPELL_DICT_LST)" ]] || \
		! grep -q "^DICT[ \t]*uk[ \t]*UA[ \t]*uk_UA\$$" $(MYSPELL_DICT_LST); \
	then \
		echo "DICT uk UA uk_UA" >> $(MYSPELL_DICT_LST); \
	fi

myspell-zip:	$(DIST)/myspell-uk_UA-$(VERSION).zip

myspell-rpm:	srctar
	bin/make_rpm.sh myspell-uk $(VERSION)

$(DIST)/myspell-uk_UA-$(VERSION).zip: myspell
	rm -f $@
	zip -j $@ $(MYSPELL_DIST)/uk_UA.aff $(MYSPELL_DIST)/uk_UA.dic src/myspell/README*

# myspell dependencies
$(MYSPELL_DIST)/uk_UA.aff:	$(affixfile_src) src/myspell/myspell.header encodings.inc
	mkdir -p $(MYSPELL_DIST)
	sed s/xxENCODINGxx/UTF-8/ < src/myspell/myspell.header > tmp.header
	cat tmp.header $(affixfile_src) | $(iconv) -f $(SOURCE_ENC) -t $(MYSPELL_ENC) > $@
	-rm tmp.header

$(MYSPELL_DIST)/uk_UA.dic:	$(wordlist_src) encodings.inc
	wc -l < $(wordlist_src) > $@
	cat $(wordlist_src) | $(iconv) -f $(SOURCE_ENC) -t $(MYSPELL_ENC) >> $@

mozilla-xpi:	myspell
	mkdir -p $(XPI_DIST)/dictionaries
	cp $(MYSPELL_DIST)/uk_UA.aff $(XPI_DIST)/dictionaries/uk-UA.aff
	cp $(MYSPELL_DIST)/uk_UA.dic $(XPI_DIST)/dictionaries/uk-UA.dic
	cat src/mozilla/README_uk_UA.txt.header src/myspell/README_uk_UA.txt > $(XPI_DIST)/README_uk_UA.txt
	cp COPYING.LGPL $(XPI_DIST)/
	cp src/mozilla/*.png $(XPI_DIST)/
	$(UPDATE_VERSION) < src/mozilla/install.js > $(XPI_DIST)/install.js
	$(UPDATE_VERSION) < src/mozilla/install.rdf > $(XPI_DIST)/install.rdf
	cd $(XPI_DIST) && zip -r ../ukrainian_dictionary-$(VERSION)-mozilla.xpi * && cd ..
#	cp src/mozilla/install* $(XPI_DIST)

ooo:	myspell
	mkdir -p $(OXT_DIST)
	cp -r src/openoffice.org/* $(OXT_DIST)
	$(UPDATE_VERSION) < src/openoffice.org/description.xml > $(OXT_DIST)/description.xml
	cp $(MYSPELL_DIST)/uk_UA.aff $(OXT_DIST)/uk_UA/
	cp $(MYSPELL_DIST)/uk_UA.dic $(OXT_DIST)/uk_UA/
	cp src/myspell/README_uk_UA.txt $(OXT_DIST)/uk_UA/
	cp src/thesaurus/th_uk_UA.dat $(OXT_DIST)/uk_UA/
	bin/th_gen_idx.pl < src/thesaurus/th_uk_UA.dat > $(OXT_DIST)/uk_UA/th_uk_UA.idx
	-rm *.oxt
	cd $(OXT_DIST) && zip --exclude=\*CVS\* -r ../dict-uk_UA-$(VERSION).oxt * && cd ..

# for myspell engine (Firefox <=2, Thunderbird <=2...)
mozilla-xpi-old:	myspell
	grep -v "IGNORE" $(MYSPELL_DIST)/uk_UA.aff | sed "s/$(MYSPELL_ENC_NAME)/KOI8-U/" | iconv -f $(MYSPELL_ENC) -t koi8-u > $(XPI_DIST)/dictionaries/uk-UA.aff
	cat $(MYSPELL_DIST)/uk_UA.dic | iconv -f $(MYSPELL_ENC) -t koi8-u > $(XPI_DIST)/dictionaries/uk-UA.dic
	cat src/mozilla/old/README_uk_UA.txt.header src/myspell/README_uk_UA.txt > $(XPI_DIST)/dictionaries/README_uk_UA.txt
	cp COPYING.LGPL $(XPI_DIST)/dictionaries/
	cp src/mozilla/old/install* $(XPI_DIST)
	cd $(XPI_DIST) && zip -r ukrainian_dictionary-$(VERSION)-mozilla-old.xpi dictionaries install.* && cd ..

#
# ispell rules
#
ispell:		$(ISPELL_DIST)/ukrainian.aff $(ISPELL_DIST)/ukrainian.hash

install-ispell-dict:	ispell
	install -m 0755 -d $(PREFIX)$(ISPELLDIR)
	install -m 0644 $(ISPELL_DIST)/ukrainian.aff $(ISPELL_DIST)/ukrainian.hash $(PREFIX)$(ISPELLDIR)

install-ispell:		install-ispell-dict
	install -m 0755 -d  $(PREFIX)$(ISPELL_DOC_DIR)
	install -m 0644	src/ispell/README Copyright COPYING.* $(PREFIX)$(ISPELL_DOC_DIR)

ispell-tar:	$(DIST)/ispell-uk-$(VERSION).tgz

$(DIST)/ispell-uk-$(VERSION).tgz: ispell
	mkdir -p $(ISPELL_DIST)/doc
	cp -u src/ispell/README Copyright COPYING.* $(ISPELL_DIST)/doc
	tar cCvfz $(DIST) --owner=root --group=root $@ --exclude='*.enc*' ispell-uk-$(VERSION)

ispell-rpm:	srctar
	bin/make_rpm.sh ispell-uk $(VERSION)

# dependencies for ispell
$(ISPELL_DIST)/ukrainian.aff:	$(affixfile_src) bin/affconv.pl src/ispell/ispell.header encodings.inc
	(cat src/ispell/ispell.header && grep -v "REP" $(affixfile_src) | perl bin/affconv.pl ) | $(iconv) -f $(SOURCE_ENC) -t $(ISPELL_ENC) > $@

$(ISPELL_DIST)/uk_words.enc:	$(wordlist_src) encodings.inc
	$(iconv) -f $(SOURCE_ENC) -t $(ISPELL_ENC) < $(wordlist_src) > $@

$(ISPELL_DIST)/ukrainian.hash:	$(ISPELL_DIST)/uk_words.enc $(ISPELL_DIST)/ukrainian.aff
	buildhash $(ISPELL_DIST)/uk_words.enc $(ISPELL_DIST)/ukrainian.aff $(ISPELL_DIST)/ukrainian.hash

# wordlist rules
#
ukrainian:	$(wordlist_src) aspell
	# XXX need to sorth this somehow (and do nont use one more locale)
	iconv -f $(SOURCE_ENC) -t $(ASPELL_ENC) < $(wordlist_src) |\
		aspell expand --encoding=$(ASPELL_ENC_NAME) \
		--local-data-dir=$(ASPELL_DIST) --lang=uk | \
		tr -s ' ' '\n' | sed '/^$$/d' > $@ 

install-wordlist: ukrainian
	install -m 0755 -d $(PREFIX)/usr/share/dict
	install -m 0644 ukrainian $(PREFIX)/usr/share/dict

# common rules
#
$(affixfile_src): affix-dir
$(wordlist_src): dictionary-dir

affix-dir:
	$(MAKE) -C src/Affix

dictionary-dir:
	$(MAKE) -C src/Dictionary

# regression test
#
regtest:	aspell $(wordlist_src)
	$(MAKE) -C test regtest

regtestroll:
	$(MAKE) -C test regtestroll


srctar: clean
	tar cfz $(DIST)/spell-uk-$(VERSION).tgz --exclude=test/all* --exclude=dist/*spell* --exclude=dist/*openoffice* --exclude=dist/*.oxt --exclude=*.old --exclude=src_text --exclude=CVS --exclude=--exclude=.* *
	mkdir -p $(DIST)/spell-uk-$(VERSION)
	tar xCfz $(DIST)/spell-uk-$(VERSION) $(DIST)/spell-uk-$(VERSION).tgz
	tar cCfz $(DIST) $(DIST)/spell-uk-$(VERSION).tgz --owner=root --group=root spell-uk-$(VERSION)
	rm -rf $(DIST)/spell-uk-$(VERSION) 


# cleaning
#
clean:
	rm -f $(CLEANFILES)
	rm -rf $(CLEANDIRS)
	$(MAKE) -C src/Affix clean
	$(MAKE) -C src/Dictionary clean
	$(MAKE) -C test clean


.PHONY: all regtest regtestroll clean aspell myspell ispell 
.PHONY: install install-all install-aspell install-myspell install-myspell-dict install-ispell install-wordlist 
.PHONY: aspell-tar myspell-zip ispell-tar srctar affix-dir dictionary-dir
