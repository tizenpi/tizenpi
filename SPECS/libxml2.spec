Name:           libxml2
Version:        2.8.0
Release:        0
Summary:        A Library to Manipulate XML Files
License:        MIT
Group:          System/Libraries
Url:            http://xmlsoft.org
# Source ftp://xmlsoft.org/libxml2/libxml2-git-snapshot.tar.gz changes every day
Source:         ftp://xmlsoft.org/libxml2/%{name}-%{version}.tar.gz
Source2:        baselibs.conf
Source1001: 	libxml2.manifest
BuildRequires:  pkg-config
BuildRequires:  readline-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

%description
The XML C library was initially developed for the GNOME project. It is
now used by many programs to load and save extensible data structures
or manipulate any kind of XML files.

This library implements a number of existing standards related to
markup languages, including the XML standard, name spaces in XML, XML
Base, RFC 2396, XPath, XPointer, HTML4, XInclude, SGML catalogs, and
XML catalogs. In most cases, libxml tries to implement the
specification in a rather strict way. To some extent, it provides
support for the following specifications, but does not claim to
implement them: DOM, FTP client, HTTP client, and SAX.

The library also supports RelaxNG. Support for W3C XML Schemas is in
progress.


%package tools
Summary:        Tools using libxml
Group:          System/Libraries

%description tools
This package contains xmllint, a very useful tool proving libxml's power.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       %{name}-tools = %{version}
Requires:       glibc-devel
Requires:       readline-devel
Requires:       xz-devel
Requires:       zlib-devel

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure --disable-static \
    --docdir=%_docdir/%name \
    --with-html-dir=%_docdir/%name/html \
    --with-fexceptions \
    --with-history \
    --without-python \
    --enable-ipv6 \
    --with-sax1 \
    --with-regexps \
    --with-threads \
    --with-reader \
    --with-http

make %{?_smp_mflags} BASE_DIR="%_docdir" DOC_MODULE="%name"

%check
# qemu-arm can't keep up atm, disabling check for arm
%ifnarch %arm
make check
%endif

%install
make install DESTDIR="%buildroot" BASE_DIR="%_docdir" DOC_MODULE="%name"
ln -s libxml2/libxml %{buildroot}%{_includedir}/libxml

%remove_docs

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
#%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING*
%{_libdir}/lib*.so.*

%files tools
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_bindir}/xmllint
%{_bindir}/xmlcatalog

%files devel
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_bindir}/xml2-config
%dir %{_datadir}/aclocal
%{_datadir}/aclocal/libxml.m4
%{_includedir}/libxml
%{_includedir}/libxml2
%{_libdir}/lib*.so
# libxml2.la is needed for the python-libxml2 build. Deleting it breaks build of python-libxml2.
%{_libdir}/libxml2.la
%{_libdir}/*.sh
%{_libdir}/pkgconfig/*.pc

%changelog
