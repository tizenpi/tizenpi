Name:           popt
Version:        1.16
Release:        0
License:        XFree86-1.0
Summary:        A C library for parsing command line parameters
Url:            http://www.rpm5.org/
Group:          Base/Libraries
Source:         popt-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	popt.manifest
BuildRequires:  pkgconfig

%description
Popt is a C library for parsing command line parameters.  Popt was
heavily influenced by the getopt() and getopt_long() functions. It
improves on them by allowing more powerful argument expansion. Popt can
parse arbitrary argv[] style arrays and automatically set variables
based on command line arguments.  Popt allows command line arguments to
be aliased via configuration files and includes utility functions for
parsing arbitrary strings into argv[] arrays using shell-like rules.

%package -n libpopt
Summary:        A C library for parsing command line parameters
Group:          Base/Libraries
Provides:       popt = %{version}
Obsoletes:      popt < %{version}

%description -n libpopt
Popt is a C library for parsing command line parameters.  Popt was
heavily influenced by the getopt() and getopt_long() functions. It
improves on them by allowing more powerful argument expansion. Popt can
parse arbitrary argv[] style arrays and automatically set variables
based on command line arguments.  Popt allows command line arguments to
be aliased via configuration files and includes utility functions for
parsing arbitrary strings into argv[] arrays using shell-like rules.

%package devel
Summary:        Development files for the popt library
Group:          Development/Libraries
Requires:       libpopt = %{version}

%description devel
The popt-devel package includes header files and libraries necessary
for developing programs which use the popt C library. It contains the
API documentation of the popt library, too.

%prep
%setup -q
cp %{SOURCE1001} .
%build
%configure --with-pic --disable-static
make %{?_smp_mflags}

%install
%make_install

%if "%{_libdir}" != "%{_prefix}/lib"
install -d -m755 %{buildroot}/%{_libdir}/pkgconfig
mv %{buildroot}%{_prefix}/lib/pkgconfig/%{name}.pc %{buildroot}/%{_libdir}/pkgconfig/%{name}.pc
%endif

%find_lang %{name}

%post -n libpopt -p /sbin/ldconfig

%postun -n libpopt -p /sbin/ldconfig

%lang_package

%files -n libpopt 
#%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_libdir}/libpopt.so.*

%files devel
#%manifest %{name}.manifest
%defattr(-,root,root)
%doc README
%{_libdir}/libpopt.so
%{_includedir}/popt.h
%{_mandir}/man3/popt.3*
%{_libdir}/pkgconfig/popt.pc

%changelog
