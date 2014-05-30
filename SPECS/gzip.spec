Name:           gzip
Version:        1.6
Release:        1
License:        GPL-3.0+
Summary:        The GNU data compression program
Url:            http://www.gnu.org/software/gzip/
Group:          Base/Compression
Source0:        %{name}-%{version}.tar.xz
Source1001: 	gzip.manifest
Requires:       /usr/bin/mktemp

%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.

Gzip should be installed on your system, because it is a
very commonly used data compression program.


%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure \
    --bindir=%{_bindir}

make %{?_smp_mflags}

%install
%make_install

%docs_package

%files
#%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/gzip
%{_bindir}/gunzip
%{_bindir}/zcmp
%{_bindir}/zegrep
%{_bindir}/zforce
%{_bindir}/znew
%{_bindir}/gzexe
%{_bindir}/zdiff
%{_bindir}/zfgrep
%{_bindir}/zgrep
%{_bindir}/zmore
%{_bindir}/zcat
%{_bindir}/uncompress
%{_bindir}/zless

