%define with_ruby 0

%define _localstatedir %{_var}

%define major                   2
%define libname                 %mklibname prelude %{major}
%define libnamedevel            %mklibname prelude -d
%define libnamestaticdevel      %mklibname prelude -d -s

Name:           libprelude
Version:        1.0.1
Release:        2
Summary:        Prelude Hybrid Intrusion Detection System Library
License:        GPLv2+
Group:          System/Libraries
URL:            http://www.prelude-ids.org/
Source0:	http://www.prelude-ids.org/download/releases/libprelude/%{name}-%{version}.tar.gz
Patch0:		libprelude-0.9.22-fix-str-fmt.patch
Patch1:		libprelude-0.9.21.3-ltdl.patch
# (blino) fix build with libtool 2.4, from OpenEmbedded git
Patch2:		fix-ltdl-hack.patch
Patch3:		libprelude-gnutls3.patch
Patch4:		libprelude-1.0.0-ruby.patch
Patch5:		libprelude-1.0.1-ruby1.9.diff
Patch6:		libprelude-1.0.1-gets-undeclared.patch
BuildRequires:	autoconf automake libtool
BuildRequires:  gnutls-devel
BuildRequires:  gtk-doc
BuildRequires:	libgcrypt-devel
BuildRequires:	libtool-devel
#BuildRequires:	lua5.1-devel
BuildRequires:  perl-devel
%if %{with_ruby}
BuildRequires:	ruby ruby-devel
%endif
BuildRequires:	swig
BuildRequires:  zlib-devel

%description
The Prelude Library is a collection of generic functions providing
communication between the Prelude Hybrid IDS suite components. It
provides a convenient interface for sending alerts to Prelude
Manager with transparent SSL, failover and replication support,
asynchronous events and timer interfaces, an abstracted
configuration API (hooking at the commandline, the configuration
line, or wide configuration, available from the Manager), and a
generic plugin API. It allows you to easily turn your favorite
security program into a Prelude sensor.

%package -n %{libname}
Summary:        Prelude Hybrid Intrusion Detection System Library
Group:          System/Libraries
Provides:       %{name} = %{version}-%{release}

%description -n %{libname}
The Prelude Library is a collection of generic functions providing
communication between the Prelude Hybrid IDS suite components. It
provides a convenient interface for sending alerts to Prelude
Manager with transparent SSL, failover and replication support,
asynchronous events and timer interfaces, an abstracted
configuration API (hooking at the commandline, the configuration
line, or wide configuration, available from the Manager), and a
generic plugin API. It allows you to easily turn your favorite
security program into a Prelude sensor.

%package -n %{libnamedevel}
Summary:        Libraries, includes, etc. for developing Prelude IDS sensors
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Requires:       libtool-devel
Provides:       prelude-devel = %{version}-%{release}
Obsoletes:      %{libname}-devel < %{version}-%{release}

%description -n %{libnamedevel}
Libraries, include files, etc you can use to develop Prelude IDS
sensors using the Prelude Library. The Prelude Library is a
collection of generic functions providing communication between
the Prelude Hybrid IDS suite componentst It provides a convenient
interface for sending alerts to Prelude Manager with transparent
SSL, failover and replication support, asynchronous events and
timer interfaces, an abstracted configuration API (hooking at the
commandline, the configuration line, or wide configuration,
available from the Manager), and a generic plugin API. It allows
you to easily turn your favorite security program into a Prelude
sensor.

%package -n %{libnamestaticdevel}
Summary:        Static libraries for developing Prelude IDS sensors
Group:          Development/C
Requires:       %{libnamedevel} = %{version}-%{release}
Requires:       libtool-devel
Provides:       prelude-static-devel = %{version}-%{release}
Obsoletes:      %{libname}-static-devel < %{version}-%{release}

%description -n %{libnamestaticdevel}
Libraries, include files, etc you can use to develop Prelude IDS
sensors using the Prelude Library. The Prelude Library is a
collection of generic functions providing communication between
the Prelude Hybrid IDS suite componentst It provides a convenient
interface for sending alerts to Prelude Manager with transparent
SSL, failover and replication support, asynchronous events and
timer interfaces, an abstracted configuration API (hooking at the
commandline, the configuration line, or wide configuration,
available from the Manager), and a generic plugin API. It allows
you to easily turn your favorite security program into a Prelude
sensor.

