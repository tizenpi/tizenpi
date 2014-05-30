# The split of gettext into two packages is suggested by upstream (see
# the PACKAGING file). Here we name gettext-runtime as
# gettext-lib. Please be noted that gettext-runtime is LGPL while the
# others parts are of GPL. You should be careful of the license when
# adding files into these sub-packages.


%define enable_testing 0

Name:           gettext
Version:        0.18.3.2
Release:        1
License:        GPL-3.0+ and LGPL-2.0+
Summary:        GNU libraries and utilities for producing multi-lingual messages
Url:            http://www.gnu.org/software/gettext/
Group:          Development/Tools
Source:         ftp://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.gz
Source2:        msghack.py
Source1001:     gettext.manifest

BuildRequires:  autoconf >= 2.5
BuildRequires:  bison
# need expat for xgettext on glade
BuildRequires:  expat-devel
BuildRequires:  gcc-c++
BuildRequires:  libtool
#needed for ANSI to UTF8 conversion using msgconn
BuildRequires:  libunistring
BuildRequires:  glibc-locale

%description
The GNU gettext package provides a set of tools and documentation for
producing multi-lingual messages in programs. Tools include a set of
conventions about how programs should be written to support message
catalogs, a directory and file naming organization for the message
catalogs, a runtime library which supports the retrieval of translated
messages, and stand-alone programs for handling the translatable and
the already translated strings. Gettext provides an easy to use
library and tools for creating, using, and modifying natural language
catalogs and is a powerful and simple method for internationalizing
programs.

MeeGo's gettext is split into two packages: gettext-libs and
gettext-devel. gettext-libs is an LGPLv2+ package that contains
libraries and runtime needed by i18n programs; gettext-devel is used
only for development and building -- and shouldn't be needed by end
users.  This gettext package is a meta-package that depends on
gettext-devel for transition.

%package tools
License:        GPL-3.0+
Summary:        Development files for %{name}
Group:          Development/Tools
Requires:       %{name}-runtime = %{version}
Obsoletes:      gettext-devel <= 0.18.1.1-1.15
Provides:       gettext-devel

%description tools
This package contains all development related files necessary for
developing or compiling applications/libraries that needs
internationalization capability. You also need this package if you
want to add gettext support for your project.

%package runtime
License:        LGPL-2.0+
Summary:        Libraries for %{name}
Group:          System/Libraries
Obsoletes:      gettext-libs <= 0.18.1.1-1.15
Provides:       gettext-libs

%description runtime
This package contains libraries used internationalization support.

%prep
%setup -q


%build
cp %{SOURCE1001} .
[ -f  %{_datadir}/automake/depcomp ] && cp -f %{_datadir}/automake/{depcomp,ylwrap} .

%ifarch %arm
# We add a compile flag for ARM to deal with a bug in qemu (msgmerge using pthread/gomp)
# msgmerge will lockup during execution.
%define addconfflag --without-libpth-prefix --disable-openmp
%else
%endif

mkdir -p gettext-tools/intl

%reconfigure --without-included-gettext --enable-nls --disable-static \
    --enable-shared --with-pic-=yes --disable-csharp --without-libpth-prefix --disable-openmp
make %{?_smp_mflags} GCJFLAGS="-findirect-dispatch"

#%check
#make check

%install
make install DESTDIR=%{buildroot} INSTALL="install -p" \
    lispdir=%{_datadir}/emacs/site-lisp \
    aclocaldir=%{_datadir}/aclocal EXAMPLESFILES=""

install -pm 755 %{SOURCE2} %{buildroot}%{_bindir}/msghack

# make preloadable_libintl.so executable
chmod 755 %{buildroot}%{_libdir}/preloadable_libintl.so

rm -f %{buildroot}%{_infodir}/dir

# doc relocations
for i in gettext-runtime/man/*.html; do
  rm %{buildroot}%{_datadir}/doc/gettext/`basename $i`
done
rm -r %{buildroot}%{_datadir}/doc/gettext/javadoc*

rm -rf %{buildroot}%{_datadir}/doc/gettext/examples

rm -rf htmldoc
mkdir htmldoc
mv %{buildroot}%{_datadir}/doc/gettext/* %{buildroot}%{_datadir}/doc/libasprintf/* htmldoc
rm -r %{buildroot}%{_datadir}/doc/libasprintf
rm -r %{buildroot}%{_datadir}/doc/gettext

# remove unpackaged files from the buildroot
rm -rf %{buildroot}%{_datadir}/emacs
rm %{buildroot}%{_libdir}/lib*.la


%find_lang %{name}-runtime
%find_lang %{name}-tools
cat %{name}-*.lang > %{name}.lang

%docs_package

%post runtime -p /sbin/ldconfig

%postun runtime -p /sbin/ldconfig

%post tools -p /sbin/ldconfig

%postun tools -p /sbin/ldconfig

%files tools -f %{name}.lang
#%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_datadir}/%{name}/projects/*
%{_datadir}/%{name}/config.rpath
%{_datadir}/%{name}/*.h
%{_datadir}/%{name}/intl
%{_datadir}/%{name}/po
%{_datadir}/%{name}/msgunfmt.tcl
%{_datadir}/aclocal/*
%{_includedir}/*
%{_libdir}/libasprintf.so
%{_libdir}/libgettextpo.so
%{_libdir}/libgettextlib*.so
%{_libdir}/libgettextsrc*.so
%{_libdir}/preloadable_libintl.so
%{_libdir}/gettext/hostname
%{_libdir}/gettext/project-id
%{_libdir}/gettext/urlget
%{_libdir}/gettext/user-email
%{_libdir}/libgettextpo.so.*
%{_datadir}/%{name}/javaversion.class
%{_datadir}/%{name}/archive*.tar.xz
%{_datadir}/%{name}/styles
%{_bindir}/autopoint
%{_bindir}/gettextize
%{_bindir}/msgattrib
%{_bindir}/msgcat
%{_bindir}/msgcmp
%{_bindir}/msgcomm
%{_bindir}/msgconv
%{_bindir}/msgen
%{_bindir}/msgexec
%{_bindir}/msgfilter
%{_bindir}/msgfmt
%{_bindir}/msggrep
%{_bindir}/msghack
%{_bindir}/msginit
%{_bindir}/msgmerge
%{_bindir}/msgunfmt
%{_bindir}/msguniq
%{_bindir}/recode-sr-latin
%{_bindir}/xgettext

# Don't include language files here since that may inadvertently
# involve unneeded files. If you need to include a file in -libs, list
# it here explicitly
%files runtime
#%manifest %{name}.manifest
%defattr(-,root,root,-)
# Files listed here should be of LGPL license only, refer to upstream
# statement in PACKAGING file
%license gettext-runtime/intl/COPYING*
%doc %{_datadir}/gettext/ABOUT-NLS
%{_bindir}/gettext
%{_bindir}/ngettext
%{_bindir}/envsubst
%{_bindir}/gettext.sh
%{_libdir}/libasprintf.so.*
