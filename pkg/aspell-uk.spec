%define debug_package %{nil}
%define languagecode uk

Summary:	Ukrainian dictionaries for aspell
Name:		aspell-%{languagecode}
Version:	1.7.0
Release:	1
Epoch:		5
URL:		http://ispell-uk.sourceforge.net/
Source:		spell-uk-%{version}.tgz
License:	GPL and LGPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
#BuildArch:	noarch
#ExcludeArch:	ia64

Requires:	aspell >= 0.60
BuildRequires:	aspell >= 0.60

Provides:	spell-%{languagecode}

%define is_mdk  %(test -e /etc/mandrake-release && echo 1 || echo 0)
%define is_suse  %(test -e /etc/SuSE-release && echo 1 || echo 0)
%define is_fedora %(test -e /etc/fedora-release && echo 1 || echo 0)


Group: Applications/Text

%if %is_mdk
# Mandriva Stuff
Group:		System/Internationalization
Requires:	locales-%{languagecode}
Provides:	aspell-dictionary
#Autoreqprov:	no
%endif

%if %is_suse
# SUSE Stuff
Group:          Productivity/Text/Spell
Provides:       locale(aspell:uk)
#Autoreqprov:	on
%endif

#%elseif %is_fedora
#%else
# RedHat Stuff
#%endif


%description
This is ukrainian dictionary for spellchecking with aspell program

%prep
%setup -q -n spell-uk-%{version}

%build
export CFLAGS="$RPM_OPT_FLAGS"
make aspell

%install
rm -fr $RPM_BUILD_ROOT
make install-aspell-dict PREFIX=$RPM_BUILD_ROOT

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(644,root,root)
%doc README README.uk TODO Copyright COPYING.GPL COPYING.LGPL
#%{_datadir}/aspell/*
%{_libdir}/aspell-*/uk*
%{_libdir}/aspell-*/koi8-u-nl*

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

* Sat Sep 24 2005 10:37:03 Andriy Rysin <arysin@yahoo.com> 1.1a
- Release 1.1a
- Integration of ispell, aspell and myspell into one source package
