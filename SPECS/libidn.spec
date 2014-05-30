Name:           libidn
Version:        1.25
Release:        0
License:        (GPL-2.0+ or LGPL-3.0+) and GPL-3.0+
Summary:        Support for Internationalized Domain Names (IDN)
Url:            http://www.gnu.org/software/libidn/
Group:          System/Libraries
Source0:        http://ftp.gnu.org/gnu/libidn/libidn-%{version}.tar.gz
Source1:        baselibs.conf
Source1001: 	libidn.manifest
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
GNU Libidn is an implementation of the Stringprep, Punycode, and IDNA
specifications defined by the IETF Internationalized Domain Names (IDN)
working group. It is used to prepare internationalized strings (such as
domain name labels, usernames, and passwords) in order to increase the
likelihood that string input and string comparison work in ways that
make sense for typical users around the world. The library contains a
generic Stringprep implementation that does Unicode 3.2 NFKC
normalization, mapping and prohibition of characters, and bidirectional
character handling. Profiles for iSCSI, Kerberos 5, Nameprep, SASL, and
XMPP are included. Punycode and ASCII Compatible Encoding (ACE) via
IDNA is supported.

%package devel
License:        LGPL-2.1+
Summary:        Include Files and Libraries mandatory for Development
Group:          System/Libraries
Requires:       %{name} = %{version}
Requires:       glibc-devel

%description devel
GNU Libidn is an implementation of the Stringprep, Punycode, and IDNA
specifications defined by the IETF Internationalized Domain Names (IDN)
working group. It is used to prepare internationalized strings (such as
domain name labels, usernames, and passwords) in order to increase the
likelihood that string input and string comparison work in ways that
make sense for typical users around the world. The library contains a
generic Stringprep implementation that does Unicode 3.2 NFKC
normalization, mapping and prohibition of characters, and bidirectional
character handling. Profiles for iSCSI, Kerberos 5, Nameprep, SASL, and
XMPP are included. Punycode and ASCII Compatible Encoding (ACE) via
IDNA is supported.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure --with-pic --disable-static --disable-gtk-doc
make %{?_smp_mflags}

#%check
%if ! 0%{?qemu_user_space_build}
#make check
%endif

%install
%make_install
rm -f %{buildroot}/%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/libidn.la
%find_lang %{name}


%post -p /sbin/ldconfig

%postun
/sbin/ldconfig


%lang_package

%docs_package

%files
#%manifest %{name}.manifest
%license COPYING
%{_libdir}/libidn.so.*
%{_infodir}/libidn*
%{_bindir}/idn
%{_datadir}/emacs/site-lisp/idna.el
%{_datadir}/emacs/site-lisp/punycode.el

%files devel
#%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libidn.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/libidn.pc

%changelog
