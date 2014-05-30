%define keepstatic 1
Name:           libtool
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  lzma
BuildRequires:  zlib-devel
BuildRequires:	makeinfo
Requires:       automake > 1.4
Requires:       tar
Summary:        A Tool to Build Shared Libraries
License:        GPL-2.0+
Group:          Development/Tools
Version:        2.4.2
Release:        0
Requires:       libltdl = %{version}
Url:            http://www.gnu.org/software/libtool/
Source:         http://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.gz
Source2:        baselibs.conf
Source3:        libtool-rpmlintrc
Source1001: 	libtool.manifest
Provides:       libltdl-devel
# fedora name
Provides:       libtool-ltdl-devel

%description
GNU libtool is a set of shell scripts to automatically configure UNIX
architectures to build shared libraries in a generic fashion.

%package -n libltdl
Summary:        Libtool Runtime Library
Group:          System/Libraries

%description -n libltdl
Library needed by programs that use the ltdl interface of GNU libtool.

%prep
%setup -q -n libtool-%{version}
cp %{SOURCE1001} .

%build
%configure
# force rebuild with non-broken makeinfo
rm -f doc/libtool.info
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

#%post -n libltdl -p /sbin/ldconfig

#%postun -n libltdl -p /sbin/ldconfig

%files
#%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
/usr/bin/libtool
/usr/bin/libtoolize
/usr/include/libltdl
/usr/include/ltdl.h
%{_libdir}/libltdl.a
%attr(644, root, root) %{_libdir}/libltdl.la
%{_libdir}/libltdl.so
/usr/share/aclocal/*.m4
%doc %{_infodir}/libtool.info*
%doc %{_mandir}/man1/libtool.1.gz
%doc %{_mandir}/man1/libtoolize.1.gz
/usr/share/libtool

%files -n libltdl
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/libltdl.so.*

%changelog
