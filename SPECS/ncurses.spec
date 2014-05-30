#
# spec file for package ncurses
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

#


Name:           ncurses
#!BuildIgnore: terminfo
BuildRequires:  gcc-c++
BuildRequires:  pkg-config
%define terminfo() %{_datadir}/%{0}/%{1}
%define tabset()   %{_datadir}/%{0}/%{1}
Version:        5.9
Release:        0
Summary:        New curses Libraries
License:        MIT
Group:          Base/Libraries
Url:            http://invisible-island.net/ncurses/ncurses.html
Source0:        ncurses-%{version}.tar.gz
Source2:        handle.linux
Source4:        ncurses-rpmlintrc
Source6:        edit.sed
Source7:        baselibs.conf
Source1001: 	ncurses.manifest
%global         _sysconfdir /etc
%global         _miscdir    %{_datadir}/misc
%global         _incdir     %{_includedir}
%global         root        %{_tmppath}/%{name}-%{version}-store

%description
As soon as a text application needs to directly control its output to
the screen (if it wants to place the cursor at location (x,y) then
write text), ncurses is used. The panel and the forms libraries are
included in this package. These new libraries support color, special
characters, and panels.


%package -n ncurses-utils
Summary:        Tools using the new curses libraries
License:        MIT
Group:          Base/Utilities
Provides:       ncurses:%{_bindir}/tput

%description -n ncurses-utils
The ncurses based utilities are as follows:

clear -- emits clear-screen for current terminal

tabs -- set tabs on a terminal

toe   -- table of entries utility

tput  -- shell-script access to terminal capabilities.

tset  -- terminal-initialization utility

reset -- terminal initialization utility

%package -n terminfo-base
Summary:        A terminal descriptions database
License:        MIT
Group:          Base/Utilities
Provides:       ncurses:%{_datadir}/tabset

%description -n terminfo-base
This is the terminfo basic database, maintained in the ncurses package.
This database is the official successor to the 4.4BSD termcap file and
contains information about any known terminal. The ncurses library
makes use of this database to use terminals correctly.


%package -n libncurses
Summary:        The New curses Libraries
License:        MIT
Group:          Base/Libraries
Requires:       terminfo-base
Provides:       ncurses = %{version}
Obsoletes:      ncurses < %{version}
#Recommends:     ncurses-utils = %{version}

%description -n libncurses
The ncurses library is used by the most curses based terminal
applications for controling its output and input to the screen.


%package -n libncurses6
Summary:        The New curses Libraries
License:        MIT
Group:          Base/Libraries
Requires:       terminfo-base
Provides:       ncurses = 6.0

%description -n libncurses6 
The ncurses library is used by the most curses based terminal
applications for controling its output and input to the screen.

%package -n terminfo
Summary:        A terminal descriptions database
License:        Public-Domain
Group:          Base/Utilities

%description -n terminfo
This is the terminfo reference database, maintained in the ncurses
package. This database is the official successor to the 4.4BSD termcap
file and contains information about any known terminal. The ncurses
library makes use of this database to use terminals correctly. If you
just use the Linux console, xterm, and VT100, you probably will not
need this database -- a minimal /usr/share/terminfo tree for these
terminals is already included in the terminfo-base package.

%package -n ncurses-devel
Summary:        Include Files and Libraries mandatory for Development
License:        MIT
Group:          Base/Development
Provides:       ncurses:%{_incdir}/ncurses.h
Requires:       ncurses = %{version}-%{release}
Requires:       libncurses = %{version}-%{release}
Requires:       libncurses6 = %{version}-%{release}

%description -n ncurses-devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%prep
%setup -q -n ncurses-%{version}
cp %{SOURCE1001} .
rm -vf include/ncurses_dll.h
rm -vf mkdirs.sh
rm -vf tar-copy.sh
rm -vf mk-dlls.sh

