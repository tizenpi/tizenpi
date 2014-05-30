Name:           autoconf
BuildRequires:  xz
BuildRequires:  m4 >= 1.4.6
Url:            http://www.gnu.org/software/autoconf
Requires:       m4 >= 1.4.6
Requires:       perl >= 5.6
Version:        2.69
Release:        0
Summary:        A GNU Tool for Automatically Configuring Source Code
License:        GPL-3.0+
Group:          Development/Tools/Building
Source:         autoconf-%{version}.tar.xz
Source1001: 	autoconf.manifest
BuildArch:      noarch

%description
GNU Autoconf is a tool for configuring source code and makefiles. Using
autoconf, programmers can create portable and configurable packages,
because the person building the package is allowed to specify various
configuration options.

You should install autoconf if you are developing software and would
like to create shell scripts to configure your source code packages.

Note that the autoconf package is not required for the end user who may
be configuring software with an autoconf-generated script; autoconf is
only required for the generation of the scripts, not their use.

%prep
%setup -q -n autoconf-%{version}
cp %{SOURCE1001} .

%build
%configure
make %{?_smp_mflags}

%check
trap 'test $? -ne 0 && cat tests/testsuite.log' EXIT
make check

%install
%{?make_install} %{!?make_install:make install DESTDIR=%{buildroot}}
rm -f $RPM_BUILD_ROOT%{_prefix}/share/emacs/site-lisp/*.el*
# info's dir file is not auto ignored on some systems
rm -rf %{buildroot}%{_infodir}/dir

%post
%install_info --info-dir=%{_infodir} %{_infodir}/autoconf.info.gz

%postun
%install_info_delete --info-dir=%{_infodir} %{_infodir}/autoconf.info.gz


%files
#%manifest %{name}.manifest
%defattr(-,root,root)
%doc COPYING
%{_prefix}/bin/*
%{_prefix}/share/autoconf
%doc %{_infodir}/*.gz
%doc %{_mandir}/man1/*.gz

%changelog
