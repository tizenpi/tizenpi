#
# spec file for package krb5
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define build_mini 0
%define srcRoot krb5-1.10.2
%define krb5docdir  %{_defaultdocdir}/krb5

Name:           krb5
Url:            http://web.mit.edu/kerberos/www/
BuildRequires:  autoconf
BuildRequires:  bison
BuildRequires:  keyutils
BuildRequires:  keyutils-devel
BuildRequires:  libcom_err-devel
BuildRequires:  ncurses-devel
Version:        1.10.2
Release:        0
Summary:        MIT Kerberos5 Implementation--Libraries
License:        MIT
Group:          Productivity/Networking/Security
Source0:         krb5-%{version}.tar.bz2
Source1:        baselibs.conf
Source2:        krb5-rpmlintrc
Source1001: 	krb5.manifest

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of clear text passwords.


%package devel
Summary:        MIT Kerberos5 - Include Files and Libraries
Group:          Development/Libraries/C and C++
Requires:         %{name} = %{version}
Requires:       keyutils-devel
Requires:       libcom_err-devel

%description devel
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords. This package includes Libraries and
Include Files for Development

%prep
%setup -q -n %{srcRoot}
cp %{SOURCE1001} .

%build
# needs to be re-generated
rm -f src/lib/krb5/krb/deltat.c
cd src
./util/reconf
CFLAGS="$RPM_OPT_FLAGS -I/usr/include/et -fno-strict-aliasing -D_GNU_SOURCE -fPIC " \
%configure \
	--prefix=/usr/lib/mit \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--libexecdir=/usr/lib/mit/sbin \
	--libdir=%{_libdir} \
	--includedir=%{_includedir} \
        --localstatedir=%{_localstatedir}/lib/kerberos \
	--enable-shared \
	--disable-static \
        --enable-kdc-replay-cache \
        --enable-dns-for-realm \
        --disable-rpath \
        --disable-pkinit \
        --without-pam \
        --with-system-et \
        --with-system-ss
make %{?jobs:-j%jobs} 

%install
cd src
make DESTDIR=%{buildroot} install 
cd ..
# Munge the krb5-config script to remove rpaths and CFLAGS.
sed "s|^CC_LINK=.*|CC_LINK='\$(CC) \$(PROG_LIBPATH)'|g" src/krb5-config > $RPM_BUILD_ROOT/usr/lib/mit/bin/krb5-config
# install autoconf macro
mkdir -p %{buildroot}/%{_datadir}/aclocal
install -m 644 src/util/ac_check_krb5.m4 %{buildroot}%{_datadir}/aclocal/
# install sample config files
# I'll probably do something about this later on
mkdir -p %{buildroot}%{_sysconfdir} %{buildroot}%{_localstatedir}/lib/kerberos/krb5kdc
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}/var/log/krb5
mkdir -p %{buildroot}/etc/sysconfig/SuSEfirewall2.d/services/
# create plugin directories
mkdir -p %{buildroot}/%{_libdir}/krb5/plugins/kdb
mkdir -p %{buildroot}/%{_libdir}/krb5/plugins/preauth
mkdir -p %{buildroot}/%{_libdir}/krb5/plugins/libkrb5
# all libs must have permissions 0755 
for lib in `find %{buildroot}/%{_libdir}/ -type f -name "*.so*"`
do 
  chmod 0755 ${lib} 
done
# and binaries too
chmod 0755 %{buildroot}/usr/lib/mit/bin/ksu
find . -type f -name '*.ps' -exec gzip -9 {} \;
# create rc* links 
# create links for kinit and klist, because of the java ones
#ln -sf ../../usr/lib/mit/bin/kinit   %{buildroot}/usr/bin/kinit
#ln -sf ../../usr/lib/mit/bin/klist   %{buildroot}/usr/bin/klist


mkdir -p %{buildroot}/usr/bin
ln -sf ../../usr/lib/mit/bin/krb5-config %{buildroot}/usr/bin/krb5-config
# install doc
install -d -m 755 %{buildroot}/%{krb5docdir}
install -m 644 %{_builddir}/%{srcRoot}/README %{buildroot}/%{krb5docdir}/README
# cleanup
rm -f  %{buildroot}/usr/share/man/man1/tmac.doc*
rm -f  /usr/share/man/man1/tmac.doc*
rm -rf %{buildroot}/usr/lib/mit/share/examples
rm -rf %{buildroot}/usr/lib/mit/share/locale
#####################################################
# krb5(-mini) pre/post/postun
#####################################################

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig


########################################################
# files sections
########################################################

