%define _localstatedir %{_var}

%define major                   2
%define libname                 %mklibname prelude %{major}
%define libnamedevel            %mklibname prelude -d
%define libnamestaticdevel      %mklibname prelude -d -s

Name:           libprelude
Version:        0.9.21.3
Release:        %mkrel 1
Summary:        Prelude Hybrid Intrusion Detection System Library
License:        GPLv2+
Group:          System/Libraries
URL:            http://www.prelude-ids.org/
Source0:	http://www.prelude-ids.org/download/releases/libprelude/%{name}-%{version}.tar.gz
Source1:        http://www.prelude-ids.org/download/releases/libprelude/%{name}-%{version}.tar.gz.sig
Source2:        http://www.prelude-ids.org/download/releases/libprelude/%{name}-%{version}.tar.gz.md5
Source3:        http://www.prelude-ids.org/download/releases/libprelude/%{name}-%{version}.txt
Patch0:		libprelude-0.9.21.2-fix-str-fmt.patch 
BuildRequires:  chrpath
BuildRequires:  gtk-doc
BuildRequires:  libgnutls-devel
BuildRequires:  zlib-devel
BuildRequires:  perl-devel
BuildRequires:	libltdl-devel
%if %mdkversion >= 1020
BuildRequires:  multiarch-utils
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
Requires:       libltdl-devel
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
Requires:       libltdl-devel
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

%prep
%setup -q
%patch0 -p0
%{__perl} -pi -e "s|/lib/|/%{_lib}/|g" configure.in
%{__autoconf}

%build
%{configure2_5x} \
    --enable-static \
    --enable-shared \
    --with-perl-installdirs=vendor \
    --enable-python \
    --without-included-regex \
    --includedir=%{_includedir}/%{name} \
    --enable-gtk-doc \
    --with-html-dir=%{_docdir}/%{libnamedevel}
%{make}

(
cd bindings/perl
perl Makefile.PL INSTALLDIRS=vendor
make
)

%install
%{__rm} -rf %{buildroot}

%{makeinstall_std}

%{makeinstall_std} -C bindings/perl

%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libprelude.so.*.*.*

%if %mdkversion >= 1020
%multiarch_binaries %{buildroot}%{_bindir}/libprelude-config
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
%{__rm} -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog README INSTALL
%{_libdir}/lib*.so.*

%files -n %{libnamedevel}
%defattr(-,root,root,0755)
%doc %{_docdir}/%{libnamedevel}
%if %mdkversion >= 1020
%{multiarch_bindir}/libprelude-config
%endif
%{_bindir}/libprelude-config
%{_libdir}/*.so
%{_libdir}/*.la
%dir %{_includedir}/libprelude
%{_includedir}/libprelude/*.h
%{_datadir}/aclocal/*.m4

%files -n %{libnamestaticdevel}
%defattr(-,root,root,0755)
%{_libdir}/*.a

%files -n prelude-tools
%defattr(-,root,root,0755)
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
%defattr(-,root,root,0755)
%{_libdir}/python*/site-packages/*

%files -n perl-prelude
%defattr(-,root,root,0755)
%{perl_vendorarch}/Prelude.pm
%{perl_vendorarch}/auto/Prelude
%{perl_vendorarch}/PreludeEasy.pm
%{perl_vendorarch}/auto/PreludeEasy
