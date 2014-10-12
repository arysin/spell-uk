%define languagecode uk_UA

%define dictdir	%{_datadir}/dict/ooo

Summary:	MySpell spelling dictionary for Ukrainian
Name:		myspell-%{languagecode}
Version:	1.8.0
Release:	1
URL:		http://ispell-uk.sourceforge.net/
Source:		spell-uk-%{version}.tgz
License:	GPL and LGPL
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildArch:	noarch


%define is_mdk  %(test -e /etc/mandrake-release && echo 1 || echo 0)
%define is_suse  %(test -e /etc/SuSE-release && echo 1 || echo 0)
%define is_fedora %(test -e /etc/fedora-release && echo 1 || echo 0)

# default (Fedora) group
Group: Applications/Text

%if %is_mdk
# Mandriva Stuff
Group:			System/Internationalization
Requires:		locales-uk
Provides:       myspell-dictionary = %{version}
Provides:		myspell-uk = %{version}
#Autoreqprov:	no
%endif

%if %is_suse
# SUSE Stuff
Group:          Productivity/Text/Spell
Provides:       myspell-dictionary = %{version}
Provides:       ooo-dictionaries:/usr/lib/ooo-1.1/share/dict/ooo/uk_UA.dic
Provides:       locale(OpenOffice_org:uk) locale(seamonkey-spellchecker:uk)
#Autoreqprov:	on
%endif

#%else
# RedHat Stuff
#Group: Applications/Text
#%endif


%description
myspell-uk_UA package contain spell checking data for Ukrainian language to be used by
OpenOffice.org or any other myspell-capable application, like Mozilla.
#myspell-hyph-uk packages contain hyphenation dictionaries.

%prep
%setup -q -n spell-uk-%{version}

%build
make myspell

%install
rm -rf $RPM_BUILD_ROOT
make install-myspell-dict PREFIX=$RPM_BUILD_ROOT MYSPELLDIR=%{dictdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [[ ! -f "%{dictdir}/dictionary.lst" ]] || \
      ! grep -q "^DICT[ \t]*uk[ \t]*UA[ \t]*uk_UA\$" %{dictdir}/dictionary.lst
then
    echo "DICT uk UA uk_UA" >> %{dictdir}/dictionary.lst
fi

%preun
if [[ "$1" = "0" ]]; then #This is being completely erased, not upgraded
  perl -ni -e "/^DICT\s*uk\s*UA\s*uk_UA\$/ or print" %{dictdir}/dictionary.lst
fi


%files
%defattr(-,root,root)
%doc src/myspell/README_uk_UA.txt
#COPYING

%{dictdir}/uk_UA.aff
%{dictdir}/uk_UA.dic

%changelog
* Mon Dec 09 2011 22:11:52 Andriy Rysin <arysin@yahoo.com> 1.6.6
- 2K of new words
- some fixes

* Mon May 16 2011 22:11:52 Andriy Rysin <arysin@yahoo.com> 1.6.5
- 4K of new words
- some fixes

* Mon Aug 17 2009 23:11:52 Andriy Rysin <arysin@yahoo.com> 1.6.0
- 15K of new words
- many fixes

* Sat Jan 24 2009 13:00:00 Andriy Rysin <arysin@yahoo.com> 1.5.7
- 1K of new words
- some fixes

* Sun Sep 21 2008 13:00:00 Andriy Rysin <arysin@yahoo.com> 1.5.5
- 2K of new words
- some fixes

* Sun Dec 27 2007 13:00:00 Andriy Rysin <arysin@yahoo.com> 1.5.0
- 3K of new words
- some fixes
- some packaging updates

* Sun May 27 2007 13:00:00 Andriy Rysin <arysin@yahoo.com> 1.4.0
- 10K of new words
- some fixes
- myspell now has triple license: GPL, LGPL and MPL

* Sun Apr 08 2007 06:08:09 Andriy Rysin <arysin@yahoo.com> 1.3.3
- Some updates and mozilla package fixes

* Tue Jan 26 2007 9:23:00 Andriy Rysin <arysin@yahoo.com> 1.3.1
- Some packaging and filenaming fixes

* Tue Jan 26 2007 01:23:00 Andriy Rysin <arysin@yahoo.com> 1.3.0
- Release 1.3.0
- Changed versioning to 3 digits
- Added generation of mozilla xpi package
- Added recognition of grave accent (`) often used as apostrophe
- New words and fixes

* Tue Dec 19 2006 21:18:16 Andriy Rysin <arysin@yahoo.com> 1.2
- Release 1.2
- New words
- Rules and words fixes

* Sat Sep 17 2005 10:37:03 Andriy Rysin <arysin@yahoo.com> 1.1a-1
- Release 1.1a
- Integration of ispell, aspell and myspell into one source package
