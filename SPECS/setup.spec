Name:           setup
Version:        0.9
Release:        1
License:        Public Domain
Summary:        A set of system configuration and setup files
Url:            https://fedorahosted.org/setup/
Group:          Base/Configuration
Source0:        %{name}-%{version}.tar.bz2
Source1001:     setup.manifest
BuildRequires:  bash
BuildArch:      noarch

%description
The setup package contains a set of important system configuration and
setup files, such as passwd, group, and profile.

%package misc
Summary:    Misc. basic tools and scripts
Requires:   setup
%description misc
Misc. basic tools and scripts.


%prep
%setup -q

cp %{SOURCE1001} .
./shadowconvert.sh

%build

#%check
# Run any sanity checks.
#make check

%install
cp -ar files/* %{buildroot}
touch %{buildroot}%{_sysconfdir}/environment
chmod 0644 %{buildroot}%{_sysconfdir}/environment
chmod 0400 %{buildroot}%{_sysconfdir}/{shadow,gshadow}
touch %{buildroot}%{_sysconfdir}/fstab
ln -nsf /proc/self/mounts %{buildroot}%{_sysconfdir}/mtab


rm %{buildroot}/%{_sysconfdir}/filesystems

#throw away useless and dangerous update stuff until rpm will be able to
#handle it ( http://rpm.org/ticket/6 )

# TODO nie działa to bo nie ma lua skompilowanego
#%post -p <lua>
#for i, name in ipairs({"passwd", "shadow", "group", "gshadow"}) do
#     os.remove("/etc/"..name..".rpmnew")
#end
%files
#%manifest %{name}.manifest
%license COPYING
#%manifest setup.manifest
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/passwd
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/group
%verify(not md5 size mtime) %attr(0000,root,root) %config(noreplace,missingok) %{_sysconfdir}/shadow
%verify(not md5 size mtime) %attr(0000,root,root) %config(noreplace,missingok) %{_sysconfdir}/gshadow
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/services
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/exports
%config(noreplace) %{_sysconfdir}/aliases
%config(noreplace) %{_sysconfdir}/environment
%config(noreplace) %{_sysconfdir}/host.conf
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/hosts
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/hosts.allow
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/hosts.deny
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/motd
%config(noreplace) %{_sysconfdir}/printcap
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/inputrc
%config(noreplace) %{_sysconfdir}/bashrc
%config(noreplace) %{_sysconfdir}/profile
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/protocols
%attr(0600,root,root) %config(noreplace,missingok) %{_sysconfdir}/securetty
%dir %{_sysconfdir}/profile.d
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/shells
%ghost %attr(0644,root,root) %verify(not md5 size mtime) /var/log/lastlog
%ghost %attr(0600,root,root) %verify(not md5 size mtime) /var/log/faillog
%ghost %attr(0664,root,utmp) %verify(not md5 size mtime) /var/log/wtmp
%ghost %attr(0600,root,root) %verify(not md5 size mtime) /var/log/btmp
%ghost %attr(0664,root,utmp) %verify(not md5 size mtime) /run/utmp
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) %{_sysconfdir}/fstab
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) %{_sysconfdir}/mtab
/run/*
/etc/profile.d/*

%files misc
#%manifest %{name}.manifest
%{_bindir}/*
%{_sbindir}/*
%docs_package
