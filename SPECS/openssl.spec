Name:           openssl
BuildRequires:  bc
BuildRequires:  ed
BuildRequires:  pkg-config
BuildRequires:  zlib-devel
%define ssletcdir %{_sysconfdir}/ssl
%define num_version 1.0.0
Provides:       ssl
Version:        1.0.1g
Release:        0
Summary:        Secure Sockets and Transport Layer Security
License:        OpenSSL
Group:          Security/Crypto Libraries
Url:            http://www.openssl.org/
Source:         http://www.%{name}.org/source/%{name}-%{version}.tar.gz
# to get mtime of file:
Source1:        openssl.changes
Source2:        baselibs.conf
Source1001: 	openssl.manifest

%description
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, full-featured, and open source toolkit implementing
the Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS
v1) protocols with full-strength cryptography. The project is managed
by a worldwide community of volunteers that use the Internet to
communicate, plan, and develop the OpenSSL toolkit and its related
documentation.

Derivation and License

OpenSSL is based on the excellent SSLeay library developed by Eric A.
Young and Tim J. Hudson. The OpenSSL toolkit is licensed under an
Apache-style license, which basically means that you are free to get it
and to use it for commercial and noncommercial purposes.

%package -n libopenssl
Summary:        Secure Sockets and Transport Layer Security
Group:          Security/Crypto Libraries

%description -n libopenssl
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, full-featured, and open source toolkit implementing
the Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS
v1) protocols with full-strength cryptography. The project is managed
by a worldwide community of volunteers that use the Internet to
communicate, plan, and develop the OpenSSL toolkit and its related
documentation.

Derivation and License

OpenSSL is based on the excellent SSLeay library developed by Eric A.
Young and Tim J. Hudson. The OpenSSL toolkit is licensed under an
Apache-style license, which basically means that you are free to get it
and to use it for commercial and noncommercial purposes.


%package -n libopenssl-devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Obsoletes:      openssl-devel < %{version}
Requires:       %name = %version
Requires:       libopenssl = %{version}
Requires:       zlib-devel
Provides:       openssl-devel = %{version}

%description -n libopenssl-devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%package misc
Summary:        Additional data files and scripts for %{name}
Group:          Security/Crypto Libraries

%description misc
Additional data files and scripts for %{name}.

%package doc
Summary:        Additional Package Documentation
Group:          Security/Crypto Libraries
BuildArch:      noarch

%description doc
This package contains optional documentation provided in addition to
this package's base documentation.

