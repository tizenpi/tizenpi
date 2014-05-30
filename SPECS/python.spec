Name:           python
Version:        2.7.3
Release:        1
License:        Python-2.0
Summary:        Python Interpreter
Url:            http://www.python.org/
Group:          Development/Languages
%define         tarversion %{version}
%define         tarname Python-%{tarversion}
Source0:        %{tarname}.tar.bz2
Source1:        macros.python
Source2:        pythonstart
Source3:        python.sh
Source4:        python.csh
Source5:        _local.pth
Source1001:     %name.manifest
BuildRequires:  automake
BuildRequires:  db4-devel
BuildRequires:  fdupes
BuildRequires:  gmp-devel
BuildRequires:  bzip2-devel
BuildRequires:  openssl-devel
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  sqlite-devel
BuildRequires:  zlib-devel
%define         python_version    %(echo %{tarversion} | head -c 3)
%define         idle_name         idle
Provides:       %{name} = %{python_version}
# FIXME
Provides:       /bin/python
Obsoletes:      python-elementtree
Obsoletes:      python-nothreads
Obsoletes:      python-sqlite

%description
Python is an interpreted, object-oriented programming language, and is
often compared to Tcl, Perl, Scheme, or Java.  You can find an overview
of Python in the documentation and tutorials included in the python-doc
(HTML) or python-doc-pdf (PDF) packages.

If you want to install third party modules using distutils, you need to
install python-devel package.

%package curses
Summary:        Python Interface to the (N)Curses Library
Requires:       python = %{version}
Obsoletes:      pyth_cur
Provides:       pyth_cur

%description curses
An easy to use interface to the (n)curses CUI library. CUI stands for
Console User Interface.

%package -n python-devel
Summary:        Include Files and Libraries Mandatory for Building Python Modules
Requires:       glibc-devel
Requires:       python = %{version}

%description -n python-devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.

This package contains header files, a static library, and development
tools for building Python modules, extending the Python interpreter or
embedding Python in applications.

%package -n python-xml
Summary:        A Python XML Interface
Requires:       python = %{version}
# pyxml used to live out of tree
Provides:       pyxml = 0.8.5
Obsoletes:      pyxml < 0.8.5

%description -n python-xml
The expat module is a Python interface to the expat XML parser. Since
Python2.x, it is part of the core Python distribution.

%package -n libpython
Summary:        Python Interpreter shared library

%description -n libpython
Python is an interpreted, object-oriented programming language, and is
often compared to Tcl, Perl, Scheme, or Java.  You can find an overview
of Python in the documentation and tutorials included in the python-doc
(HTML) or python-doc-pdf (PDF) packages.

This package contains libpython2.6 shared library for embedding in
other applications.

%prep
%setup -q -n %{tarname}

# drop Autoconf version requirement
sed -i 's/^version_required/dnl version_required/' configure.in

# remove newslist.py because of bad license
rm Demo/scripts/newslist.*

%build
cp %{S:1001} .
export OPT=$(echo $RPM_OPT_FLAGS | sed -s "s/--param=ssp-buffer-size=32//g")
export CXX=%{__cxx}
export CC=%{__cc}

autoreconf -f -i . # Modules/_ctypes/libffi
# prevent make from trying to rebuild asdl stuff, which requires existing
# python installation
touch Parser/asdl* Python/Python-ast.c Include/Python-ast.h

%configure \
    --docdir=%{_docdir}/python \
    --enable-ipv6 \
    --with-fpectl \
    --enable-shared \
    --enable-unicode=ucs4

LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH \
    make %{?_smp_mflags} profile-opt

%install
# replace rest of /usr/local/bin/python or /usr/bin/python2.x with /usr/bin/python
find . -wholename "./Parser" -prune -o -name '*.py' -type f -print0 | xargs -0 grep -lE '^#! *(/usr/.*bin/(env +)?)?python' | xargs sed -r -i -e '1s@^#![[:space:]]*(/usr/(local/)?bin/(env +)?)?python([0-9]+\.[0-9]+)?@#!/usr/bin/python@'
# the grep inbetween makes it much faster
########################################
# install it
########################################
export OPT=$(echo $RPM_OPT_FLAGS | sed -s "s/--param=ssp-buffer-size=32//g")
%make_install 
# install site-specific tweaks
#ln -s python%{python_version} %{buildroot}%{_bindir}/python2
install -m 644 %{SOURCE4} %{buildroot}%{_libdir}/python%{python_version}/distutils
install -m 644 %{SOURCE5} %{buildroot}%{_libdir}/python%{python_version}/site-packages
install -d -m 755 %{buildroot}%{_sysconfdir}/rpm
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm
# make sure /usr/lib/python/site-packages exists even on lib64 machines
mkdir -p %{buildroot}%{_prefix}/lib/python%{python_version}/site-packages

########################################
# some cleanups
########################################
# remove hard links and replace them with symlinks
for dir in bin include %{_lib} ; do
    rm -f %{buildroot}/%{_prefix}/$dir/python
    ln -s python%{python_version} %{buildroot}/%{_prefix}/$dir/python
