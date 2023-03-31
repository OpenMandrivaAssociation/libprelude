%define major                   28
%define libname                 %mklibname prelude %{major}
%define cppmajor                12
%define libcpp                  %mklibname preludecpp %{cppmajor}
%define libnamedevel            %mklibname prelude -d

%bcond_with ruby
%bcond_with python
%bcond_with perl
%bcond_with lua
%bcond_with swig

Name:           libprelude
Version:        5.1.1
Release:        2
Summary:        Prelude SIEM Library
License:        GPLv2+
Group:          System/Libraries
URL:            https://www.prelude-siem.org/
Source0:        https://www.prelude-siem.org/pkg/src/5.1.0/%{name}-%{version}.tar.gz
# https://www.prelude-siem.org/issues/860
Patch0:         libprelude-5.1.0-ruby_vendorarchdir.patch
# https://www.prelude-siem.org/issues/862
Patch1:         libprelude-5.1.0-gnutls_priority_set_direct.patch
# https://www.prelude-siem.org/issues/863
Patch2:         libprelude-5.1.0-fsf_address.patch
# https://www.prelude-siem.org/issues/865
Patch3:         libprelude-5.1.0-fix_timegm.patch
# https://www.prelude-siem.org/issues/885
Patch4:         libprelude-5.1.0-fix_pthread_atfork.patch
# https://www.prelude-siem.org/issues/887
Patch5:         libprelude-5.1.0-fix_prelude_tests_timer.patch
Patch6:         libprelude-5.1.0-fix_awk_error.patch
Patch7:         libprelude-5.1.0-fix_py38.patch
Patch8:         libprelude-5.1.0-fix_gtkdoc_1.32.patch
Patch9:         libprelude-5.1.0-linking.patch
Patch10:        libprelude-5.1.0-fix_libprelude-error_on_gnu.patch
Patch11:        libprelude-5.1.0-disable_test-poll_on_kfreebsd.patch
Patch12:        libprelude-5.1.0-fix-test_rwlock1.patch
# https://github.com/swig/swig/issues/1689
# https://github.com/swig/swig/pull/1692
# For now, add a minimum patch to support ruby2.7
Patch13:        libprelude-5.1.1-ruby27.patch

BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  flex
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(gpg-error)
BuildRequires:  libltdl-devel
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(zlib)

%if %{with swig}
BuildRequires:  swig
%endif

%if %{with perl}
BuildRequires:  perl-devel
%endif

%if %{with python}
BuildRequires:  pkgconfig(python3)
%endif

%if %{with lua}
BuildRequires:  pkgconfig(lua) >= 5.2
%endif

%if %{with ruby}
BuildRequires:  pkgconfig(ruby)
%endif

%description
The Prelude Library is a collection of generic functions providing
communication between the Prelude SIEM suite components. It
provides a convenient interface for sending alerts to Prelude
Manager with transparent SSL, failover and replication support,
asynchronous events and timer interfaces, an abstracted
configuration API (hooking at the commandline, the configuration
line, or wide configuration, available from the Manager), and a
generic plugin API. It allows you to easily turn your favorite
security program into a Prelude sensor.

%package -n %{libname}
Summary:        Prelude SIEM Library
Group:          System/Libraries
Provides:       %{name} = %{version}-%{release}

%description -n %{libname}
The Prelude Library is a collection of generic functions providing
communication between the Prelude SIEM suite components. It
provides a convenient interface for sending alerts to Prelude
Manager with transparent SSL, failover and replication support,
asynchronous events and timer interfaces, an abstracted
configuration API (hooking at the commandline, the configuration
line, or wide configuration, available from the Manager), and a
generic plugin API. It allows you to easily turn your favorite
security program into a Prelude sensor.

%files -n %{libname}
%doc AUTHORS ChangeLog README NEWS
%license COPYING LICENSE.README HACKING.README
%{_libdir}/libprelude.so.%{major}
%{_libdir}/libprelude.so.%{major}.*

%package -n %{libcpp}
Summary:        Prelude SIEM Library
Group:          System/Libraries

