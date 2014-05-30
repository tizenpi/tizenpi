Name:           gcc
%define separate_bi32 0
%define separate_bi64 0
%ifarch ppc
%define separate_bi64 1
%endif
%ifarch x86_64 s390x ppc64
%define separate_bi32 1
%endif
Url:            http://gcc.gnu.org/
%define gcc_version 48
%define gcc_suffix 4.8
Version:        4.8
Release:        0
VCS:            platform/upstream/gcc#submit/tizen/20130710.130950-0-g53ff3a85824df4cdadecc563ddb81c5a021bcc0b
Summary:        The system GNU C Compiler
License:        GPL-3.0+
Group:          Development/Toolchain
Provides:       c_compiler
Obsoletes:      gcc-mudflap
Requires:       cpp
Requires:       gcc%{gcc_version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source:         cpp
Source99:       README.packaging

%description
The system GNU C Compiler.



%package -n gcc-32bit
Summary:        The system GNU C Compiler
License:        GPL-3.0+
Requires:       gcc = %{version}
Requires:       gcc%{gcc_version}-32bit

%description -n gcc-32bit
The system GNU C Compiler.



%package -n gcc-64bit
Summary:        The system GNU C Compiler
License:        GPL-3.0+
Requires:       gcc = %{version}
Requires:       gcc%{gcc_version}-64bit

%description -n gcc-64bit
The system GNU C Compiler.



%package -n cpp
Summary:        The system GNU Preprocessor
License:        GPL-3.0+
Requires:       cpp%{gcc_version}

%description -n cpp
The system GNU Preprocessor.



%package -n gcc-locale
Summary:        The system GNU Compiler locale files
License:        GPL-3.0+
Requires:       gcc%{gcc_version}-locale

%description -n gcc-locale
The system GNU Compiler locale files.



%package -n gcc-info
Summary:        The system GNU Compiler documentation
License:        GFDL-1.2
Requires:       gcc%{gcc_version}-info

%description -n gcc-info
The system GNU Compiler documentation.

# There is intentionally no postun with install_info_delete as there
# is no way to just remove the aliased entries.  The content owners
# install_info_delete will also remove the aliases though.
# install-info does not pick up descriptions from the content.

%package -n gcc-c++
Summary:        The system GNU C++ Compiler
License:        GPL-3.0+
Provides:       c++_compiler
Requires:       gcc = %{version}
Requires:       gcc%{gcc_version}-c++

%description -n gcc-c++
The system GNU C++ Compiler.


%package -n gcc-c++-32bit
Summary:        The system GNU C++ Compiler
License:        GPL-3.0+
Requires:       gcc-32bit = %{version}
Requires:       gcc-c++ = %{version}
Requires:       libstdc++%{gcc_version}-devel-32bit

%description -n gcc-c++-32bit
The system GNU C++ Compiler 32 bit support.


%package -n gcc-c++-64bit
Summary:        The system GNU C++ Compiler
License:        GPL-3.0+
Requires:       gcc-64bit = %{version}
Requires:       gcc-c++ = %{version}
Requires:       libstdc++%{gcc_version}-devel-64bit

%description -n gcc-c++-64bit
The system GNU C++ Compiler 64 bit support.



%package -n libstdc++-devel
Summary:        The system GNU C++ development files
License:        GPL-3.0-with-GCC-exception
Requires:       libstdc++%{gcc_version}-devel

%description -n libstdc++-devel
The system GNU C++ development files.



%package -n gcc-fortran
Summary:        The system GNU Fortran Compiler
License:        GPL-3.0+
Requires:       gcc = %{version}
Requires:       gcc%{gcc_version}-fortran

%description -n gcc-fortran
The system GNU Fortran Compiler.


%package -n gcc-fortran-32bit
Summary:        The system GNU Fortran Compiler
License:        GPL-3.0+
Requires:       gcc%{gcc_version}-fortran-32bit
Requires:       gcc-fortran = %{version}

%description -n gcc-fortran-32bit
The system GNU Fortran Compiler 32 bit support.


%package -n gcc-fortran-64bit
Summary:        The system GNU Fortran Compiler
License:        GPL-3.0+
Requires:       gcc%{gcc_version}-fortran-64bit
Requires:       gcc-fortran = %{version}

%description -n gcc-fortran-64bit
The system GNU Fortran Compiler 64 bit support.


%package -n gcc-java
Summary:        The system GNU Java Compiler
License:        GPL-3.0+
Requires:       gcc%{gcc_version}-java
Requires:       libgcj-devel = %{version}
#Recommends:     gcc-gij = %{version}
Requires:       gcc = %{version}

%description -n gcc-java
The system GNU Java Compiler.



%package -n libgcj-devel
Summary:        The system GNU Java development files.
License:        GPL-2.0-with-classpath-exception
Requires:       libgcj%{gcc_version}-devel

%description -n libgcj-devel
The system GNU Java development files.



%package -n gcc-gij
Summary:        The system GNU Java bytecode interpreter
License:        GPL-2.0+
Requires:       gcc%{gcc_version}-gij

%description -n gcc-gij
The system GNU Java bytecode interpreter.



%package -n gcc-gij-32bit
Summary:        The system GNU Java bytecode interpreter
License:        GPL-2.0+
Requires:       gcc%{gcc_version}-gij-32bit

%description -n gcc-gij-32bit
The system GNU Java bytecode interpreter as 32 bit application.



%package -n gcc-gij-64bit
Summary:        The system GNU Java bytecode interpreter
License:        GPL-2.0+
Requires:       gcc%{gcc_version}-gij-64bit

%description -n gcc-gij-64bit
The system GNU Java bytecode interpreter as 64 bit application.



%package -n gcc-objc
Summary:        The system GNU Objective C Compiler
License:        GPL-3.0+
Requires:       gcc = %{version}
Requires:       gcc%{gcc_version}-objc
%ifarch ppc64
Obsoletes:      gcc-objc-64bit
%endif

%description -n gcc-objc
The system GNU Objective C Compiler.



%package -n gcc-objc-32bit
Summary:        The system GNU Objective C Compiler
License:        GPL-3.0+
Requires:       gcc%{gcc_version}-objc-32bit
Requires:       gcc-objc = %{version}

%description -n gcc-objc-32bit
The system GNU Objective C Compiler 32 bit support.



%package -n gcc-objc-64bit
Summary:        The system GNU Objective C Compiler
License:        GPL-3.0+
Requires:       gcc%{gcc_version}-objc-64bit
Requires:       gcc-objc = %{version}

%description -n gcc-objc-64bit
The system GNU Objective C Compiler 64 bit support.



%package -n gcc-obj-c++
Summary:        The system GNU Objective C++ Compiler
License:        GPL-3.0+
Requires:       gcc%{gcc_version}-obj-c++
Requires:       gcc-objc = %{version}

%description -n gcc-obj-c++
The system GNU Objective C++ Compiler.



%package -n gcc-ada
Summary:        The system GNU Ada Compiler
License:        GPL-3.0+
Requires:       gcc = %{version}
Requires:       gcc%{gcc_version}-ada

%description -n gcc-ada
The system GNU Ada Compiler.


%package -n gcc-z9
Summary:        The system GNU C Compiler
License:        GPL-3.0+
Requires:       gcc

%description -n gcc-z9
The system GNU C Compiler.


%prep 

%build
echo "This is a dummy package to provide a dependency on the system compiler." > README

%install
mkdir -p $RPM_BUILD_ROOT/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/doc/packages/gcc-objc/
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/doc/packages/gcc-obj-c++/
# Link all the binaries
for program in \
        gcc gcov \
        g++ \
        cpp \
	gcj gcjh gcj-dbtool jcf-dump jv-convert gc-analyze \
	gij \
	gappletviewer \
	gjar gjarsigner gjavah gkeytool gnative2ascii gorbd grmic \
	grmid grmiregistry gserialver gtnameserv \
%if %{separate_bi32}
	grmiregistry32 \
	gij32 \
%endif
%if %{separate_bi64}
	grmiregistry64 \
	gij64 \
%endif
        gfortran \
	gnat gnatbind gnatbl gnatchop gnatclean gnatfind gnatkr \
	gnatlink gnatls gnatmake gnatname gnatprep gnatxref gprmake \
    ; do
  ln -sf $program-%{gcc_suffix} $RPM_BUILD_ROOT%{_prefix}/bin/$program
done
# Link section 1 manpages
for man1 in \
        gcc gcov \
        g++ \
        cpp \
        gfortran \
	gcj gcjh gcj-dbtool jcf-dump jv-convert gc-analyze \
	gij \
	gappletviewer gjar gjarsigner gjavah \
	gkeytool gnative2ascii gorbd grmic grmid grmiregistry gserialver \
	gtnameserv \
    ; do
  ln -sf $man1-%{gcc_suffix}.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/$man1.1.gz
done
# Provide the traditional /lib/cpp that only handles C
cp $RPM_SOURCE_DIR/cpp $RPM_BUILD_ROOT/lib/
chmod 755 $RPM_BUILD_ROOT/lib/cpp
# Provide extra symlinks
ln -sf g++-%{gcc_suffix} $RPM_BUILD_ROOT%{_prefix}/bin/c++
ln -sf gcc-%{gcc_suffix} $RPM_BUILD_ROOT%{_prefix}/bin/cc
ln -sf g++-%{gcc_suffix}.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/c++.1.gz
ln -sf gcc-%{gcc_suffix}.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/cc.1.gz
%ifarch s390 s390x
dir=`gcc-%{gcc_suffix} -print-prog-name=cc1`
dir=${dir%/cc1}
mkdir -p $RPM_BUILD_ROOT/$dir
cat > $RPM_BUILD_ROOT/$dir/defaults.spec <<EOF
*default_spec:
%{!mtune=*:-mtune=z10} %{!march=*:-march=z9-109}
EOF
%endif

%files
%defattr(-,root,root)
%{_prefix}/bin/gcc
%{_prefix}/bin/cc
%{_prefix}/bin/gcov
%doc %{_mandir}/man1/gcc.1.gz
%doc %{_mandir}/man1/cc.1.gz
%doc %{_mandir}/man1/gcov.1.gz

%files -n cpp
%defattr(-,root,root)
/lib/cpp
%{_prefix}/bin/cpp
%doc %{_mandir}/man1/cpp.1.gz

%files -n gcc-c++
%defattr(-,root,root)
%{_prefix}/bin/g++
%{_prefix}/bin/c++
%doc %{_mandir}/man1/g++.1.gz
%doc %{_mandir}/man1/c++.1.gz

%files -n gcc-fortran
%defattr(-,root,root)
%{_prefix}/bin/gfortran
%doc %{_mandir}/man1/gfortran.1.gz

%files -n gcc-java
%defattr(-,root,root)
%{_prefix}/bin/gcj
%{_prefix}/bin/gcjh
%{_prefix}/bin/gcj-dbtool
%{_prefix}/bin/jcf-dump
%{_prefix}/bin/jv-convert
%{_prefix}/bin/gc-analyze
%doc %{_mandir}/man1/gcj.1.gz
%doc %{_mandir}/man1/gcjh.1.gz
%doc %{_mandir}/man1/gcj-dbtool.1.gz
%doc %{_mandir}/man1/jcf-dump.1.gz
%doc %{_mandir}/man1/jv-convert.1.gz
%doc %{_mandir}/man1/gc-analyze.1.gz

%files -n gcc-gij
%defattr(-,root,root)
%{_prefix}/bin/gij
%{_prefix}/bin/gappletviewer
%{_prefix}/bin/gjar
%{_prefix}/bin/gjarsigner
%{_prefix}/bin/gjavah
%{_prefix}/bin/gkeytool
%{_prefix}/bin/gnative2ascii
%{_prefix}/bin/gorbd
%{_prefix}/bin/grmic
%{_prefix}/bin/grmid
%{_prefix}/bin/grmiregistry
%{_prefix}/bin/gserialver
%{_prefix}/bin/gtnameserv
%doc %{_mandir}/man1/gij.1.gz
%doc %{_mandir}/man1/gappletviewer.1.gz
%doc %{_mandir}/man1/gjar.1.gz
%doc %{_mandir}/man1/gjarsigner.1.gz
%doc %{_mandir}/man1/gjavah.1.gz
%doc %{_mandir}/man1/gkeytool.1.gz
%doc %{_mandir}/man1/gnative2ascii.1.gz
%doc %{_mandir}/man1/gorbd.1.gz
%doc %{_mandir}/man1/grmic.1.gz
%doc %{_mandir}/man1/grmid.1.gz
%doc %{_mandir}/man1/grmiregistry.1.gz
%doc %{_mandir}/man1/gserialver.1.gz
%doc %{_mandir}/man1/gtnameserv.1.gz

%files -n gcc-objc
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-obj-c++
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-locale
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-info
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-ada
%defattr(-,root,root)
%{_prefix}/bin/gnat
%{_prefix}/bin/gnatbind
%{_prefix}/bin/gnatbl
%{_prefix}/bin/gnatchop
%{_prefix}/bin/gnatclean
%{_prefix}/bin/gnatfind
%{_prefix}/bin/gnatkr
%{_prefix}/bin/gnatlink
%{_prefix}/bin/gnatls
%{_prefix}/bin/gnatmake
%{_prefix}/bin/gnatname
%{_prefix}/bin/gnatprep
%{_prefix}/bin/gnatxref
%{_prefix}/bin/gprmake

%files -n libstdc++-devel
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n libgcj-devel
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%if %{separate_bi32}

%files -n gcc-32bit
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-c++-32bit
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-fortran-32bit
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-objc-32bit
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-gij-32bit
%defattr(-,root,root)
%{_prefix}/bin/gij32
%{_prefix}/bin/grmiregistry32

%endif
%if %{separate_bi64}

%files -n gcc-64bit
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-c++-64bit
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-fortran-64bit
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-objc-64bit
%defattr(-,root,root)
# empty - only for the dependency
%doc README

%files -n gcc-gij-64bit
%defattr(-,root,root)
%{_prefix}/bin/gij64
%{_prefix}/bin/grmiregistry64

%endif
%ifarch s390 s390x

%files -n gcc-z9
%defattr(-,root,root)
/usr/lib*/gcc/*-suse-linux/*/defaults.spec
%endif

%changelog