done
# kill imageop.so, it's insecure
rm -f %{buildroot}/%{_libdir}/python%{python_version}/lib-dynload/imageop.so
# replace duplicate .pyo/.pyc with hardlinks
fdupes %{buildroot}/%{_libdir}/python%{python_version}
########################################
# documentation
########################################
export PDOCS=%{buildroot}%{_docdir}/%{name}
install -d -m 755 $PDOCS
install -c -m 644 README                            $PDOCS/
ln -s python%{python_version}.1.gz %{buildroot}%{_mandir}/man1/python.1.gz

########################################
# devel
########################################
# install Makefile.pre.in and Makefile.pre
cp Makefile Makefile.pre.in Makefile.pre %{buildroot}%{_libdir}/python%{python_version}/config/

########################################
# startup script
########################################
install -d -m 755 %{buildroot}%{_sysconfdir}/profile.d
install -m 644 %{SOURCE2} %{buildroot}/etc
install -m 644 %{SOURCE3} %{SOURCE4} %{buildroot}%{_sysconfdir}/profile.d

rm -rf %{buildroot}%{_bindir}/idle
rm -rf %{buildroot}%{_libdir}/python%{python_version}/idlelib
rm -rf %{buildroot}%{_libdir}/python%{python_version}/lib-tk

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files curses
#%manifest %{name}.manifest
%defattr(644, root, root, 755)
%{_libdir}/python%{python_version}/curses
%{_libdir}/python%{python_version}/lib-dynload/_curses.so
%{_libdir}/python%{python_version}/lib-dynload/_curses_panel.so

