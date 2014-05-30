%global nss_softokn_fips_version 3.12.4

Name:           nss
BuildRequires:  gcc-c++
BuildRequires:  nspr-devel
BuildRequires:  pkg-config
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(sqlite3)
Version:        3.15.4
Release:        0
Summary:        Network Security Services
License:        MPL-1.1 or GPL-2.0+ or LGPL-2.1+
Group:          Security/Crypto Libraries
Url:            http://www.mozilla.org/projects/security/pki/nss/
# cvs -d :pserver:anonymous@cvs-mirror.mozilla.org:/cvsroot co -r <RTM_TAG> NSS
Source:         nss-%{version}.tar.bz2
Source1:        nss.pc.in
Source3:        nss-config.in
Source4:        %{name}-rpmlintrc
Source5:        baselibs.conf
Source6:        setup-nsssysinit.sh
Source7:        cert9.db
Source8:        key4.db
Source9:        pkcs11.txt
Source1001: 	nss.manifest
%define nspr_ver %(rpm -q --queryformat '%{VERSION}' nspr)
Requires(pre):  nspr >= %nspr_ver
Requires(pre):  libfreebl3 >= %{nss_softokn_fips_version}
Requires(pre):  libsoftokn3 >= %{nss_softokn_fips_version}
Requires:       nss-certs
%define nssdbdir %{_sysconfdir}/pki/nssdb
%define run_testsuite 0

%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled server
applications. Applications built with NSS can support SSL v2 and v3,
TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3
certificates, and other security standards.


%package devel
Summary:        Network (Netscape) Security Services development files
Group:          Development/Libraries
Requires:       libfreebl3
Requires:       libsoftokn3
Requires:       nspr-devel
Requires:       nss = %{version}-%{release}

%description devel
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled server
applications. Applications built with NSS can support SSL v2 and v3,
TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3
certificates, and other security standards.


%package tools
Summary:        Tools for developing, debugging, and managing applications that use NSS
Group:          Security/Crypto Libraries
Requires(pre):  nss >= %{version}

%description tools
The NSS Security Tools allow developers to test, debug, and manage
applications that use NSS.


%package sysinit
Summary:        System NSS Initialization
Group:          System/Management
Requires:       nss >= %{version}
Requires(post): coreutils

%description sysinit
Default Operation System module that manages applications loading
NSS globally on the system. This module loads the system defined
PKCS #11 modules for NSS and chains with other NSS modules to load
any system or user configured modules.


%package -n libfreebl3
Summary:        Freebl library for the Network Security Services
Group:          Security/Crypto Libraries

%description -n libfreebl3
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled server
applications. Applications built with NSS can support SSL v2 and v3,
TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3
certificates, and other security standards.

This package installs the freebl library from NSS.


%package -n libsoftokn3
Summary:        Network Security Services Softoken Module
Group:          Security/Network
Requires:       libfreebl3 = %{version}-%{release}

%description -n libsoftokn3
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled server
applications. Applications built with NSS can support SSL v2 and v3,
TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3
certificates, and other security standards.

Network Security Services Softoken Cryptographic Module


%package certs
Summary:        CA certificates for NSS
Group:          Security/Certificate Management

%description certs
This package contains the integrated CA root certificates from the
Mozilla project.


%prep
%setup -n nss-%{version} -q
cp %{SOURCE1001} .

%build
#modified="$(sed -n '/^----/n;s/ - .*$//;p;q' "%{_sourcedir}/%{name}.changes")"
#DATE="\"$(date -d "${modified}" "+%%b %%e %%Y")\""
#TIME="\"$(date -d "${modified}" "+%%R")\""
#find . -name '*.[ch]' -print -exec sed -i "s/__DATE__/${DATE}/g;s/__TIME__/${TIME}/g" {} +
cd nss
export FREEBL_NO_DEPEND=1
export NSPR_INCLUDE_DIR=`nspr-config --includedir`
export NSPR_LIB_DIR=`nspr-config --libdir`
export OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export LIBDIR=%{_libdir}
export CC=%{_host}-gcc
%ifarch x86_64 aarch64
export USE_64=1
%endif
export NSS_USE_SYSTEM_SQLITE=1
MAKE_FLAGS="BUILD_OPT=1 NSS_ENABLE_ECC=1 CC=%{_host}-gcc"
make nss_build_all $MAKE_FLAGS
# run testsuite
%if 0%{?run_testsuite}
export BUILD_OPT=1
export HOST="localhost"
export DOMSUF=" "
export USE_IP=TRUE
export IP_ADDRESS="127.0.0.1"
cd tests
./all.sh
if grep "FAILED" ../../../tests_results/security/localhost.1/output.log ; then
  echo "Testsuite FAILED"
  exit 1
