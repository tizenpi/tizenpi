Name:           bzip2
Version:        1.0.6
Release:        0
Provides:       bzip
Obsoletes:      bzip
BuildRequires:  libtool
BuildRequires:  pkg-config
Url:            http://www.bzip.org/
Summary:        A Program for Compressing Files
License:        BSD-3-Clause
Group:          Base/Tools
Source:         bzip2-%{version}.tar.gz
Source1:        bznew.gz
Source2:        bznew.1.gz
Source3:        baselibs.conf
Source100:      rpmlintrc
Source1001: 	bzip2.manifest

%description
The bzip2 program is a very powerful program for compressing files.


%package -n libbz2
Summary:        The bzip2 runtime library
Group:          System/Libraries
Provides:       bzip2-libs

%description -n libbz2
The bzip2 runtime library

%package devel
Summary:        The bzip2 runtime library development files
Group:          Development/Libraries
Requires:       libbz2 = %{version} glibc-devel

%description devel
The bzip2 runtime library development files.

%prep
%setup -q
cp %{SOURCE1001} .

%build
profile_bzip2()
{
    tmpfile=$(mktemp)
    trap "rm -f $tmpfile $tmpfile.bz2" EXIT
    tar -cjf $tmpfile.bz2 /usr/src || true
   # time ./bzip2 $tmpfile
    time ./bzip2 -d < $tmpfile.bz2 > /dev/null
}
autoreconf -fiv
%if %{do_profiling}
export CFLAGS="$RPM_OPT_FLAGS %{cflags_profile_generate}"
%endif
%configure --with-pic --disable-static
%if %{do_profiling}
make %{?_smp_mflags}
profile_bzip2
mkdir .libs.save
mv .libs/*.gcda .libs.save/
make clean
mv .libs.save .libs
export CFLAGS="$RPM_OPT_FLAGS %{cflags_profile_feedback}"
%configure --with-pic --disable-static
%endif
make %{?_smp_mflags}

%install
%make_install
gzip -dc %{SOURCE1} > bznew
install -D -m 755 bznew $RPM_BUILD_ROOT%{_bindir}/bznew
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man1

%post -n libbz2 -p /sbin/ldconfig

%postun -n libbz2  -p /sbin/ldconfig

%docs_package

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/*

%files -n libbz2
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE
%{_libdir}/libbz2.so.1
%{_libdir}/libbz2.so.1.*

%files devel
%manifest %{name}.manifest
%{_includedir}/bzlib.h
%{_libdir}/libbz2.so
%{_libdir}/pkgconfig/bzip2.pc

%changelog