%files devel
#%manifest %{name}.manifest
%defattr(-,root,root)
/usr/bin/krb5-config
%dir /usr/lib/mit
%dir /usr/lib/mit/bin
%dir /usr/lib/mit/sbin
%dir /usr/lib/mit/share
%dir %{_datadir}/aclocal
%{_libdir}/libgssrpc.so
%{_libdir}/libk5crypto.so
%{_libdir}/libkadm5clnt_mit.so
%{_libdir}/libkadm5clnt.so
%{_libdir}/libkadm5srv_mit.so
%{_libdir}/libkadm5srv.so
%{_libdir}/libkdb5.so
%{_libdir}/libkrb5.so
%{_libdir}/libkrb5support.so
%{_libdir}/libverto.so
%{_libdir}/libverto-k5ev.so
%{_includedir}/*
/usr/lib/mit/bin/krb5-config
/usr/lib/mit/sbin/krb5-send-pr
/usr/lib/mit/share/gnats
%{_mandir}/man1/krb5-send-pr.1*
%{_mandir}/man1/krb5-config.1*
%{_datadir}/aclocal/ac_check_krb5.m4


%files
#%manifest %{name}.manifest
%defattr(-,root,root)
%dir %{krb5docdir}
# add directories
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%dir %{_libdir}/krb5/plugins/preauth
%dir %{_libdir}/krb5/plugins/libkrb5
%dir %{_localstatedir}/lib/kerberos/
%dir %{_localstatedir}/lib/kerberos/krb5kdc
%attr(0700,root,root) %dir /var/log/krb5
%dir /usr/lib/mit
%dir /usr/lib/mit/sbin
%dir /usr/lib/mit/bin
%doc %{krb5docdir}/README
#%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/krb5.conf
#%attr(0600,root,root) %config(noreplace) %{_localstatedir}/lib/kerberos/krb5kdc/kdc.conf
#%attr(0600,root,root) %config(noreplace) %{_localstatedir}/lib/kerberos/krb5kdc/kadm5.acl
#%attr(0600,root,root) %config(noreplace) %{_localstatedir}/lib/kerberos/krb5kdc/kadm5.dict
%{_libdir}/libgssapi_krb5.*
%{_libdir}/libgssrpc.so.*
%{_libdir}/libk5crypto.so.*
%{_libdir}/libkadm5clnt_mit.so.*
%{_libdir}/libkadm5srv_mit.so.*
%{_libdir}/libkdb5.so.*
%{_libdir}/libkrb5.so.*
%{_libdir}/libkrb5support.so.*
%{_libdir}/libverto.so.*
%{_libdir}/libverto-k5ev.so.*
%{_libdir}/krb5/plugins/kdb/*
#/usr/lib/mit/sbin/*
/usr/lib/mit/sbin/kadmin.local
/usr/lib/mit/sbin/kadmind
/usr/lib/mit/sbin/kpropd
/usr/lib/mit/sbin/kproplog
/usr/lib/mit/sbin/kprop
/usr/lib/mit/sbin/kdb5_util
/usr/lib/mit/sbin/krb5kdc
/usr/lib/mit/sbin/uuserver
/usr/lib/mit/sbin/sserver
/usr/lib/mit/sbin/gss-server
/usr/lib/mit/sbin/sim_server
/usr/lib/mit/bin/k5srvutil
/usr/lib/mit/bin/kvno
/usr/lib/mit/bin/kinit
/usr/lib/mit/bin/kdestroy
/usr/lib/mit/bin/kpasswd
/usr/lib/mit/bin/klist
/usr/lib/mit/bin/kadmin
/usr/lib/mit/bin/ktutil
/usr/lib/mit/bin/kswitch
%attr(0755,root,root) /usr/lib/mit/bin/ksu
/usr/lib/mit/bin/uuclient
/usr/lib/mit/bin/sclient
/usr/lib/mit/bin/gss-client
/usr/lib/mit/bin/sim_client
#/usr/bin/kinit
#/usr/bin/klist
%{_mandir}/man1/kvno.1*
%{_mandir}/man1/kinit.1*
%{_mandir}/man1/kdestroy.1*
%{_mandir}/man1/kpasswd.1*
%{_mandir}/man1/klist.1*
%{_mandir}/man1/kerberos.1*
%{_mandir}/man1/ksu.1*
%{_mandir}/man1/sclient.1*
%{_mandir}/man1/kadmin.1*
%{_mandir}/man1/ktutil.1*
%{_mandir}/man1/k5srvutil.1*
%{_mandir}/man1/kswitch.1*
%{_mandir}/man5/*
%{_mandir}/man5/.k5login.5.gz
%{_mandir}/man5/.k5identity.5*
%{_mandir}/man8/*