%prep
%setup -q
cp %{SOURCE1001} .
echo "adding/overwriting some entries in the 'table' hash in Configure"
# $dso_scheme:$shared_target:$shared_cflag:$shared_ldflag:$shared_extension:$ranlib:$arflags
export DSO_SCHEME='dlfcn:linux-shared:-fPIC::.so.\$(SHLIB_MAJOR).\$(SHLIB_MINOR)::'
cat <<EOF_ED | ed -s Configure
/^);
-
i
#
# local configuration added from specfile
# ... MOST of those are now correct in openssl's Configure already,
# so only add them for new ports!
#
#config-string,  $cc:$cflags:$unistd:$thread_cflag:$sys_id:$lflags:$bn_ops:$cpuid_obj:$bn_obj:$des_obj:$aes_obj:$bf_obj:$md5_obj:$sha1_obj:$cast_obj:$rc4_obj:$rmd160_obj:$rc5_obj:$wp_obj:$cmll_obj:$dso_scheme:$shared_target:$shared_cflag:$shared_ldflag:$shared_extension:$ranlib:$arflags:$multilib
#"linux-elf",    "gcc:-DL_ENDIAN			::-D_REENTRANT::-ldl:BN_LLONG \${x86_gcc_des} \${x86_gcc_opts}:\${x86_elf_asm}:$DSO_SCHEME:",
#"linux-ia64",   "gcc:-DL_ENDIAN	-DMD32_REG_T=int::-D_REENTRANT::-ldl:SIXTY_FOUR_BIT_LONG RC4_CHUNK RC4_CHAR:\${ia64_asm}:		$DSO_SCHEME:",
#"linux-ppc",    "gcc:-DB_ENDIAN			::-D_REENTRANT::-ldl:BN_LLONG RC4_CHAR RC4_CHUNK DES_RISC1 DES_UNROLL:\${no_asm}:		$DSO_SCHEME:",
#"linux-ppc64",  "gcc:-DB_ENDIAN -DMD32_REG_T=int::-D_REENTRANT::-ldl:RC4_CHAR RC4_CHUNK DES_RISC1 DES_UNROLL SIXTY_FOUR_BIT_LONG:\${no_asm}:	$DSO_SCHEME:64",
"linux-elf-arm","gcc:-DL_ENDIAN			::-D_REENTRANT::-ldl:BN_LLONG:\${no_asm}:							$DSO_SCHEME:",
"linux-mips",   "gcc:-DB_ENDIAN			::-D_REENTRANT::-ldl:BN_LLONG RC4_CHAR RC4_CHUNK DES_RISC1 DES_UNROLL:\${no_asm}:		$DSO_SCHEME:",
"linux-sparcv7","gcc:-DB_ENDIAN			::-D_REENTRANT::-ldl:BN_LLONG RC4_CHAR RC4_CHUNK DES_UNROLL BF_PTR:\${no_asm}:			$DSO_SCHEME:",
#"linux-sparcv8","gcc:-DB_ENDIAN -DBN_DIV2W -mv8	::-D_REENTRANT::-ldl:BN_LLONG RC4_CHAR RC4_CHUNK DES_UNROLL BF_PTR::asm/sparcv8.o:::::::::::::	$DSO_SCHEME:",
#"linux-x86_64", "gcc:-DL_ENDIAN -DNO_ASM -DMD32_REG_T=int::-D_REENTRANT::-ldl:SIXTY_FOUR_BIT_LONG:\${no_asm}:						$DSO_SCHEME:64",
#"linux-s390",   "gcc:-DB_ENDIAN			::(unknown):   :-ldl:BN_LLONG:\${no_asm}:							$DSO_SCHEME:",
#"linux-s390x",  "gcc:-DB_ENDIAN -DNO_ASM -DMD32_REG_T=int::-D_REENTRANT::-ldl:SIXTY_FOUR_BIT_LONG:\${no_asm}:					$DSO_SCHEME:64",
"linux-parisc",	"gcc:-DB_ENDIAN 		::-D_REENTRANT::-ldl:BN_LLONG RC4_CHAR DES_PTR DES_UNROLL DES_RISC1:\${no_asm}:			$DSO_SCHEME:",
.
wq
EOF_ED
# fix ENGINESDIR path
sed -i 's,/lib/engines,/%_lib/engines,' Configure
# Record mtime of changes file instead of build time
CHANGES=`stat --format="%y" %SOURCE1`
sed -i -e "s|#define DATE \(.*\).LC_ALL.*date.|#define DATE \1$CHANGES|" crypto/Makefile

%build
RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed -s "s/--param=ssp-buffer-size=32//g")
export RPM_OPT_FLAGS
export cross=armv6l-tizen-linux-gnueabi-
export CC="${cross}gcc"
export AR="${cross}ar"
export RANLIB="${cross}ranlib"

