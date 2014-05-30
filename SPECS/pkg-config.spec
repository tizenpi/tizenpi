Name:           pkg-config
Version:        0.28
Release:        0
Summary:        A library management system
License:        GPL-2.0+
Group:          Base/Tools
Url:            http://pkgconfig.freedesktop.org/
Source:         http://pkgconfig.freedesktop.org/releases/%{name}-%{version}.tar.gz
Source1001: 	pkg-config.manifest
Provides:       pkgconfig = %{version}
# pkg-config has a virtual internal pkg-config.pc file, so we should provide it
Provides:       pkgconfig(pkg-config) = %{version}

%description
The pkg-config program is used to retrieve information about installed
libraries in the system. It is typically used to compile and link
against one or more libraries.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure\
    #--with-internal-glib \
%if "%{_lib}" == "lib"
       --with-pc_path=/usr/local/lib/pkgconfig:/usr/local/share/pkgconfig:%{_libdir}/pkgconfig:%{_datadir}/pkgconfig:/opt/kde3/%{_lib}/pkgconfig
%else
       --with-pc_path=/usr/local/%{_lib}/pkgconfig:/usr/local/lib/pkgconfig:/usr/local/share/pkgconfig:%{_libdir}/pkgconfig:%{_datadir}/pkgconfig:/opt/kde3/%{_lib}/pkgconfig
%endif
make %{?_smp_mflags}

%install
%make_install
rm %{buildroot}%{_datadir}/doc/pkg-config/pkg-config-guide.html

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/pkg-config
%{_bindir}/*-pkg-config
%dir %{_datadir}/aclocal
%{_datadir}/aclocal/pkg.m4

%docs_package

%changelog
