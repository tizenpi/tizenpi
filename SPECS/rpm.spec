%define rpmhome /usr/lib/rpm

Name:           rpm
Summary:        The RPM Package Manager
License:        GPL-2.0+
Group:          Base/Package Management
Version:        4.11.0.1
Release:        0
Url:            http://www.rpm.org
BuildRequires:  binutils
BuildRequires:  bzip2
BuildRequires:  file-devel
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  gettext-tools
BuildRequires:  glibc-devel
BuildRequires:  gzip
BuildRequires:  libacl-devel
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  libcap-devel
BuildRequires:  libelf-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig(lua)
BuildRequires:  make
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  patch
BuildRequires:  pkgconfig(popt)
BuildRequires:  xz-devel
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(nss)
BuildRequires:  uthash-devel
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  libattr-devel
BuildRequires:  pkgconfig(libsmack)


Provides:       rpminst
Provides:	    rpm-libs

### SOURCES BEGIN ###
Source1:       	db-4.8.30.tar.bz2
Source2:	    db-4.8.30-integration.dif
Source4:        rpm-tizen_macros
Source8:        rpmconfigcheck
Source13:	    find-docs.sh
Source22:	    device-sec-policy
Source23:       find-provides.ksyms
Source1001: 	rpm.manifest
### SOURCES END ###
Source0:        rpm-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#
# avoid bootstrapping problem
%define _binary_payload w9.bzdio

%description
RPM Package Manager is the main tool for managing the software packages
of Tizen.

RPM can be used to install and remove software packages. With rpm, it
is easy to update packages.  RPM keeps track of all these manipulations
in a central database.	This way it is possible to get an overview of
all installed packages.  RPM also supports database queries.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Requires:       rpm = %{version}
Requires:       popt-devel

%description devel
This package contains the RPM C library and header files.  These
development files will simplify the process of writing programs which
manipulate RPM packages and databases and are intended to make it
easier to create graphical package managers or any other tools that
need an intimate knowledge of RPM packages in order to function.

%package build
Summary:        Tools and Scripts to create rpm packages
Requires:       rpm = %{version}
Provides:       rpmbuild rpm:%_bindir/rpmbuild
Requires:       bzip2
Requires:       xz
Requires:       gzip
Requires:       binutils
Requires:       make
Requires:       gcc
Requires:       findutils
Requires:       patch
Requires:       glibc-devel

%description build
If you want to build a rpm, you need this package. It provides rpmbuild
and requires some packages that are usually required 

%package security-plugin
Summary: MSM security plugin for rpm
Requires: rpm = %{version}-%{release}
Requires: smack
Requires: libxml2
Requires: nss

%description security-plugin
This package contains the MSM security plugin for rpm that performs
security-related functionality. 


%prep
%setup -q -n rpm-%{version}
### PREP BEGIN ###
cp %{SOURCE1001} .
rm -rf sqlite
tar xjf %{S:1}
ln -s db-4.8.30 db
chmod -R u+w db/*
# will get linked from db3
rm -f rpmdb/db.h
patch -p0 < %{S:2}

if [ -s /etc/rpm/tizen_macros ]; then
	cp -a /etc/rpm/tizen_macros %{SOURCE4}
fi
cp -a %{SOURCE4} tizen_macros
rm -f m4/libtool.m4
rm -f m4/lt*.m4
### PREP END ###

%build
### BUILD BEGIN ###
CPPFLAGS="$CPPFLAGS `pkg-config --cflags nss`"
export CPPFLAGS 
export CFLAGS="%{optflags} -ffunction-sections"
export LDFLAGS="-Wl,-Bsymbolic-functions -ffunction-sections"
%ifarch armv5tel
export CFLAGS="-g -O0 -fno-strict-aliasing -ffunction-sections"
%endif

%if %{_target_cpu}
%ifarch %arm
BUILDTARGET="--host=%{_target_cpu}-tizen-linux-gnueabi"
%else
BUILDTARGET="--build=%{_target_cpu}-tizen-linux"
%endif
%endif

autoreconf -i -f
./configure --disable-dependency-tracking --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
--libdir=%{_libdir} --sysconfdir=/etc --localstatedir=/var  --with-lua \
--with-acl --with-cap  --enable-shared %{?with_python: --enable-python} --with-msm $BUILDTARGET \
--build %{_build}

make %{?_smp_mflags}
### BUILD END ###

%install
mkdir -p %{buildroot}/usr/lib
mkdir -p %{buildroot}/usr/share/locale
ln -s ../share/locale %{buildroot}/usr/lib/locale
%make_install
install -m 644 db3/db.h %{buildroot}/usr/include/rpm
# remove .la file and the static variant of libpopt
# have to remove the dependency from other .la files as well
#for f in %{buildroot}/%{_libdir}/*.la; do
#    sed -i -e "s,/%_lib/libpopt.la,-lpopt,g" $f
#done
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cp -a tizen_macros %{buildroot}/usr/lib/rpm
mkdir -p %{buildroot}/usr/lib/rpm/tizen
install -m 755 %{SOURCE13} %{buildroot}/usr/lib/rpm/tizen
install -m 755 %{SOURCE23} %{buildroot}/usr/lib/rpm
install -m 644 %{SOURCE22} %{buildroot}%{_sysconfdir}/device-sec-policy
install -m 644 %{SOURCE22} %{buildroot}%{_libdir}/rpm-plugins/msm-device-sec-policy
ln -s ../tizen_macros %{buildroot}/usr/lib/rpm/tizen/macros
for d in BUILD RPMS SOURCES SPECS SRPMS BUILDROOT ; do
  mkdir -p %{buildroot}/usr/src/packages/$d
  chmod 755 %{buildroot}/usr/src/packages/$d
done
for d in %{buildroot}/usr/lib/rpm/platform/*-linux/macros ; do
  dd=${d%%-linux/macros}
  dd=${dd##*/}
  mkdir %{buildroot}/usr/src/packages/RPMS/$dd
  chmod 755 %{buildroot}/usr/src/packages/RPMS/$dd
