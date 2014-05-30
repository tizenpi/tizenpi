Name:           keyutils
Url:            http://people.redhat.com/~dhowells/keyutils/
Summary:        Linux Key Management Utilities
License:        GPL-2.0+ ; LGPL-2.1+
Group:          System/Kernel
Version:        1.5.3
Release:        0
Source0:        http://people.redhat.com/~dhowells/keyutils/%name-%version.tar.bz2
Source1001: 	keyutils.manifest

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel can call back to user space to get a
key instantiated.

%package -n libkeyutils
Summary:        Key utilities library
Group:          System/Kernel

%description -n libkeyutils
This package provides a wrapper library for the key management facility
system calls.

%package devel
Summary:        Development package for building linux key management utilities
Group:          System/Kernel
Requires:       libkeyutils = %version
Requires:       glibc-devel

%description devel
This package provides headers and libraries for building key utilities.

%prep
%setup -q
cp %{SOURCE1001} .

%build
make %{?_smp_mflags} NO_ARLIB=1 CFLAGS="$RPM_OPT_FLAGS" CC="%__cc"

%install
make install NO_ARLIB=1 DESTDIR=$RPM_BUILD_ROOT LIBDIR=/%_lib USRLIBDIR=/usr/%_lib

%post -n libkeyutils -p /sbin/ldconfig 

%postun -n libkeyutils -p /sbin/ldconfig

%files
#%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENCE.GPL
/sbin/*
/bin/*
/usr/share/keyutils
%{_mandir}/*/*
%config(noreplace) /etc/*

%files -n libkeyutils
#%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENCE.LGPL
/%{_lib}/libkeyutils.so.*

%files devel
#%manifest %{name}.manifest
%defattr(-,root,root,-)
/usr/%{_lib}/libkeyutils.so
%{_includedir}/*