%build
    cflags ()
    {
	local flag=$1; shift
	local var=$1; shift
	test -n "${flag}" -a -n "${var}" || return
	case "${!var}" in
	*${flag}*) return
	esac
	set -o noclobber
	case "$flag" in
	-Wl,*)
	    if echo 'int main () { return 0; }' | \
	       ${CC:-gcc} -Werror $flag -o /dev/null -xc - > /dev/null 2>&1 ; then
		eval $var=\${$var:+\$$var\ }$flag
	    fi
	    ;;
	*)
	    if ${CC:-gcc} -Werror $flag -S -o /dev/null -xc /dev/null > /dev/null 2>&1 ; then
		eval $var=\${$var:+\$$var\ }$flag
	    fi
	    if ${CXX:-g++} -Werror $flag -S -o /dev/null -xc++ /dev/null > /dev/null 2>&1 ; then
		eval $var=\${$var:+\$$var\ }$flag
	    fi
	esac
	set +o noclobber
    }

    test ! -f /.buildenv || . /.buildenv
       OPATH=$PATH
      FALLBK="xterm,linux,vt100,vt102"
	  CC=gcc
	 CXX=g++
    CFLAGS="${RPM_OPT_FLAGS} -pipe -D_REENTRANT"
    if [[ "$BUILD_BASENAME" = debug-* ]] ; then
	CFLAGS="${CFLAGS} -g -DTRACE"
    fi
    cflags -Wl,-O2                  LDFLAGS
    cflags -Wl,-Bsymbolic-functions LDFLAGS
    cflags -Wl,--hash-size=8599     LDFLAGS
    cflags -Wl,--as-needed          LDFLAGS
    CXXFLAGS=$CFLAGS
    test -n "$TERM" || TERM=linux
    GZIP="-9"
    #export CC CFLAGS CXX CXXFLAGS GZIP TERM LDFLAGS
    #
    # Detect 64bit architecures and be sure that
    # we use an unsigned long for chtype to be
    # backward compatible with ncurses 5.4
    #
    echo 'int main () { return !(sizeof(void*) >= 8); }' | gcc -x c -o test64 -
    if ./test64 ; then
	WITHCHTYPE="--with-chtype=long"
    else
	WITHCHTYPE=""
	CFLAGS="${CFLAGS} -D_LARGEFILE64_SOURCES -D_FILE_OFFSET_BITS=64"
    fi
    rm -f ./test64
    #
    # For security of some configure and install scripts
    #
    TMPDIR=$(mktemp -d /tmp/ncurses.XXXXXXXX) || exit 1
    trap 'rm -rf ${TMPDIR}' EXIT
    export TMPDIR
    #
    # No --enable-term-driver as this had crashed last time
    # in ncurses/tinfo/lib_setup.c due to the fact that
    # _nc_globals.term_driver was a NULL function pointer
    #
    # No --enable-tcap-names because we may have to recompile
    # programs or foreign programs won't work
    #
    # No --enable-safe-sprintf because this seems to
    # crash on some architectures
    #
    # No --enable-xmc-glitch because this seems to break yast2
    # on console/konsole (no magic cookie support on those?)
    #
    # No --with-termlib=tinfo because libncurses depend on
    # libtinfo (is linked with) and therefore there is no
    # advantage about splitting of a libtinfo (IMHO).
    #
    touch --reference=README config.sub config.guess
    %configure \
    --target=arm-linux \
	--with-build-cc=/usr/bin/gcc \
    --without-ada		\
	--without-debug		\
	--without-profile	\
	--without-manpage-tbl	\
	--with-shared		\
	--with-normal		\
	--with-manpage-format=gzip \
	--with-manpage-renames=${PWD}/man/man_db.renames \
	--with-manpage-aliases	\
	--with-ospeed=speed_t	\
	--with-gpm		\
	--with-dlsym		\
	--with-termlib=tinfo	\
	--with-ticlib=tic	\
	--with-xterm-kbs=del	\
	--disable-root-environ	\
	--disable-termcap	\
	--disable-overwrite	\
	--disable-rpath		\
	--disable-leaks		\
	--disable-xmc-glitch	\
	--enable-symlinks	\
	--enable-big-core	\
	--enable-const		\
	--enable-hashmap	\
	--enable-no-padding	\
	--enable-symlinks	\
	--enable-sigwinch	\
    --enable-pc-files \
    --with-pkg-config-libdir=%{_libdir}/pkgconfig \
    --with-pkg-config \
	--enable-colorfgbg	\
	--enable-sp-funcs	\
	--without-pthread	\
	--disable-reentrant	\
	--disable-ext-mouse	\
	--disable-widec		\
	--disable-ext-colors	\
	--enable-weak-symbols	\
	--enable-wgetch-events	\
	--enable-pthreads-eintr	\
	--enable-string-hacks	\
	--prefix=%{_prefix}	\
	--exec-prefix=%{_prefix}\
	--libdir=%{_libdir}	\
	--datadir=%{_datadir}	\
	--mandir=%{_mandir}	\
	--includedir=%{_incdir}	\
	"${WITHCHTYPE}" 	\
	--disable-widec		\
	--disable-tic-depends	\
	--with-ticlib=tic
    #--with-pkg-config-libdir=%{_libdir}/pkgconfig \
    #
    #  The configure line
    #
    c=$(grep '^ *$ *\./configure' config.log)
    #
    # This is a hack to be able to boot strap
    # a libncurses with correct fallback.c.
    #
    make %{?_smp_mflags} -C include
    make %{?_smp_mflags} -C ncurses fallback.c FALLBACK_LIST=""
    make %{?_smp_mflags} -C progs   termsort.c transform.h infocmp tic
    rm   -f ncurses/fallback.c
    PATH=$PWD/progs:$OPATH
    LD_LIBRARY_PATH=$PWD/lib
    export LD_LIBRARY_PATH PATH
    pushd ncurses/
	TERMINFO=$PWD/tmp
	export TERMINFO
	mkdir -p $TERMINFO
