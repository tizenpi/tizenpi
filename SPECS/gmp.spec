%define keepstatic 1
Name:           gmp
Version:        5.1.3
Release:        0
License:        GPL-3.0+ ; LGPL-3.0+
Summary:        The GNU MP Library
Url:            http://gmplib.org/
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	gmp.manifest
BuildRequires:  gcc-c++
BuildRequires:  pkg-config

%description
A library for calculating huge numbers (integer and floating point).

%package -n libgmp
Summary:        Shared library for the GNU MP Library
Group:          System/Libraries

%description -n libgmp
Shared library for the GNU MP Library.

%package -n libgmpxx
Summary:        C++ bindings for the GNU MP Library
Group:          System/Libraries
Requires:       libgmp = %{version}

%description -n libgmpxx
C++ bindings for the GNU MP Library.

%package devel
Summary:        Include Files and Libraries for Development with the GNU MP Library
Group:          Development/Languages/C and C++
Requires:       libgmp = %{version}
Requires:       libgmpxx = %{version}

%description devel
These libraries are needed to develop programs which calculate with
huge numbers (integer and floating point).

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="%{optflags} -fexceptions";
%reconfigure \
         --enable-mpbsd --enable-cxx
make %{?_smp_mflags}

%check
# do not disable "make check", FIX THE BUGS!
make check

%install
%make_install

%post -n libgmp -p /sbin/ldconfig

%post -n libgmpxx -p /sbin/ldconfig

%postun -n libgmp -p /sbin/ldconfig

%postun -n libgmpxx -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%doc AUTHORS README NEWS

%files -n libgmp
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libgmp.so.10*

%files -n libgmpxx
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libgmpxx.so.4*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%doc AUTHORS README NEWS
%doc %{_infodir}/gmp.info*.gz
%{_libdir}/libgmp.a
%{_libdir}/libgmpxx.a
%{_libdir}/libgmp.so
%{_libdir}/libgmpxx.so
%{_libdir}/pkgconfig/gmp.pc
/usr/include/gmp.h
/usr/include/gmpxx.h
