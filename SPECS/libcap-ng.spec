%{!?python_sitelib:  %global python_sitelib  %(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           libcap-ng
Version:        0.6.6
Release:        0
License:        LGPL-2.1+
Summary:        An alternate POSIX capabilities library
%define soname 0
%define rname libcap-ng
%define ext_man .gz
Url:            http://people.redhat.com/sgrubb/libcap-ng
Group:          System/Libraries
# http://people.redhat.com/sgrubb/libcap-ng/libcap-ng-%{version}.tar.gz
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source99:       libcap-ng.rpmlintrc
Source1001: 	libcap-ng.manifest
BuildRequires:  kernel-headers >= 2.6.11
BuildRequires:  libattr-devel
BuildRequires:  pkg-config
BuildRequires:  python

%description
Libcap-ng is a library that makes using posix capabilities easier

%package devel

License:        LGPL-2.1+
Summary:        Header files for libcap-ng library
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       kernel-headers >= 2.6.11
Requires:       pkgconfig

%description devel
The libcap-ng-devel package contains the files needed for developing
applications that need to use the libcap-ng library.

%package utils

License:        GPL-2.0+
Summary:        Utilities for analysing and setting file capabilities
Group:          System/Base

%description utils
The libcap-ng-utils package contains applications to analyse the
posix capabilities of all the program running on a system. It also
lets you set the file system based capabilities.

%prep
%setup -q -n %{rname}-%{version}
cp %{SOURCE1001} .

%build
%configure --disable-static --with-pic --with-python=no
make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

%files
#%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING.LIB
%attr(0755,root,root) %{_libdir}/%{rname}.so.%{soname}
%attr(0755,root,root) %{_libdir}/%{rname}.so.%{soname}.*

%files devel
#%manifest %{name}.manifest
%defattr(-,root,root,-)
%attr(0644,root,root) %{_mandir}/man3/*.3%{ext_man}
%attr(0644,root,root) %{_includedir}/cap-ng.h
%attr(0755,root,root) %{_libdir}/%{rname}.so
%attr(0644,root,root) %{_datadir}/aclocal/cap-ng.m4
%{_libdir}/pkgconfig/%{rname}.pc

%files utils
#%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%attr(0755,root,root) %{_bindir}/captest
%attr(0755,root,root) %{_bindir}/filecap
%attr(0755,root,root) %{_bindir}/netcap
%attr(0755,root,root) %{_bindir}/pscap
%attr(0644,root,root) %{_mandir}/man8/*.8%{ext_man}

%changelog