#%if 0%{?_crossbuild}
export BUILD_TIC=/usr/bin/tic
#%else
#export BUILD_TIC=$PWD/../progs/tic
#%endif
	$BUILD_TIC -I -r -e $FALLBK ../misc/terminfo.src > terminfo.src
	$BUILD_TIC -o $TERMINFO -s terminfo.src
	sh -e ./tinfo/MKfallback.sh $TERMINFO ../misc/terminfo.src $BUILD_TIC ${FALLBK//,/ } > fallback.c
	rm -rf $TERMINFO
	unset  TERMINFO
	cp -p fallback.c ../fallback.c.backup
    popd
    PATH=$OPATH
    unset LD_LIBRARY_PATH
    #
    # Refresh second install path
    #
    rm -rf %{root}
    mkdir  %{root}
    #
    # Now rebuild libncurses and do the rest of this job
    #
    find -name fallback.o | xargs -r rm -vf
    cp fallback.c.backup ncurses/fallback.c
    make %{?_smp_mflags}
    lib=%{_libdir}
    inc=%{_incdir}/ncurses
    # must not use %jobs here (would lead to: ln: ncurses.h already exists)
    make install DESTDIR=%{root} includedir=${inc} libdir=${lib}
    ln -sf ${inc##*/}/{curses,ncurses,term,termcap}.h %{root}${inc%%/*}/
    sh %{S:6} --cflags "-I${inc}" --libs "-lncurses" --libs "-ltinfo" %{root}%{_bindir}/ncurses5-config
    #
    # Now use --with-pthread for reentrant pthread support (abi > 5).
    #
    eval ./${c#*./} --with-pthread --enable-reentrant --enable-ext-mouse --disable-widec --disable-ext-colors --without-progs
    find -name fallback.o | xargs -r rm -vf
    cp fallback.c.backup ncurses/fallback.c
    make %{?_smp_mflags}
    lib=%{_libdir}/ncurses6
    inc=%{_incdir}/ncurses6/ncurses
    # must not use %jobs here (would lead to: ln: ncurses.h already exists)
    make install.libs install.includes DESTDIR=%{root} includedir=${inc} libdir=${lib}
    ln -sf ${inc##*/}/{curses,ncurses,term}.h %{root}${inc%%/*}/
    sh %{S:6} --cflags "-I${inc} -I${inc%%/*}" --libs "-L${lib} -lncurses" --libs "-ltinfo" %{root}%{_bindir}/ncurses6-config
    pushd man
	sh ../edit_man.sh normal installing %{root}%{_mandir} . ncurses6-config.1
    popd
    #
    # Now use --enable-widec for UTF8/wide character support.
    # The libs with 16 bit wide characters are binary incompatible
    # to the normal 8bit wide character libs.
    #
    eval ./${c#*./} --disable-ext-mouse --enable-widec --disable-ext-colors --without-progs
    find -name fallback.o | xargs -r rm -vf
    cp fallback.c.backup ncurses/fallback.c
    make %{?_smp_mflags}
    lib=%{_libdir}
    inc=%{_incdir}/ncursesw
    # must not use %jobs here (would lead to: ln: ncurses.h already exists)
    make install.libs install.includes DESTDIR=%{root} includedir=${inc} libdir=${lib}
    sh %{S:6} --cflags "-I${inc}" --libs "-lncursesw" --libs "-ltinfo" %{root}%{_bindir}/ncursesw5-config
    pushd man
	sh ../edit_man.sh normal installing %{root}%{_mandir} . ncursesw5-config.1
    popd
    #
    # Do both --enable-widec and --with-pthread (abi > 5).
    #
    eval ./${c#*./} --with-pthread --enable-reentrant --enable-ext-mouse --enable-widec --enable-ext-colors --without-progs
    find -name fallback.o | xargs -r rm -vf
    cp fallback.c.backup ncurses/fallback.c
    make %{?_smp_mflags}
    lib=%{_libdir}/ncurses6
    inc=%{_incdir}/ncurses6/ncursesw
    # must not use %jobs here (would lead to: ln: ncurses.h already exists)
    make install.libs install.includes DESTDIR=%{root} includedir=${inc} libdir=${lib}
    sh %{S:6} --cflags "-I${inc} -I${inc%%/*}" --libs "-L${lib} -lncursesw" --libs "-ltinfo" %{root}%{_bindir}/ncursesw6-config
    pushd man
	sh ../edit_man.sh normal installing %{root}%{_mandir} . ncursesw6-config.1
    popd

%install
    GZIP="-9"
    export GZIP
    (cd %{root}/; tar -cpSf - *)|tar -xpsSf - -C %{buildroot}/
    rm -rf %{root}
    #mkdir -p %{buildroot}/%{_lib}
    for model in libncurses libncursest libncursesw libncursestw libtinfo
    do
	#for lib in %{buildroot}%{_libdir}/${model}.so.* ; do
	#    test   -e "${lib}" || continue
	#    mv "${lib}" %{buildroot}/%{_lib}/ || continue
	#done
	for lib in %{buildroot}/%{_libdir}/${model}.so.5 ; do
	    test -e "${lib}" || continue
	    test -L "${lib}" || continue
	    lib=${lib#%{buildroot}}
	    lnk=%{buildroot}%{_libdir}/${model}.so
	    case "${lib##*/}" in
	    libncurses*)
		rm -f ${lnk}
		echo '/* GNU ld script */'		>  ${lnk}
		echo "INPUT(${lib} AS_NEEDED(-ltinfo))" >> ${lnk}
		;;
	    #*)	ln -sf ${lib} %{buildroot}%{_libdir}/${model}.so
	    esac
	done
    done
    chmod 0755 %{buildroot}/%{_libdir}/lib*.so.*
    chmod 0755 %{buildroot}/%{_libdir}/lib*.so.*
    chmod a-x  %{buildroot}/%{_libdir}/lib*.a
    if test -d %{buildroot}%{_libdir}/ncurses6 ; then
	mv %{buildroot}%{_libdir}/ncurses6/*.so.6*   %{buildroot}%{_libdir}/
	for lib in %{buildroot}%{_libdir}/ncurses6/*.so
	do
	    lnk=$lib
	    lib=/%{_libdir}/${lib##*/}.6
	    case "${lib##*/}" in
	    libncurses*)
		rm -f "${lnk}"
		echo '/* GNU ld script */'		>  ${lnk}
		echo "INPUT(${lib} AS_NEEDED(-ltinfo))"	>> ${lnk} 
		;;
	    libtinfo*)
		test -L "${lnk}" || continue
		ln -sf ${lib} ${lnk}
		;;
	    *)
		test -L "${lnk}" || continue
		ln -sf ../${lib##*/} ${lnk}
	    esac
	done
	for model in libncurses libncursest libncursesw libncursestw libtinfo
	do
	    for lib in %{buildroot}%{_libdir}/${model}.so.* ; do
		test   -e "${lib}" || continue
		#mv "${lib}" %{buildroot}/%{_lib}/ || continue
	    done
	    for lib in %{buildroot}/%{_libdir}/${model}.so.6 ; do
		test -e "${lib}" || continue
		test -L "${lib}" || continue
		lib=${lib#%{buildroot}}
		lnk=%{buildroot}%{_libdir}/ncurses6/${model}.so
		case "${lib##*/}" in
		libncurses*)
		    rm -f ${lnk}
		    echo '/* GNU ld script */'		    >  ${lnk}
		    echo 'SEARCH_DIR(%{_libdir}/ncurses6)'  >> ${lnk}
		    echo "INPUT(${lib} AS_NEEDED(-ltinfo))" >> ${lnk}
		    ;;
		*)  : #ln -sf ${lib} %{buildroot}%{_libdir}/ncurses6/${model}.so
	    esac
	    done
	done
	chmod 0755 %{buildroot}/%{_libdir}/lib*.so.6*
	chmod 0755 %{buildroot}/%{_libdir}/lib*.so.6*
	chmod a-x  %{buildroot}/%{_libdir}/ncurses6/lib*.a
    fi
    test -n "%{buildroot}" || ldconfig -N
    mkdir -p %{buildroot}%{_defaultdocdir}/ncurses
    bzip2 -c misc/terminfo.src > misc/terminfo.src.bz2
    install -m 644 misc/terminfo.src.bz2	%{buildroot}%{_defaultdocdir}/ncurses/
    install -m 644 doc/html/*.html		%{buildroot}%{_defaultdocdir}/ncurses/
    bzip2 doc/ncurses-intro.doc -c > doc/ncurses-intro.txt.bz2
    install -m 644 doc/ncurses-intro.txt.bz2	%{buildroot}%{_defaultdocdir}/ncurses/
    bzip2 doc/hackguide.doc -c > doc/hackguide.txt.bz2
    install -m 644 doc/hackguide.txt.bz2	%{buildroot}%{_defaultdocdir}/ncurses/
    install -m 644 README			%{buildroot}%{_defaultdocdir}/ncurses/
    install -m 644 NEWS				%{buildroot}%{_defaultdocdir}/ncurses/
    mkdir -p %{buildroot}%{_sysconfdir}
    mkdir -p %{buildroot}%{_miscdir}
    LD_LIBRARY_PATH=$PWD/lib
    export LD_LIBRARY_PATH
    pushd ncurses/
	{ echo "# See annotated version in %{_defaultdocdir}/ncurses/terminfo.src.bz2"
#%if 0%{?_crossbuild}
	BUILD_TIC=/usr/bin/tic
#%else
#	BUILD_TIC=$PWD/../progs/tic
#%endif
	$BUILD_TIC -C -r ../misc/terminfo.src | grep -E -v '^#'; } > termcap
	# Gererate new termcap entries for various linux consoles
	TERMCAP=termcap \
	TERMINFO=%{buildroot}%{_datadir}/terminfo \
	    bash %{SOURCE2}
	install -m 0644 termcap.new %{buildroot}%{_miscdir}/termcap
    popd
    unset LD_LIBRARY_PATH
    if test `%{_bindir}/id -u` = '0' ; then
	chown root:root %{buildroot}%{_miscdir}/termcap
	chmod 0644      %{buildroot}%{_miscdir}/termcap
    fi
    ln -sf %{_miscdir}/termcap %{buildroot}%{_sysconfdir}/termcap
    (cat > default.list) <<-EOF
	%{tabset std}
	%{tabset stdcrt}
	%{tabset vt100}
	%{tabset vt300}
	%{terminfo a/ansi}
	%{terminfo d/dumb}
	%{terminfo g/gnome}
	%{terminfo g/gnome-rh72}
	%{terminfo k/klone+color}
	%{terminfo k/kvt}
	%{terminfo l/linux}
	%{terminfo l/linux-m}
	%{terminfo l/linux-nic}
	%{terminfo m/mlterm}
	%{terminfo n/nxterm}
	%{terminfo r/rxvt}
	%{terminfo s/screen}
	%{terminfo s/screen-w}
	%{terminfo s/screen-256color}
	%{terminfo s/sun}
	%{terminfo u/unknown}
	%{terminfo v/vt100}
	%{terminfo v/vt102}
	%{terminfo v/vt220}
	%{terminfo v/vt220-8}
	%{terminfo v/vt220-8bit}
	%{terminfo v/vt320}
	%{terminfo v/vt52}
	%{terminfo x/xterm}
	%{terminfo x/xterm-color}
	%{terminfo x/xterm-256color}
	%{terminfo x/xterm-basic}
	%{terminfo x/xterm-nic}
	%{terminfo x/xterm-r6}
	EOF
    find %{buildroot}%{tabset ""} %{buildroot}%{terminfo ""} \
	\( -type f -or -type l \) | \
	sed "s@^%{buildroot}@@g" | \
	grep -v -F -x -f default.list \
	> extension.list
    rm -f %{buildroot}%{_prefix}/lib/terminfo

%post   -n libncurses -p /sbin/ldconfig

%postun -n libncurses -p /sbin/ldconfig

%post   -n libncurses6 -p /sbin/ldconfig

%postun -n libncurses6 -p /sbin/ldconfig

%files -n terminfo-base -f default.list
#%manifest %{name}.manifest
%defattr(-,root,root)
%{_sysconfdir}/termcap
%config %{_miscdir}/termcap
%dir %{_datadir}/tabset/
%dir %{_datadir}/terminfo/
%dir %{_datadir}/terminfo/*/

%files -n ncurses-utils
#%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/clear
%{_bindir}/reset
%{_bindir}/tabs
%{_bindir}/toe
%{_bindir}/tput
%{_bindir}/tset

%files -n libncurses
#%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/lib*.so.5*

%files -n libncurses6
#%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/lib*.so.6*

%files -n ncurses-devel
#%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/ncurses*-config
%{_bindir}/captoinfo
%{_bindir}/infocmp
%{_bindir}/infotocap
%{_bindir}/tic
%dir %{_incdir}/ncurses/
%dir %{_incdir}/ncursesw/
%dir %{_incdir}/ncurses6/
%dir %{_incdir}/ncurses6/ncurses/
%dir %{_incdir}/ncurses6/ncursesw/
%{_incdir}/*.h
%{_incdir}/ncurses*/*.h
%{_incdir}/ncurses*/*/*.h
%dir %{_libdir}/ncurses6/
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/ncurses6/lib*.a
%{_libdir}/ncurses6/lib*.so

%files -f extension.list -n terminfo
#%manifest %{name}.manifest
%defattr(-,root,root)

%docs_package
%dir %{_defaultdocdir}/ncurses/
%doc %{_defaultdocdir}/ncurses/*

%changelog
