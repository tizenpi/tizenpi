Name:           libgpg-error
Version:        1.10
Release:        0
License:        GPL-2.0+ ; LGPL-2.1+
Summary:        Library That Defines Common Error Values for All GnuPG Components
Url:            http://www.gnupg.org/
Group:          Security/Crypto Libraries
Source:         %{name}-%{version}.tar.bz2
Source1:        baselibs.conf
Source1001: 	libgpg-error.manifest
BuildRequires:  gettext-tools
BuildRequires:  libtool

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon, and possibly more in the future.

%package devel
License:        GPL-2.0+ ; LGPL-2.1+ ; MIT
Summary:        Development package for libgpg-error
Group:          Development/Libraries
Requires:       glibc-devel
Requires:       libgpg-error = %{version}

%description devel
Files needed for software development using libgpg-error.

%prep
%setup -q -n libgpg-error-%{version}
cp %{SOURCE1001} .

%build
autoreconf -fiv
%configure --disable-static --with-pic
make %{?_smp_mflags}

%install
%make_install
rm -r %{buildroot}%{_datadir}/common-lisp
%find_lang %{name}

%post  -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%lang_package


%files 
#%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING.LIB COPYING 
%{_libdir}/libgpg-error*.so.*

%files devel
#%manifest %{name}.manifest
%defattr(-,root,root)
%{_datadir}/aclocal/gpg-error.m4
%{_includedir}/*
%{_bindir}/*
%{_libdir}/libgpg-error*.so

%changelog
