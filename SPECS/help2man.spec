Name:           help2man
Version:        1.40.10
Release:        0
License:        GPL-3.0+
Summary:        Create Simple Man Pages from --help Output
Url:            http://www.gnu.org/software/help2man/
Group:          Development/Tools/Doc Generators
Source:         %{name}-%{version}.tar.gz
Source1001: 	help2man.manifest
BuildRequires:  gettext-tools
BuildRequires:  perl-gettext
Requires:       perl-gettext

%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a way
to generate a placeholder man page pointing to that resource while
still providing some useful information.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure --enable-nls
make %{?_smp_mflags}

%install
%make_install

%find_lang %{name} --with-man


%files -f %{name}.lang
#%manifest %{name}.manifest
%defattr(-,root,root,-)
%doc COPYING 
%{_bindir}/help2man
%{_libdir}/help2man/
%doc %{_infodir}/help2man.info.gz
#%{ext_info}
%doc %{_mandir}/man1/help2man.1.gz
#%{ext_man}
%dir %{_mandir}/??
%dir %{_mandir}/??/man1

%changelog
