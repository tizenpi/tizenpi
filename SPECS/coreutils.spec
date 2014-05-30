Name:           coreutils
Version:        8.21
Summary:        GNU Core Utilities
License:        GPL-3.0+
Group:          Base/Utilities
BuildRequires:  automake
BuildRequires:  gmp-devel
BuildRequires:  help2man
BuildRequires:  libacl-devel
BuildRequires:  libcap-devel
BuildRequires:  smack-devel
BuildRequires:  pam-devel
BuildRequires:  xz
BuildRequires:  gettext-tools
BuildRequires:  bison
BuildRequires:  gperf
BuildRequires:  makeinfo
Url:            http://www.gnu.org/software/coreutils/
Release:        0
Provides:       fileutils = %{version}
Provides:       mktemp = %{version}
Provides:       sh-utils = %{version}
Provides:       stat = %version}
Provides:       textutils = %{version}
Obsoletes:      fileutils < %{version}
Obsoletes:      mktemp < %{version}
Obsoletes:      sh-utils < %{version}
Obsoletes:      stat < %version}
Obsoletes:      textutils < %{version}
Requires:       pam >= 1.1.1.90
Source:         coreutils-%{version}.tar.xz
Source3:        baselibs.conf
Source4:        gnulib.tar.bz2
Source5:        po.tar.bz2
Source1001: 	coreutils.manifest
Provides:       /bin/basename
Provides:       /bin/cat
Provides:       /bin/chmod
Provides:       /bin/chown
Provides:       /bin/cp
Provides:       /bin/ln
Provides:       /bin/ls
Provides:       /bin/mkdir
Provides:       /bin/mv
Provides:       /bin/pwd
Provides:       /bin/rm
Provides:       /bin/sort
Provides:       /bin/touch

%description
Basic file, shell, and text manipulation utilities.  The package
contains the following programs:

[ arch base64 basename cat chcon chgrp chmod chown chroot cksum comm cp
csplit cut date dd df dir dircolors dirname du echo env expand expr
factor false fmt fold groups head id install join kill link ln logname
ls md5sum mkdir mkfifo mknod mktemp mv nice nl nohup od paste pathchk
pinky pr printenv printf ptx pwd readlink rm rmdir runcon seq sha1sum
sha224sum sha256sum sha384sum sha512sum shred shuf sleep sort split
stat stty sum sync tac tail tee test timeout touch tr true tsort tty
uname unexpand uniq unlink uptime users vdir wc who whoami yes


%prep
%setup -q -a 4 -a 5
cp %{SOURCE1001} .

%build
./bootstrap --no-git --gnulib-srcdir=gnulib --skip-po --no-bootstrap-sync
#AUTOPOINT=true autoreconf -fi
export CFLAGS="%optflags -Wall"
%configure --libexecdir=%{_libdir} --without-included-regex \
  	    --enable-install-program=arch \
	    --enable-no-install-program=uptime \
	    --enable-libsmack=yes \
	    gl_cv_func_printf_directive_n=yes \
	    gl_cv_func_isnanl_works=yes \
  	    DEFAULT_POSIX2_VERSION=199209

make -C po update-po
make %{?_smp_mflags} V=1

%install
%make_install pkglibexecdir=%{_libdir}/%{name}
echo '.so man1/test.1' > %{buildroot}/%{_mandir}/man1/\[.1

%find_lang %name

%lang_package

%files
#%manifest %{name}.manifest
%defattr(-,root,root)
%doc README NEWS
%license COPYING
%{_bindir}/*
%{_libdir}/%{name}
%dir %{_prefix}/share/locale/*/LC_TIME

%docs_package


%changelog
