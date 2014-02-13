%bcond_with crosscompile

%if !%{with crosscompile}
%bcond_without perl
%bcond_without python
%endif
%bcond_with ruby

%define _localstatedir %{_var}

%define major	2
%define cppmaj	0
%define libname	%mklibname prelude %{major}
%define libcpp	%mklibname preludecpp  %{cppmaj}
%define devname	%mklibname prelude -d

Summary:        Prelude Hybrid Intrusion Detection System Library
Name:           libprelude
Version:        1.0.1
Release:        6
License:        GPLv2+
Group:          System/Libraries
Url:            http://www.prelude-ids.org/
Source0:	http://www.prelude-ids.org/download/releases/libprelude/%{name}-%{version}.tar.gz
Patch0:		libprelude-0.9.22-fix-str-fmt.patch
Patch1:		libprelude-0.9.21.3-ltdl.patch
# (blino) fix build with libtool 2.4, from OpenEmbedded git
Patch2:		fix-ltdl-hack.patch
Patch3:		libprelude-gnutls3.patch
Patch4:		libprelude-1.0.0-ruby.patch
Patch5:		libprelude-1.0.1-ruby1.9.diff
Patch6:		libprelude-1.0.1-gets-undeclared.patch

BuildRequires:  gtk-doc
BuildRequires:	swig
BuildRequires:	libtool-devel
BuildRequires:  pkgconfig(gnutls)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(zlib)
%if !%{with crosscompile}
BuildRequires:  perl-devel
BuildRequires:  pkgconfig(python)
%endif
%if %{with ruby}
BuildRequires:	ruby-devel
%endif

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

%package -n %{libcpp}
Summary:        Prelude Hybrid Intrusion Detection System Library
Group:          System/Libraries
Conflicts:	%{_lib}prelude2 < 1.0.1-4

%description -n %{libcpp}
This package contains the C++ shared library for %{name}.

%package -n %{devname}
Summary:        Libraries, includes, etc. for developing Prelude IDS sensors
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Requires:       %{libcpp} = %{version}-%{release}
Provides:       prelude-devel = %{version}-%{release}

%description -n %{devname}
This package includes the development files for %{name}.

%package -n prelude-tools
Summary:        The interface for %{libname}
Group:          Networking/Other

%description -n prelude-tools
Provides a convenient interface for sending alerts to Prelude
Manager.

%if !%{with crosscompile}
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
%endif

%if %{with ruby}
%package -n ruby-prelude
Summary:	Ruby bindings for prelude
Group:		Development/Ruby
Requires:	%{libname} = %{version}-%{release}

%description -n ruby-prelude
Provides ruby bindings for prelude.
%endif

%prep
%setup -q
%apply_patches

rm -f bindings/python/_PreludeEasy.cxx
sed -i -e "s|/lib/|/%{_lib}/|g" configure.in
autoreconf -fi

%build
%configure2_5x \
	--without-included-ltdl \
	--disable-static \
	--enable-shared \
	--with-perl-installdirs=vendor \
	--without-lua \
%if %{with python}
	--with-python \
%else
	--without-python \
%endif
%if %{with perl}
	--with-perl \
%else
	--without-perl \
%endif
%if %{with ruby}
	--with-ruby \
%endif
	--without-included-regex \
	--includedir=%{_includedir}/%{name} \
	--enable-gtk-doc \
	--with-html-dir=%{_docdir}/%{devname}

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

%if %{with ruby}
rm -f %{buildroot}%{ruby_sitearchdir}/*.*a
%endif
rm -f %{buildroot}%{_sysconfdir}/prelude/default/*.conf-dist

%multiarch_binaries %{buildroot}%{_bindir}/libprelude-config

%files -n %{libname}
%{_libdir}/libprelude.so.%{major}*

%files -n %{libcpp}
%{_libdir}/libpreludecpp.so.%{cppmaj}*

%files -n %{devname}
%doc AUTHORS ChangeLog README INSTALL
#doc #{_docdir}/%{devname}
%{multiarch_bindir}/libprelude-config
%{_bindir}/libprelude-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libprelude
%{_includedir}/libprelude/*
%{_datadir}/aclocal/*.m4

%doc AUTHORS ChangeLog README INSTALL
%{_bindir}/prelude-adduser
%{_bindir}/prelude-admin
%{_mandir}/man1/prelude-admin.1*
%dir %{_sysconfdir}/prelude
%dir %{_sysconfdir}/prelude/default
%dir %{_sysconfdir}/prelude/profile
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/prelude/default/*.conf
%dir %{_var}/spool/prelude

%if !%{with crosscompile}
%files -n python-prelude
%{_libdir}/python*/site-packages/*

%files -n perl-prelude
%{perl_vendorarch}/Prelude.pm
%{perl_vendorarch}/auto/Prelude
%{perl_vendorarch}/auto/PreludeEasy
%endif

%if %{with ruby}
%files -n ruby-prelude
%{ruby_sitearchdir}/*
%endif