%files
#%manifest %{name}.manifest
%defattr(644, root, root, 755)
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README
%license LICENSE
%config %{_sysconfdir}/pythonstart
%config %{_sysconfdir}/profile.d/python.*
%dir %{_libdir}/python%{python_version}
%{_libdir}/python%{python_version}/ssl.py*
%{_libdir}/python%{python_version}/bsddb
%{_libdir}/python%{python_version}/sqlite3
%dir %{_libdir}/python%{python_version}/lib-dynload
%{_libdir}/python%{python_version}/lib-dynload/_bsddb.so
%{_libdir}/python%{python_version}/lib-dynload/_hashlib.so
%{_libdir}/python%{python_version}/lib-dynload/_sqlite3.so
%{_libdir}/python%{python_version}/lib-dynload/_ssl.so
%{_libdir}/python%{python_version}/lib-dynload/readline.so
%defattr(644, root, root, 755)
%config %{_sysconfdir}/rpm/macros.python
%doc %{_mandir}/man1/python.1*
%doc %{_mandir}/man1/python%{python_version}.1*
%dir %{_includedir}/python%{python_version}
%{_includedir}/python%{python_version}/pyconfig.h
%{_libdir}/python
%dir %{_prefix}/lib/python%{python_version}
%dir %{_prefix}/lib/python%{python_version}/site-packages
%dir %{_libdir}/python%{python_version}
%dir %{_libdir}/python%{python_version}/config
%{_libdir}/python%{python_version}/config/Setup
%{_libdir}/python%{python_version}/config/Makefile
%{_libdir}/python%{python_version}/*.*
%{_libdir}/python%{python_version}/compiler
%{_libdir}/python%{python_version}/ctypes
%{_libdir}/python%{python_version}/distutils
%{_libdir}/python%{python_version}/email
%{_libdir}/python%{python_version}/encodings
%{_libdir}/python%{python_version}/hotshot
%{_libdir}/python%{python_version}/importlib
%{_libdir}/python%{python_version}/json
%{_libdir}/python%{python_version}/lib2to3
%{_libdir}/python%{python_version}/logging
%{_libdir}/python%{python_version}/multiprocessing
%{_libdir}/python%{python_version}/plat-*
%{_libdir}/python%{python_version}/pydoc_data
%{_libdir}/python%{python_version}/unittest
%{_libdir}/python%{python_version}/wsgiref
%dir %{_libdir}/python%{python_version}/site-packages
%{_libdir}/python%{python_version}/site-packages/README
%{_libdir}/python%{python_version}/site-packages/_local.pth
%dir %{_libdir}/python%{python_version}/lib-dynload
%{_libdir}/python%{python_version}/lib-dynload/_bisect.so
%{_libdir}/python%{python_version}/lib-dynload/_csv.so
%{_libdir}/python%{python_version}/lib-dynload/_collections.so
%{_libdir}/python%{python_version}/lib-dynload/_ctypes.so
%{_libdir}/python%{python_version}/lib-dynload/_ctypes_test.so
%{_libdir}/python%{python_version}/lib-dynload/_elementtree.so
%{_libdir}/python%{python_version}/lib-dynload/_functools.so
%{_libdir}/python%{python_version}/lib-dynload/_heapq.so
%{_libdir}/python%{python_version}/lib-dynload/_hotshot.so
%{_libdir}/python%{python_version}/lib-dynload/_io.so
%{_libdir}/python%{python_version}/lib-dynload/nis.so
%{_libdir}/python%{python_version}/lib-dynload/_json.so
%{_libdir}/python%{python_version}/lib-dynload/_locale.so
%{_libdir}/python%{python_version}/lib-dynload/_lsprof.so
%{_libdir}/python%{python_version}/lib-dynload/audioop.so
%{_libdir}/python%{python_version}/lib-dynload/dbm.so
#%{_libdir}/python%{python_version}/lib-dynload/_md5.so
%{_libdir}/python%{python_version}/lib-dynload/_multiprocessing.so
%{_libdir}/python%{python_version}/lib-dynload/_random.so
#%{_libdir}/python%{python_version}/lib-dynload/_sha.so
#%{_libdir}/python%{python_version}/lib-dynload/_sha256.so
#%{_libdir}/python%{python_version}/lib-dynload/_sha512.so
%{_libdir}/python%{python_version}/lib-dynload/_socket.so
%{_libdir}/python%{python_version}/lib-dynload/_struct.so
%{_libdir}/python%{python_version}/lib-dynload/_testcapi.so
%{_libdir}/python%{python_version}/lib-dynload/array.so
%{_libdir}/python%{python_version}/lib-dynload/binascii.so
%{_libdir}/python%{python_version}/lib-dynload/bz2.so
%{_libdir}/python%{python_version}/lib-dynload/cPickle.so
%{_libdir}/python%{python_version}/lib-dynload/cStringIO.so
%{_libdir}/python%{python_version}/lib-dynload/cmath.so
%{_libdir}/python%{python_version}/lib-dynload/crypt.so
%{_libdir}/python%{python_version}/lib-dynload/datetime.so
%{_libdir}/python%{python_version}/lib-dynload/fcntl.so
%{_libdir}/python%{python_version}/lib-dynload/future_builtins.so
%{_libdir}/python%{python_version}/lib-dynload/grp.so
%{_libdir}/python%{python_version}/lib-dynload/itertools.so
%{_libdir}/python%{python_version}/lib-dynload/linuxaudiodev.so
%{_libdir}/python%{python_version}/lib-dynload/math.so
%{_libdir}/python%{python_version}/lib-dynload/mmap.so
%{_libdir}/python%{python_version}/lib-dynload/operator.so
%{_libdir}/python%{python_version}/lib-dynload/ossaudiodev.so
%{_libdir}/python%{python_version}/lib-dynload/parser.so
%{_libdir}/python%{python_version}/lib-dynload/resource.so
%{_libdir}/python%{python_version}/lib-dynload/select.so
%{_libdir}/python%{python_version}/lib-dynload/spwd.so
%{_libdir}/python%{python_version}/lib-dynload/strop.so
%{_libdir}/python%{python_version}/lib-dynload/syslog.so
%{_libdir}/python%{python_version}/lib-dynload/termios.so
%{_libdir}/python%{python_version}/lib-dynload/time.so
%{_libdir}/python%{python_version}/lib-dynload/unicodedata.so
%{_libdir}/python%{python_version}/lib-dynload/zlib.so
%{_libdir}/python%{python_version}/lib-dynload/_codecs*.so
%{_libdir}/python%{python_version}/lib-dynload/_multibytecodec.so
%{_libdir}/python%{python_version}/lib-dynload/Python-%{tarversion}-py%{python_version}.egg-info
# these modules don't support 64-bit arches (disabled by setup.py)
%ifnarch x86_64
# requires sizeof(int) == sizeof(long) == sizeof(char*)
%{_libdir}/python%{python_version}/lib-dynload/dl.so
%endif
%attr(755, root, root) %{_bindir}/pydoc
%attr(755, root, root) %{_bindir}/python
%attr(755, root, root) %{_bindir}/python%{python_version}
%attr(755, root, root) %{_bindir}/smtpd.py
%{_bindir}/python2
%exclude %{_bindir}/2to3

%post -n libpython -p /sbin/ldconfig

%postun -n libpython -p /sbin/ldconfig

%files -n python-devel
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/python%{python_version}/config/*
%exclude %{_libdir}/python%{python_version}/config/Setup
%exclude %{_libdir}/python%{python_version}/config/Makefile
%defattr(644, root, root, 755)
%{_libdir}/libpython*.so
%{_libdir}/pkgconfig/python-%{python_version}.pc
%{_libdir}/pkgconfig/python.pc
%{_libdir}/pkgconfig/python2.pc
%{_includedir}/python*
%exclude %{_includedir}/python%{python_version}/pyconfig.h
%{_libdir}/python%{python_version}/test
%defattr(755, root, root)
%{_bindir}/python-config
%{_bindir}/python2-config
%{_bindir}/python%{python_version}-config

%files -n python-xml
#%manifest %{name}.manifest
%defattr(644, root, root, 755)
%{_libdir}/python%{python_version}/xml
%{_libdir}/python%{python_version}/lib-dynload/pyexpat.so

%files -n libpython
#%manifest %{name}.manifest
%defattr(644, root, root)
%{_libdir}/libpython*.so.*
%changelog