#./config --test-sanity
#
config_flags="threads shared no-rc5 no-idea \
enable-camellia enable-md2 \
zlib \
--prefix=%{_prefix} \
--libdir=%{_lib} \
--openssldir=%{ssletcdir} \
$RPM_OPT_FLAGS -std=gnu99 \
-Wa,--noexecstack \
-fomit-frame-pointer \
-DTERMIO \
-DPURIFY \
-DSSL_FORBID_ENULL \
-D_GNU_SOURCE \
$(getconf LFS_CFLAGS) \
-Wall \
-fstack-protector "
patch -p1 < 1.0.1g-docfixes-diff.patch
#
#%{!?do_profiling:%define do_profiling 0}
#%if %do_profiling
#	# generate feedback
#	./config $config_flags
#	make depend CC="gcc %cflags_profile_generate"
#	make CC="gcc %cflags_profile_generate"
#	LD_LIBRARY_PATH=`pwd` make rehash CC="gcc %cflags_profile_generate"
#	LD_LIBRARY_PATH=`pwd` make test CC="gcc %cflags_profile_generate"
#	LD_LIBRARY_PATH=`pwd` apps/openssl speed
#	make clean
#	# compile with feedback
#	# but not if it makes a cipher slower:
#	#find crypto/aes -name '*.da' | xargs -r rm
#	./config $config_flags %cflags_profile_feedback
#	make depend
#	make
#	LD_LIBRARY_PATH=`pwd` make rehash
#	LD_LIBRARY_PATH=`pwd` make test
#%else
# OpenSSL relies on uname -m (not good). Thus that little sparc line.
#	./config \
#		$config_flags
./Configure linux-generic32  shared --prefix=%{_prefix} --libdir=%{_lib} --openssldir=%{ssletcdir} 
	#make depend
    make
    LD_LIBRARY_PATH=`pwd` make rehash
	#LD_LIBRARY_PATH=`pwd` make test
#%endif
# show settings
make TABLE
echo $RPM_OPT_FLAGS
eval $(egrep PLATFORM='[[:alnum:]]' Makefile)
grep -B1 -A22 "^\*\*\* $PLATFORM$" TABLE

%install
rm -rf $RPM_BUILD_ROOT
make MANDIR=%{_mandir} INSTALL_PREFIX=$RPM_BUILD_ROOT install
install -d -m755 $RPM_BUILD_ROOT%{ssletcdir}/certs
ln -sf ./%{name} $RPM_BUILD_ROOT/%{_includedir}/ssl
mkdir $RPM_BUILD_ROOT/%{_datadir}/ssl
mv $RPM_BUILD_ROOT/%{ssletcdir}/misc $RPM_BUILD_ROOT/%{_datadir}/ssl/
# ln -s %{ssletcdir}/certs 	$RPM_BUILD_ROOT/%{_datadir}/ssl/certs
# ln -s %{ssletcdir}/private 	$RPM_BUILD_ROOT/%{_datadir}/ssl/private
# ln -s %{ssletcdir}/openssl.cnf 	$RPM_BUILD_ROOT/%{_datadir}/ssl/openssl.cnf
#