fi
%endif

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/nss
mkdir -p $RPM_BUILD_ROOT%{_includedir}/nss3
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{nssdbdir}
pushd dist/Linux*
# copy headers
cp -rL ../public/nss/*.h $RPM_BUILD_ROOT%{_includedir}/nss3
# copy dynamic libs
cp -L  lib/libnss3.so \
       lib/libnssdbm3.so \
       lib/libnssdbm3.chk \
       lib/libnssutil3.so \
       lib/libnssckbi.so \
       lib/libnsssysinit.so \
       lib/libsmime3.so \
       lib/libsoftokn3.so \
       lib/libsoftokn3.chk \
       lib/libssl3.so \
       $RPM_BUILD_ROOT%{_libdir}
cp -L  lib/libfreebl3.so \
       lib/libfreebl3.chk \
       $RPM_BUILD_ROOT/%{_libdir}
# copy static libs
cp -L  lib/libcrmf.a \
       lib/libnssb.a \
       lib/libnssckfw.a \
       $RPM_BUILD_ROOT%{_libdir}
# copy tools
cp -L  bin/certutil \
       bin/cmsutil \
       bin/crlutil \
       bin/modutil \
       bin/pk12util \
       bin/signtool \
       bin/signver \
       bin/ssltap \
       $RPM_BUILD_ROOT%{_bindir}
# copy unsupported tools
cp -L  bin/atob \
       bin/btoa \
       bin/derdump \
       bin/ocspclnt \
       bin/pp \
       bin/selfserv \
       bin/shlibsign \
       bin/strsclnt \
       bin/symkeyutil \
       bin/tstclnt \
       bin/vfyserv \
       bin/vfychain \
       $RPM_BUILD_ROOT%{_libexecdir}/nss
# prepare pkgconfig file
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
sed "s:%%LIBDIR%%:%{_libdir}:g
s:%%VERSION%%:%{version}:g
s:%%NSPR_VERSION%%:%{nspr_ver}:g" \
  %{SOURCE1} > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/nss.pc
# prepare nss-config file
popd
NSS_VMAJOR=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VMAJOR" | awk '{print $3}'`
NSS_VMINOR=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VMINOR" | awk '{print $3}'`
NSS_VPATCH=`cat nss/lib/nss/nss.h | grep "#define.*NSS_VPATCH" | awk '{print $3}'`
cat %{SOURCE3} | sed -e "s,@libdir@,%{_libdir},g" \
                     -e "s,@prefix@,%{_prefix},g" \
                     -e "s,@exec_prefix@,%{_prefix},g" \
                     -e "s,@includedir@,%{_includedir}/nss3,g" \
                     -e "s,@MOD_MAJOR_VERSION@,$NSS_VMAJOR,g" \
                     -e "s,@MOD_MINOR_VERSION@,$NSS_VMINOR,g" \
                     -e "s,@MOD_PATCH_VERSION@,$NSS_VPATCH,g" \
                     > $RPM_BUILD_ROOT/%{_bindir}/nss-config
chmod 755 $RPM_BUILD_ROOT/%{_bindir}/nss-config
# setup-nsssysinfo.sh
install -m 744 %{SOURCE6} $RPM_BUILD_ROOT%{_sbindir}/
# create empty NSS database
#LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_lib}:$RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_bindir}/modutil -force -dbdir "sql:$RPM_BUILD_ROOT%{nssdbdir}" -create
#LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_lib}:$RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_bindir}/certutil -N -d "sql:$RPM_BUILD_ROOT%{nssdbdir}" -f /dev/null 2>&1 > /dev/null
#chmod 644 "$RPM_BUILD_ROOT%{nssdbdir}"/*
#sed "s:%{buildroot}::g
#s/^library=$/library=libnsssysinit.so/
#/^NSS/s/\(Flags=internal\)\(,[^m]\)/\1,moduleDBOnly\2/" \
#  $RPM_BUILD_ROOT%{nssdbdir}/pkcs11.txt > $RPM_BUILD_ROOT%{nssdbdir}/pkcs11.txt.sed
#  mv $RPM_BUILD_ROOT%{nssdbdir}/pkcs11.txt{.sed,}
# copy empty NSS database
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{nssdbdir}
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{nssdbdir}
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{nssdbdir}
# create shlib sigs after extracting debuginfo
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_lib}:$RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_libexecdir}/nss/shlibsign -i $RPM_BUILD_ROOT%{_libdir}/libsoftokn3.so \
  LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_lib}:$RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_libexecdir}/nss/shlibsign -i $RPM_BUILD_ROOT%{_libdir}/libnssdbm3.so \
  LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_lib}:$RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_libexecdir}/nss/shlibsign -i $RPM_BUILD_ROOT/%{_libdir}/libfreebl3.so \
%{nil}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n libfreebl3 -p /sbin/ldconfig

%postun -n libfreebl3 -p /sbin/ldconfig

%post -n libsoftokn3 -p /sbin/ldconfig

%postun -n libsoftokn3 -p /sbin/ldconfig

%post sysinit
/sbin/ldconfig
# make sure the current config is enabled
%{_sbindir}/setup-nsssysinit.sh on

%preun sysinit
if [ $1 = 0 ]; then
  %{_sbindir}/setup-nsssysinit.sh off
fi

%postun sysinit -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/libnss3.so
%{_libdir}/libnssutil3.so
%{_libdir}/libsmime3.so
%{_libdir}/libssl3.so

%files devel
#%manifest %{name}.manifest
%defattr(644, root, root, 755)
%{_includedir}/nss3/
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%attr(755,root,root) %{_bindir}/nss-config

%files tools
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_bindir}/*
%exclude %{_sbindir}/setup-nsssysinit.sh
%{_libexecdir}/nss/
%exclude %{_bindir}/nss-config

%files sysinit
#%manifest %{name}.manifest
%defattr(-, root, root)
%dir %{_sysconfdir}/pki
%dir %{_sysconfdir}/pki/nssdb
%config(noreplace) %{_sysconfdir}/pki/nssdb/*
%{_libdir}/libnsssysinit.so
%{_sbindir}/setup-nsssysinit.sh

%files -n libfreebl3
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/libfreebl3.so
%{_libdir}/libfreebl3.chk

%files -n libsoftokn3
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/libsoftokn3.so
%{_libdir}/libsoftokn3.chk
%{_libdir}/libnssdbm3.so
%{_libdir}/libnssdbm3.chk

%files certs
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/libnssckbi.so

%changelog