done
mkdir -p %{buildroot}/var/lib/rpm
gzip -9 %{buildroot}/%{_mandir}/man[18]/*.[18]
export RPM_BUILD_ROOT
chmod 755 doc/manual
rm -rf doc/manual/Makefile*
rm -f %{buildroot}/usr/lib/rpmpopt
rm -rf %{buildroot}%{_mandir}/{fr,ja,ko,pl,ru,sk}
rm -f %{buildroot}%{_prefix}/share/locale/de/LC_MESSAGES/rpm.mo
rm -f %{buildroot}/usr/lib/rpm/cpanflute %{buildroot}/usr/lib/rpm/cpanflute2
install -m 755 scripts/find-supplements{,.ksyms} %{buildroot}/usr/lib/rpm
install -m 755 scripts/firmware.prov %{buildroot}/usr/lib/rpm
install -m 755 scripts/debuginfo.prov %{buildroot}/usr/lib/rpm
rm -f %{buildroot}/usr/lib/locale %{buildroot}/usr/lib/rpmrc
mkdir -p %{buildroot}/etc/rpm
chmod 755 %{buildroot}/etc/rpm
mkdir -p %{buildroot}%{rpmhome}/macros.d
# remove some nonsense or non-working scripts
pushd %{buildroot}/usr/lib/rpm/
for f in rpm2cpio.sh rpm.daily rpmdiff* rpm.log rpm.xinetd freshen.sh u_pkg.sh \
         magic magic.mgc magic.mime* rpmfile *.pl javadeps brp-redhat \
         brp-strip-static-archive vpkg-provides*.sh http.req sql.req tcl.req \
         rpmdb_* brp-sparc64-linux brp-strip-comment-note brp-java-gcjcompile
do
    rm -f $f
done
for i in /usr/share/automake-*/*; do
  if test -f "$i" && test -f "${i##*/}"; then
    rm -f "${i##*/}"
  fi
done
popd
rm -rf %{buildroot}/%{_libdir}/python%{py_ver}
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/rpm-plugins/*.la
sh %{buildroot}/usr/lib/rpm/find-lang.sh %{buildroot} rpm
%ifarch armv7hl armv7l
# rpm is using the host_cpu as default for the platform, but armv7hl is not known by the kernel.
# so we need to enforce the platform here.
echo -n %{_target_cpu}-tizen-linux-gnueabi > %{buildroot}/etc/rpm/platform
%endif

%post
/sbin/ldconfig
test -f var/lib/rpm/Packages || rpm --initdb
rm -f var/lib/rpm/Filemd5s var/lib/rpm/Filedigests var/lib/rpm/Requireversion var/lib/rpm/Provideversion

%postun 
/sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
	/etc/rpm
	/bin/rpm
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmkeys
%{_bindir}/rpmquery
%{_bindir}/rpmverify
%{_bindir}/rpmqpack
%attr(0755, root, root) %dir %{rpmhome}
%{rpmhome}/macros
%{rpmhome}/macros.d
%{rpmhome}/rpmpopt*
%{rpmhome}/rpmrc
%{rpmhome}/tizen/macros
%{rpmhome}/tizen_macros
%{rpmhome}/rpm.supp
%{rpmhome}/tgpg
%{rpmhome}/platform

%dir 	%{_libdir}/rpm-plugins
	%{_libdir}/rpm-plugins/exec.so
	%{_libdir}/librpm.so.*
	%{_libdir}/librpmio.so.*
    %{_libdir}/librpmbuild.so.*
    %{_libdir}/librpmsign.so.*
%dir 	/var/lib/rpm
%dir 	%attr(755,root,root) /usr/src/packages/BUILD
%dir 	%attr(755,root,root) /usr/src/packages/SPECS
%dir 	%attr(755,root,root) /usr/src/packages/SOURCES
%dir 	%attr(755,root,root) /usr/src/packages/SRPMS
%dir	%attr(755,root,root) /usr/src/packages/RPMS
%dir	%attr(755,root,root) /usr/src/packages/BUILDROOT
%dir	%attr(755,root,root) /usr/src/packages/RPMS/*

%files build
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/rpmbuild
%{_bindir}/gendiff
%{_bindir}/rpmspec
%{_bindir}/rpmsign

%{rpmhome}/tizen/find-*
%{rpmhome}/brp-*
%{rpmhome}/find-supplements*
%{rpmhome}/check-*
%{rpmhome}/debugedit
%{rpmhome}/find-debuginfo.sh
%{rpmhome}/find-lang.sh
%{rpmhome}/find-provides.ksyms
%{rpmhome}/*provides*
%{rpmhome}/*requires*
%{rpmhome}/*deps*
%{rpmhome}/*.prov
%{rpmhome}/*.req
%{rpmhome}/macros.*
%{rpmhome}/fileattrs


%files devel
%manifest %{name}.manifest
%defattr(644,root,root,755)
%{_bindir}/rpmgraph
/usr/include/rpm
        %{_libdir}/librpm.so
        %{_libdir}/librpmbuild.so
        %{_libdir}/librpmio.so
        %{_libdir}/librpmsign.so
        %{_libdir}/pkgconfig/rpm.pc

%files security-plugin
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/rpm-plugins/msm.so
%{_libdir}/rpm-plugins/msm-device-sec-policy
%config(noreplace) %{_sysconfdir}/device-sec-policy

%lang_package

%docs_package
%doc 	GROUPS

