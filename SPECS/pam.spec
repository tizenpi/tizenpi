%define _sbindir /sbin
%define _moduledir %{_libdir}/security
%define _secconfdir %{_sysconfdir}/security
%define _pamconfdir %{_sysconfdir}/pam.d

Name:           pam
Version:        1.1.6
Release:        1
License:        GPL-2.0+ or BSD-3-Clause
Summary:        PAM
Url:            http://www.linux-pam.org/
Group:          Security/Access Control
Source0:        Linux-PAM-%{version}.tar.bz2
Source1:        system-auth
Source2:        other
Source1001:     pam.manifest

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  db4-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  net-tools
BuildRequires:  zlib-devel
BuildRequires:  gettext-tools
BuildRequires:  smack-devel
Requires(post): /sbin/ldconfig
Requires(post): /usr/bin/install
Requires(postun): /sbin/ldconfig

%description
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

%package -n pam-modules-extra
Summary:        Extra modules provided by PAM not used in the base system
Group:          Security/Access Control
Requires:       pam = %{version}

%description -n pam-modules-extra
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication. This package
contains extra modules for use by programs that are not used in the
default Tizen install.

%package devel
Summary:        Files needed for developing PAM-aware applications and modules for PAM
Requires:       pam = %{version}

%description devel
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication. This package
contains header files and static libraries used for building both
PAM-aware applications and modules for use with PAM.

%prep
%setup -q -n Linux-PAM-%{version}
cp %{SOURCE1001} .


%build
CFLAGS="-fPIC %{optflags} " ; export CFLAGS

%reconfigure \
        --libdir=%{_libdir} \
        --includedir=%{_includedir}/security \
        --enable-isadir=../..%{_moduledir} \
        --disable-audit \
        --with-db-uniquename=_pam \
        --with-libiconv-prefix=/usr \
        --enable-read-both-confs &&

make %{?_smp_flags} CFLAGS="$CFLAGS -lfl -lcrypt"

%install
%make_install

# RPM uses docs from source tree
rm -rf %{buildroot}%{_datadir}/doc/Linux-PAM
# Included in setup package
rm -f %{buildroot}%{_sysconfdir}/environment

for phase in auth acct passwd session ; do
	ln -sf pam_unix.so %{buildroot}%{_moduledir}/pam_unix_${phase}.so
done

# Install default pam configuration files
install -d -m 0755 %{buildroot}%{_pamconfdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_pamconfdir}/
install -m 0644 %{SOURCE2} %{buildroot}%{_pamconfdir}/

%find_lang Linux-PAM

%post
/sbin/ldconfig
if [ ! -a /var/log/faillog ] ; then
	/usr/bin/install -m 600 /dev/null /var/log/faillog
fi
if [ ! -a /var/log/tallylog ] ; then
	/usr/bin/install -m 600 /dev/null /var/log/tallylog
fi

%postun -p /sbin/ldconfig

%lang_package -f Linux-PAM

%files
%manifest %{name}.manifest
%license Copyright
%{_sbindir}/pam_tally
%{_sbindir}/pam_tally2
%attr(4755,root,root) %{_sbindir}/pam_timestamp_check
%attr(4755,root,root) %{_sbindir}/unix_chkpwd
%attr(0700,root,root) %{_sbindir}/unix_update
%attr(0755,root,root) %{_sbindir}/mkhomedir_helper
%{_sysconfdir}/security/limits.conf
%{_libdir}/libpam.so.*
%{_libdir}/libpam_misc.so.*
%{_libdir}/libpamc.so.*
%dir %{_moduledir}
%{_moduledir}/pam_deny.so
%{_moduledir}/pam_env.so
%{_moduledir}/pam_keyinit.so
%{_moduledir}/pam_limits.so
%{_moduledir}/pam_loginuid.so
%{_moduledir}/pam_namespace.so
%{_moduledir}/pam_nologin.so
%{_moduledir}/pam_permit.so
%{_moduledir}/pam_lastlog.so
%{_moduledir}/pam_rootok.so
%{_moduledir}/pam_securetty.so
%{_moduledir}/pam_succeed_if.so
%{_moduledir}/pam_unix.so
%{_moduledir}/pam_wheel.so
%{_moduledir}/pam_xauth.so
%{_moduledir}/pam_filter
%{_moduledir}/pam_mkhomedir.so
%dir %{_secconfdir}
%config(noreplace) %{_secconfdir}/access.conf
%config(noreplace) %{_secconfdir}/group.conf
%config(noreplace) %{_secconfdir}/namespace.conf
#%dir %{_secconfdir}/namespace.d
%attr(755,root,root) %config(noreplace) %{_secconfdir}/namespace.init
%config(noreplace) %{_secconfdir}/pam_env.conf
%config(noreplace) %{_secconfdir}/time.conf
%dir %{_pamconfdir}
%{_pamconfdir}/system-auth
%{_pamconfdir}/other

%files -n pam-modules-extra
%manifest %{name}.manifest
%{_moduledir}/pam_access.so
%{_moduledir}/pam_debug.so
%{_moduledir}/pam_echo.so
%{_moduledir}/pam_exec.so
%{_moduledir}/pam_faildelay.so
%{_moduledir}/pam_filter.so
%{_moduledir}/pam_ftp.so
%{_moduledir}/pam_group.so
%{_moduledir}/pam_issue.so
%{_moduledir}/pam_listfile.so
%{_moduledir}/pam_localuser.so
%{_moduledir}/pam_mail.so
%{_moduledir}/pam_motd.so
%{_moduledir}/pam_pwhistory.so
%{_moduledir}/pam_rhosts.so
%{_moduledir}/pam_shells.so
%{_moduledir}/pam_stress.so
%{_moduledir}/pam_tally.so
%{_moduledir}/pam_time.so
%{_moduledir}/pam_timestamp.so
%{_moduledir}/pam_umask.so
%{_moduledir}/pam_unix_acct.so
%{_moduledir}/pam_unix_auth.so
%{_moduledir}/pam_unix_passwd.so
%{_moduledir}/pam_unix_session.so
%{_moduledir}/pam_warn.so
%{_moduledir}/pam_smack.so

%files devel
%manifest %{name}.manifest
%{_includedir}/security/*
%{_libdir}/libpam.so
%{_libdir}/libpam_misc.so
%{_libdir}/libpamc.so
%{_libdir}/security/pam_tally2.so

%docs_package