%package -n prelude-tools
Summary:        The interface for %{libname}
Group:          Networking/Other
Requires:       %{libname} = %{version}-%{release}

%description -n prelude-tools
Provides a convenient interface for sending alerts to Prelude
Manager.

%package -n python-prelude
Summary:        Python bindings for prelude
Group:          Development/Python
Requires:       %{libname} = %{version}-%{release}
%py_requires -d

%description -n python-prelude
Provides python bindings for prelude.

%package -n perl-prelude
Summary:        Perl bindings for prelude
Group:          Development/Perl
Requires:       %{libname} = %{version}-%{release}

%description -n perl-prelude
Provides perl bindings for prelude.

%if %{with_ruby}
%package -n ruby-prelude
Summary:	Ruby bindings for prelude
Group:		Development/Ruby
Requires:	%{libname} = %{version}-%{release}

%description -n ruby-prelude
Provides ruby bindings for prelude.
%endif

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1 -b .lt24
%patch3 -p2 -b .gnutls3
%patch4 -p0 -b .ruby
%patch5 -p1 -b .ruby1.9
%patch6 -p1 -b .gets

rm -f bindings/python/_PreludeEasy.cxx
%{__perl} -pi -e "s|/lib/|/%{_lib}/|g" configure.in

%build
#libtoolize --copy --force --install --ltdl
autoreconf -fi

%configure2_5x \
    --without-included-ltdl \
    --enable-static \
    --enable-shared \
    --with-perl-installdirs=vendor \
    --with-python \
    --without-lua \
%if %{with_ruby}
    --with-ruby \
%endif
    --without-included-regex \
    --includedir=%{_includedir}/%{name} \
    --enable-gtk-doc \
    --with-html-dir=%{_docdir}/%{libnamedevel}

# removing rpath
sed -i.rpath -e 's|LD_RUN_PATH=""||' bindings/Makefile.in
sed -i.rpath -e 's|^sys_lib_dlsearch_path_spec="/lib /usr/lib|sys_lib_dlsearch_path_spec="/%{_lib} %{_libdir}|' libtool

%make

(
cd bindings/perl
perl Makefile.PL INSTALLDIRS=vendor
make
)

%install

%makeinstall_std

%makeinstall_std -C bindings/perl

