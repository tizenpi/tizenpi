Name:           xz
Version:        5.0.3
Release:        0
License:        LGPL-2.1+ and GPL-2.0+
Summary:        A Program for Compressing Files
Url:            http://tukaani.org/lzma/
Group:          Base/Tools
Source:         http://tukaani.org/xz/%{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	xz.manifest
BuildRequires:  pkgconfig
Provides:       lzma = %{version}
Obsoletes:      lzma < %{version}

%ifarch %{arm} 
%define do_profiling 0
%endif

# avoid bootstrapping problem
%define _binary_payload w9.bzdio

%description
The xz command is a very powerful program for compressing files.

* Average compression ratio of LZMA is about 30% better than that of
   gzip, and 15% better than that of bzip2.

* Decompression speed is only little slower than that of gzip, being
   two to five times faster than bzip2.

* In fast mode, compresses faster than bzip2 with a comparable
   compression ratio.

* Achieving the best compression ratios takes four to even twelve
   times longer than with bzip2. However. this doesn't affect
   decompressing speed.

* Very similar command line interface to what gzip and bzip2 have.

%package -n liblzma
Summary:        LZMA library
Group:          System/Libraries

%description -n liblzma
Library for encoding/decoding LZMA files.

%package devel
Summary:        Development package for the LZMA library
Group:          Development/Libraries
Requires:       liblzma = %{version}
Provides:       lzma-devel = %{version}
Obsoletes:      lzma-devel < %{version}
Provides:       lzma-alpha-devel = %{version}
Obsoletes:      lzma-alpha-devel < %{version}

%description devel
This package contains the header files and libraries needed for
compiling programs using the LZMA library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if %{do_profiling}
profiledir=$(mktemp -d)
trap "rm -rf $profiledir" EXIT
export CFLAGS="%{optflags} %{cflags_profile_generate}=$profiledir"
%endif
%configure --disable-static --with-pic --docdir=%_docdir/%{name}
make %{?_smp_mflags}
%if %{do_profiling}
time make check
make clean
export CFLAGS="%{optflags} %{cflags_profile_feedback}=$profiledir"
%configure --disable-static --with-pic --docdir=%_docdir/%{name}
make %{?_smp_mflags}
%endif

#%check
#time make check

%install
%make_install
%find_lang %{name}

%post -n liblzma -p /sbin/ldconfig

%postun -n liblzma -p /sbin/ldconfig

%lang_package

%docs_package

%files
#%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING*
%_docdir/%{name}
%{_bindir}/*

%files -n liblzma
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/lib*.so.5*

%files devel
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_includedir}/*.h
%{_includedir}/lzma
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%changelog
