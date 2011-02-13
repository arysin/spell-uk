%define name ispell-uk
%define version 1.6.0
%define release 1
%define sourcename spell-uk-%{version}

Name:		%{name}
Summary:	Ispell spelling dictionary for Ukrainian
Version:	%{version}
Release:	%{release}
URL:		http://ispell-uk.sourceforge.net/
Source:		%{sourcename}.tgz
License:	GPL and LGPL
Group:		System/Internationalization
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
#BuildArch:	i386 x86-64
#ExcludeArch:	ia64

Requires:	ispell >= 3.2.06
BuildRequires:	ispell >= 3.2.06
#iconv


%description
This is ukrainian dictionary for spellchecking with ispell program

%prep
%setup -q -n %{sourcename}

%build
%make ispell

%install
rm -rf $RPM_BUILD_ROOT
%make install-ispell-dict PREFIX=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root)
%doc src/ispell/README Copyright COPYING.GPL COPYING.LGPL
%{_libdir}/ispell/ukrainian.aff
%{_libdir}/ispell/ukrainian.hash

%changelog
* Mon Aug 17 2009 23:11:52 Andriy Rysin <arysin@yahoo.com> 1.6.0
- 15K of new words
- many fixes

* Sat Jan 24 2009 13:00:00 Andriy Rysin <arysin@yahoo.com> 1.5.7
- 1K of new words
- some fixes

* Sun Sep 21 2008 13:00:00 Andriy Rysin <arysin@yahoo.com> 1.5.5
- 3K of new words
- some fixes

* Sun Dec 27 2007 13:00:00 Andriy Rysin <arysin@yahoo.com> 1.5.0
- 2K of new words
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

* Sun Apr 6 2003 11:20:21 Andriy Rysin <arysin@yahoo.com>
- Release 0.7
- ~ 5000 new words, some fixes

* Thu Oct 17 2002 Andriy Rysin <arysin@yahoo.com>
- Release 0.6

* Wed Oct 16 2002 Andriy Rysin <arysin@yahoo.com>
- a lot of fixes in the affix rules
- new words

* Wed Jun 26 2002 Dmytro Kovalov <kov@tokyo.email.ne.jp>
- added generation of aspell dictionaries;
- makeconfig.sh script changed to reflect aspell addition;
- included external wordlists directory used for aspell;
- some documenation cleanup.
 
* Sun May 05 2002 Andriy Rysin <arysin@yahoo.com>
- Release 0.5

* Wed Oct 3 2001 Andriy Rysin <arysin@yahoo.com>
- some improvements
- BuildArch cannot be 'noarch' because of byte order

* Wed Sep 26 2001 Eugene Onischenko <oneugene@alphadiz.com>
- Changed BuildArch to noarch
- Add Requires:
- Add Prefix definition

#* Some time in past
#- Initial version