rm -f %{buildroot}%{_libdir}/*.la
%if %{with_ruby}
rm -f %{buildroot}%{ruby_sitearchdir}/*.*a
%endif
rm -f %{buildroot}%{_sysconfdir}/prelude/default/*.conf-dist

%multiarch_binaries %{buildroot}%{_bindir}/libprelude-config

%files -n %{libname}
%doc AUTHORS ChangeLog README INSTALL
%{_libdir}/lib*.so.*

%files -n %{libnamedevel}
%doc %{_docdir}/%{libnamedevel}
%{multiarch_bindir}/libprelude-config
%{_bindir}/libprelude-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libprelude
%{_includedir}/libprelude/*
%{_datadir}/aclocal/*.m4

%files -n %{libnamestaticdevel}
%{_libdir}/*.a

%files -n prelude-tools
%doc AUTHORS ChangeLog README INSTALL
%{_bindir}/prelude-adduser
%{_bindir}/prelude-admin
%{_mandir}/man1/prelude-admin.1*
%dir %{_sysconfdir}/prelude
%dir %{_sysconfdir}/prelude/default
%dir %{_sysconfdir}/prelude/profile
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/prelude/default/*.conf
%dir %{_var}/spool/prelude

%files -n python-prelude
%{_libdir}/python*/site-packages/*

%files -n perl-prelude
%{perl_vendorarch}/Prelude.pm
%{perl_vendorarch}/auto/Prelude
%{perl_vendorarch}/auto/PreludeEasy

%if %{with_ruby}
%files -n ruby-prelude
%{ruby_sitearchdir}/*
%endif


%changelog
* Fri Apr 29 2011 Funda Wang <fwang@mandriva.org> 1.0.0-5mdv2011.0
+ Revision: 660670
- update file list
- fix build with latest gcc and libtool

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Mon Nov 01 2010 Funda Wang <fwang@mandriva.org> 1.0.0-4mdv2011.0
+ Revision: 591299
- rebuild for py 2.7

* Sun Aug 01 2010 Funda Wang <fwang@mandriva.org> 1.0.0-3mdv2011.0
+ Revision: 564324
- rebuild for perl 5.12.1
- rebuild

* Sun Apr 25 2010 Funda Wang <fwang@mandriva.org> 1.0.0-1mdv2010.1
+ Revision: 538616
- new version 1.0.0

* Tue Jan 19 2010 Frederik Himpe <fhimpe@mandriva.org> 0.9.25-1mdv2010.1
+ Revision: 493821
- update to new version 0.9.25

* Mon Nov 23 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.24.1-3mdv2010.1
+ Revision: 469376
- second try...

* Wed Nov 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.24.1-2mdv2010.1
+ Revision: 467243
- really link against system libltdl.so.7

* Fri Aug 14 2009 Frederik Himpe <fhimpe@mandriva.org> 0.9.24.1-1mdv2010.0
+ Revision: 416395
- update to new version 0.9.24.1

* Tue Jun 09 2009 Frederik Himpe <fhimpe@mandriva.org> 0.9.23-1mdv2010.0
+ Revision: 384504
- Update to new version 0.9.23

* Wed May 20 2009 Funda Wang <fwang@mandriva.org> 0.9.22-1mdv2010.0
+ Revision: 377921
- New version 0.9.22

* Sat Dec 27 2008 Funda Wang <fwang@mandriva.org> 0.9.21.3-1mdv2009.1
+ Revision: 319833
- fix ltdl path
- BR libltdl-devel
- New version 0.9.21.3

* Sat Dec 27 2008 Funda Wang <fwang@mandriva.org> 0.9.21.2-3mdv2009.1
+ Revision: 319730
- fix str fmt
- rebuild for new python

* Tue Dec 02 2008 Götz Waschk <waschk@mandriva.org> 0.9.21.2-2mdv2009.1
+ Revision: 309159
- rebuild to get rid of libtasn1 dep

* Fri Oct 17 2008 Funda Wang <fwang@mandriva.org> 0.9.21.2-1mdv2009.1
+ Revision: 294711
- New version 0.9.21.2

* Sun Oct 12 2008 Funda Wang <fwang@mandriva.org> 0.9.21.1-1mdv2009.1
+ Revision: 292854
- install to vendor
- perl-bindings are now installed in a different way
- no need to install perl bindings seperatedly
- New version 0.9.20.1

* Sat Sep 06 2008 Funda Wang <fwang@mandriva.org> 0.9.20.1-1mdv2009.0
+ Revision: 281996
- New version 0.9.20.1

* Wed Aug 06 2008 Funda Wang <fwang@mandriva.org> 0.9.19-1mdv2009.0
+ Revision: 264167
- fix file list
- new version 0.9.19

* Fri Jul 25 2008 Funda Wang <fwang@mandriva.org> 0.9.18.1-1mdv2009.0
+ Revision: 249446
- New version 0.9.18.1

* Fri Jul 18 2008 Funda Wang <fwang@mandriva.org> 0.9.18-1mdv2009.0
+ Revision: 238344
- New version 0.9.18

* Fri Jul 18 2008 Funda Wang <fwang@mandriva.org> 0.9.17.2-1mdv2009.0
+ Revision: 238146
- New version 0.9.17.2

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Apr 29 2008 David Walluck <walluck@mandriva.org> 0.9.17-1mdv2009.0
+ Revision: 199117
- 0.9.17

* Fri Jan 25 2008 David Walluck <walluck@mandriva.org> 0.9.16.2-2mdv2008.1
+ Revision: 157831
- rebuild
- 0.9.16.2

* Mon Jan 21 2008 Thierry Vignaud <tv@mandriva.org> 0.9.16.1-3mdv2008.1
+ Revision: 155662
- rebuild for new perl

* Mon Jan 21 2008 Funda Wang <fwang@mandriva.org> 0.9.16.1-2mdv2008.1
+ Revision: 155600
- rebuild against latest gnutls

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Nov 24 2007 David Walluck <walluck@mandriva.org> 0.9.16.1-1mdv2008.1
+ Revision: 111738
- 0.9.16.1

* Thu Oct 11 2007 David Walluck <walluck@mandriva.org> 0.9.16-1mdv2008.1
+ Revision: 97055
- 0.9.16

* Wed Sep 05 2007 David Walluck <walluck@mandriva.org> 0.9.15.2-1mdv2008.0
+ Revision: 80324
- 0.9.15.2

* Thu Aug 23 2007 David Walluck <walluck@mandriva.org> 0.9.15-1mdv2008.0
+ Revision: 70678
- 0.9.15
- remove incorrect Conflicts

  + Funda Wang <fwang@mandriva.org>
    - Drop BR libnetfilter
      Use py_requires macro
    - BR libnetfilter_queue

* Tue Aug 21 2007 Funda Wang <fwang@mandriva.org> 0.9.14-3mdv2008.0
+ Revision: 68212
- Obsoletes old devel name

* Mon Aug 20 2007 David Walluck <walluck@mandriva.org> 0.9.14-2mdv2008.0
+ Revision: 68082
- new lib policy
- add static lib package
- regenerate configure in %%prep
- more strict directory permissions
- change html-dir (still not ideal)

* Wed May 16 2007 David Walluck <walluck@mandriva.org> 0.9.14-1mdv2008.0
+ Revision: 27203
- 0.9.14


* Sat Mar 31 2007 David Walluck <walluck@mandriva.org> 0.9.13.2-1mdv2007.1
+ Revision: 150126
- 0.9.13.2
- 0.9.13.1

* Tue Feb 20 2007 David Walluck <walluck@mandriva.org> 0.9.13-1mdv2007.1
+ Revision: 123167
- add libprelude-0.9.13.txt
- 0.9.13

* Fri Feb 09 2007 David Walluck <walluck@mandriva.org> 0.9.12.2-1mdv2007.1
+ Revision: 118277
- 0.9.12.2

* Sun Jan 07 2007 David Walluck <walluck@mandriva.org> 0.9.12.1-1mdv2007.1
+ Revision: 105097
- 0.9.12.1

* Thu Dec 21 2006 David Walluck <walluck@mandriva.org> 0.9.12-1mdv2007.1
+ Revision: 100905
- 0.9.12

* Thu Oct 19 2006 David Walluck <walluck@mandriva.org> 0.9.11-3mdv2007.0
+ Revision: 71045
- fix build
- remove onceonly patch (fixed upstream)
- 0.9.11
- Import libprelude

* Fri Jul 14 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.10-1mdv2007.0
- 0.9.10 (Major feature enhancements)
- added P2 (missing m4 macros)

* Wed Jun 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.9-1mdv2007.0
- 0.9.9 (Major bugfixes)

* Mon May 15 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.8-2mdk
- make it build on 2006

* Mon May 15 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.8-1mdk
- 0.9.8
- force INSTALLDIRS=vendor (P1)

* Wed Mar 22 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.7.1-1mdk
- 0.9.7.1 (Major bugfixes)

* Thu Mar 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.7-1mdk
- 0.9.7 (Major bugfixes)

* Mon Mar 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.6.1-1mdk
- 0.9.6.1

* Thu Mar 02 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.6-1mdk
- 0.9.6 (Major bugfixes)

* Mon Feb 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.5-1mdk
- 0.9.5 (Minor bugfixes)

* Mon Jan 30 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.4-1mdk
- 0.9.4 (Minor bugfixes)

* Wed Jan 11 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-4mdk
- fix deps

* Tue Jan 10 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-3mdk
- use conflicts instead of obsoletes for the devel sub package (fcrozat)

* Tue Jan 10 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-2mdk
- fix deps

* Tue Jan 10 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.3-1mdk
- 0.9.3
- fix spool dir location (P0)
- added the python and perl sub packages
- fix deps

* Sat Jan 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-1mdk
- 0.9.2

* Thu Dec 29 2005 Oden Eriksson <oeriksson@mandriva.com> 0.9.1-1mdk
- 0.9.1

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 0.8.10-3mdk
- rebuilt against openssl-0.9.8a

* Tue Jan 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.10-2mdk
- fix conflicting declaration with MySQL-4.1.x
- fix deps and conditional %%multiarch
- lib64 fixes

* Thu Apr 22 2004 Laurent Culioli <laurent@mandrake.org> 0.8.10-1mdk
- 0.8.10