%description -n %{libcpp}
The Prelude Library is a collection of generic functions providing
communication between the Prelude SIEM suite components. It
provides a convenient interface for sending alerts to Prelude
Manager with transparent SSL, failover and replication support,
asynchronous events and timer interfaces, an abstracted
configuration API (hooking at the commandline, the configuration
line, or wide configuration, available from the Manager), and a
generic plugin API. It allows you to easily turn your favorite
security program into a Prelude sensor.

%files -n %{libcpp}
%{_libdir}/libpreludecpp.so.%{cppmajor}
%{_libdir}/libpreludecpp.so.%{cppmajor}.*

%package -n %{libnamedevel}
Summary:        Libraries, includes, etc. for developing Prelude IDS sensors
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Requires:       %{libcpp} = %{version}-%{release}
Requires:       libltdl-devel
Provides:       %{name}-devel = %{version}-%{release}
Provides:       prelude-devel = %{version}-%{release}

%description -n %{libnamedevel}
Libraries, include files, etc you can use to develop Prelude IDS
sensors using the Prelude Library. The Prelude Library is a
collection of generic functions providing communication between
the Prelude SIEM suite componentst It provides a convenient
interface for sending alerts to Prelude Manager with transparent
SSL, failover and replication support, asynchronous events and
timer interfaces, an abstracted configuration API (hooking at the
commandline, the configuration line, or wide configuration,
available from the Manager), and a generic plugin API. It allows
you to easily turn your favorite security program into a Prelude
sensor.

%files -n %{libnamedevel}
%doc %{_datadir}/gtk-doc/html/libprelude/
%if %{with swig}
%{_datadir}/%{name}/swig
%endif
%{_bindir}/%{name}-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}/
%{_datadir}/aclocal/*.m4
%{_mandir}/man1/%{name}-config.1*
%{_datadir}/libprelude/swig/*

%package -n prelude-tools
Summary:        The interface for %{libname}
Group:          Networking/Other
Requires:       %{libname} = %{version}-%{release}

%description -n prelude-tools
Provides a convenient interface for sending alerts to Prelude
Manager.

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


%if %{with python}
%package -n python3-prelude
Summary:        Python 3 bindings for prelude
Group:          Development/Python
Requires:       %{libname} = %{version}-%{release}
%{?python_provide:%python_provide python3-prelude}

%description -n python3-prelude
Provides python 3 bindings for prelude.

%files -n python3-prelude
%{python3_sitearch}/*
%endif

%if %{with perl}
%package -n perl-prelude
Summary:        Perl bindings for prelude
Group:          Development/Perl
Requires:       %{libname} = %{version}-%{release}

%description -n perl-prelude
Provides perl bindings for prelude.

%files -n perl-prelude
%{perl_vendorarch}/Prelude*.pm
%{perl_vendorarch}/auto/Prelude
%endif

%if %{with ruby}
%package -n ruby-prelude
Summary:        Ruby bindings for prelude
Group:          Development/Ruby
Requires:       %{libname} = %{version}-%{release}

%description -n ruby-prelude
Provides ruby bindings for prelude.

%files -n ruby-prelude
%{ruby_sitearchdir}/*
%endif

%if %{with lua}
%package -n lua-prelude
Summary:        Lua bindings for prelude
Group:          Development/Other
Requires:       %{libname} = %{version}-%{release}
Requires:       lua

%description -n lua-prelude
Provides Lua bindings for prelude generated by SWIG.
%endif

%prep
%autosetup -p1

%build
export CFLAGS="%{optflags} -pthread"
export CXXFLAGS="$CFLAGS"
export ac_cv_prog_HAVE_CXX=yes
%configure \
    --without-included-ltdl \
    --disable-static \
    --enable-shared \
%if %{with swig}
    --with-swig \
%endif
    --without-python2 \
%if %{with python}
    --with-python3 \
%endif
    --with-perl-installdirs=vendor \
    --without-included-regex \
    --includedir=%{_includedir}/%{name}
%make_build

%install
%make_install

%{_bindir}/chrpath -d %{buildroot}%{_libdir}/*.so.*

find %{buildroot} -name '*.la' -delete

