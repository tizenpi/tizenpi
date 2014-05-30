Name:           m4
Version:        1.4.16
Release:        0
License:        GPL-3.0+
Summary:        GNU m4
Url:            http://www.gnu.org/software/m4/
Group:          Development/Languages/Other
Source:         http://ftp.gnu.org/pub/gnu/m4/%{name}-%{version}.tar.bz2
Source1001: 	m4.manifest
Provides:       base:/usr/bin/m4
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
GNU m4 is an implementation of the traditional Unix macro processor.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure \
	    --without-included-regex \
	    gl_cv_func_isnanl_works=yes \
	    gl_cv_func_printf_directive_n=yes
make %{?_smp_mflags}

%check
make %{?_smp_mflags} check || true

%install
%make_install

%files
#manifest %{name}.manifest
%defattr(-,root,root)
%doc COPYING
%{_bindir}/*
%doc %{_infodir}/*.gz
%{_mandir}/*/*

