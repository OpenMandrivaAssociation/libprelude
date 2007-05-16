%define major   2
%define libname %mklibname prelude %{major}

Summary:        Prelude Hybrid Intrusion Detection System Library
Name:           libprelude
Version:        0.9.14
Release:        %mkrel 1
License:        GPL
Group:          System/Libraries
URL:            http://www.prelude-ids.org/
Source0:        http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz
Source1:        http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz.sig
Source2:        http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz.md5
Source3:        http://www.prelude-ids.org/download/releases/%{name}-%{version}.txt
Patch0:         libprelude-0.9.3-spool-dir.patch
BuildRequires:  automake1.8
BuildRequires:  autoconf2.5
BuildRequires:  chrpath
BuildRequires:  gtk-doc
BuildRequires:  libgnutls-devel
BuildRequires:  zlib-devel
BuildRequires:  perl-devel
BuildRequires:  python
BuildRequires:  python-devel
%if %mdkversion >= 1020
BuildRequires:  multiarch-utils => 1.0.3
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

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
Provides:       %{name} = %{version}

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

%package -n %{libname}-devel
Summary:        Libraries, includes, etc. to develop Prelude IDS sensors
Group:          Development/C
Requires:       %{libname} = %{version}
Requires:       libltdl-devel
Provides:       libprelude-devel = %{version}
Provides:       %{_lib}prelude-devel = %{version}
Provides:       prelude-devel = %{version}
Conflicts:      %{mklibname prelude 0}-devel

%description -n %{libname}-devel
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
Requires:       %{libname} = %{version}

%description -n prelude-tools
Provides a convenient interface for sending alerts to Prelude
Manager.

%package -n python-prelude
Summary:        Python bindings for prelude
Group:          Development/Python
Requires:       %{libname} = %{version}

%description -n python-prelude
Provides python bindings for prelude.

%package -n perl-prelude
Summary:        Perl bindings for prelude
Group:          Development/Perl
Requires:       %{libname} = %{version}

%description -n perl-prelude
Provides perl bindings for prelude.

%prep
%setup -q
%patch0 -p0
%{__perl} -pi -e "s|/lib/|/%{_lib}/|g" configure.in

%build
%{__rm} -f configure
%{__libtoolize} --copy --force; aclocal-1.8 -I m4 -I libmissing/m4; automake-1.8 --add-missing --copy --foreign; autoconf

%{configure2_5x} \
    --enable-static \
    --enable-shared \
    --with-perl-installdirs=vendor \
    --enable-python \
    --without-included-regex \
    --includedir=%{_includedir}/%{name} \
    --enable-gtk-doc \
    --with-html-dir=%{_datadir}/doc/%{name}-devel-%{version}

%{__make}

%install
%{__rm} -rf %{buildroot}

%{makeinstall_std}
%{makeinstall_std} -C bindings/perl

%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libprelude.so.*.*.*

%if %mdkversion >= 1020
%multiarch_binaries %{buildroot}%{_bindir}/libprelude-config
%endif

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc %{_datadir}/doc/%{name}-devel-%{version}
%if %mdkversion >= 1020
%{multiarch_bindir}/libprelude-config
%endif
%{_bindir}/libprelude-config
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/*.a
%dir %{_includedir}/libprelude
%{_includedir}/libprelude/*.h
%{_datadir}/aclocal/*.m4

%files -n prelude-tools
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL
%dir %{_sysconfdir}/prelude
%dir %{_sysconfdir}/prelude/default
%dir %{_sysconfdir}/prelude/profile
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/prelude/default/*.conf
%{_bindir}/prelude-adduser
%dir /var/spool/prelude

%files -n python-prelude
%defattr(-,root,root)
%{_libdir}/python*/site-packages/*

%files -n perl-prelude
%defattr(-,root,root)
%{perl_vendorlib}/*/auto/Prelude/Prelude.so
%{perl_vendorlib}/*/Prelude.pm


