%define _localstatedir %{_var}

%define major                   2
%define libname                 %mklibname prelude %{major}
%define libnamedevel            %mklibname prelude -d
%define libnamestaticdevel      %mklibname prelude -d -s

Name:           libprelude
Version:        1.0.1
Release:        1
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
BuildRequires:	autoconf automake libtool
BuildRequires:  gnutls-devel
BuildRequires:  gtk-doc
BuildRequires:	libgcrypt-devel
BuildRequires:	libtool-devel
BuildRequires:	lua5.1-devel
BuildRequires:  perl-devel
BuildRequires:	ruby
BuildRequires:	ruby-devel
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

%package -n ruby-prelude
Summary:	Ruby bindings for prelude
Group:		Development/Ruby
Requires:	%{libname} = %{version}-%{release}

%description -n ruby-prelude
Provides ruby bindings for prelude.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1 -b .lt24
%patch3 -p2 -b .gnutls3
%patch4 -p0 -b .ruby
%patch5 -p1 -b .ruby1.9

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
    --with-ruby \
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
rm -f %{buildroot}%{ruby_sitearchdir}/*.*a
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

%files -n ruby-prelude
%{ruby_sitearchdir}/*
