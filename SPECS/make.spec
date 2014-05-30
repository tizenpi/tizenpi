Name:           make
Url:            http://www.gnu.org/software/make/make.html
Provides:       gmake
Version:        3.82
Release:        0
Summary:        GNU make
License:        GPL-2.0+
Group:          Development/Tools/Building
Source:         make-%version.tar.bz2
Source1001: 	make.manifest

%description
The GNU make command with extensive documentation.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export AUTOPOINT=true
%reconfigure --disable-nls
make %{?_smp_mflags}

#%check
#make check

%install
make DESTDIR=$RPM_BUILD_ROOT install
ln -s make $RPM_BUILD_ROOT/usr/bin/gmake
rm %{buildroot}/%{_datadir}/info/dir

%files 
#%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
/usr/bin/make
/usr/bin/gmake
%doc /usr/share/info/make.info-*.gz
%doc /usr/share/info/make.info.gz
%doc /usr/share/man/man1/make.1.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post
%install_info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%postun
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%changelog