# avoid file conflicts with man pages from other packages
#
pushd $RPM_BUILD_ROOT/%{_mandir}
# some man pages now contain spaces. This makes several scripts go havoc, among them /usr/sbin/Check.
# replace spaces by underscores
#for i in man?/*\ *; do mv -v "$i" "${i// /_}"; done
which readlink &>/dev/null || function readlink { ( set +x; target=$(file $1 2>/dev/null); target=${target//* }; test -f $target && echo $target; ) }
for i in man?/*; do
	if test -L $i ; then
	    LDEST=`readlink $i`
	    rm -f $i ${i}ssl
	    ln -sf ${LDEST}ssl ${i}ssl
	else
	    mv $i ${i}ssl
        fi
	case `basename ${i%.*}` in
	    asn1parse|ca|config|crl|crl2pkcs7|crypto|dgst|dhparam|dsa|dsaparam|enc|gendsa|genrsa|nseq|openssl|passwd|pkcs12|pkcs7|pkcs8|rand|req|rsa|rsautl|s_client|s_server|smime|spkac|ssl|verify|version|x509)
		# these are the pages mentioned in openssl(1). They go into the main package.
		echo %doc %{_mandir}/${i}ssl.gz >> $OLDPWD/filelist.doc;;
	    *)
		# the rest goes into the openssl-doc package.
		echo %doc %{_mandir}/${i}ssl.gz >> $OLDPWD/filelist.doc;;
	esac
done
popd
#
# check wether some shared library has been installed
#
ls -l $RPM_BUILD_ROOT%{_libdir}
test -f $RPM_BUILD_ROOT%{_libdir}/libssl.so.%{num_version}
test -f $RPM_BUILD_ROOT%{_libdir}/libcrypto.so.%{num_version}
test -L $RPM_BUILD_ROOT%{_libdir}/libssl.so
test -L $RPM_BUILD_ROOT%{_libdir}/libcrypto.so
#
# see what we've got
#
#cat > showciphers.c <<EOF
##include <openssl/err.h>
##include <openssl/ssl.h>
#int main(){
#unsigned int i;
#SSL_CTX *ctx;
#SSL *ssl;
#SSL_METHOD *meth;
#  meth = SSLv23_client_method();
#  SSLeay_add_ssl_algorithms();
#  ctx = SSL_CTX_new(meth);
#  if (ctx == NULL) return 0;
#  ssl = SSL_new(ctx);
#  if (!ssl) return 0;
#  for (i=0; ; i++) {
#    int j, k;
#    SSL_CIPHER *sc;
#    sc = (meth->get_cipher)(i);
#    if (!sc) break;
#    k = SSL_CIPHER_get_bits(sc, &j);
#    printf("%s\n", sc->name);
#  }
#  return 0;
#};
#EOF
#gcc $RPM_OPT_FLAGS -I${RPM_BUILD_ROOT}%{_includedir} -c showciphers.c
#gcc -o showciphers showciphers.o -L${RPM_BUILD_ROOT}%{_libdir} -lssl -lcrypto
#LD_LIBRARY_PATH=${RPM_BUILD_ROOT}%{_libdir} ./showciphers > AVAILABLE_CIPHERS || true
#cat AVAILABLE_CIPHERS
# Do not install demo scripts executable under /usr/share/doc
find demos -type f -perm /111 -exec chmod 644 {} \;

#process openssllib
mkdir $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libssl.so.%{num_version} $RPM_BUILD_ROOT/%{_lib}/
mv $RPM_BUILD_ROOT%{_libdir}/libcrypto.so.%{num_version} $RPM_BUILD_ROOT/%{_lib}/
mv $RPM_BUILD_ROOT%{_libdir}/engines $RPM_BUILD_ROOT/%{_lib}/
cd $RPM_BUILD_ROOT%{_libdir}/
ln -sf /%{_lib}/libssl.so.%{num_version} ./libssl.so
ln -sf /%{_lib}/libcrypto.so.%{num_version} ./libcrypto.so

cd $RPM_BUILD_DIR


%post -n libopenssl -p /sbin/ldconfig

%postun -n libopenssl -p /sbin/ldconfig

%files -n libopenssl
#%manifest %{name}.manifest
%defattr(-, root, root)
%license LICENSE
/%{_lib}/libssl.so.%{num_version}
/%{_lib}/libcrypto.so.%{num_version}
/%{_lib}/engines

%files -n libopenssl-devel
#%manifest %{name}.manifest
%defattr(-, root, root)
%{_includedir}/%{name}/
%{_includedir}/ssl
%exclude %{_libdir}/libcrypto.a
%exclude %{_libdir}/libssl.a
%{_libdir}/libssl.so
%{_libdir}/libcrypto.so
%_libdir/pkgconfig/libcrypto.pc
%_libdir/pkgconfig/libssl.pc
%_libdir/pkgconfig/openssl.pc

%files doc -f filelist.doc
#%manifest %{name}.manifest
%defattr(-, root, root)
%doc doc/* demos
#%doc showciphers.c

%files
#%manifest %{name}.manifest
%defattr(-, root, root)
%license LICENSE
%dir %{ssletcdir}
%dir %{ssletcdir}/certs
%config (noreplace) %{ssletcdir}/openssl.cnf
%attr(700,root,root) %{ssletcdir}/private
%dir %{_datadir}/ssl
%{_bindir}/%{name}

%files misc
#%manifest %{name}.manifest
%{_datadir}/ssl/misc
%{_bindir}/c_rehash


%changelog
