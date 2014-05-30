Name:           sqlite
Version:        3.7.14
Release:        0
License:        Public-Domain
%define tarversion 3071400
Summary:        Embeddable SQL Database Engine
Url:            http://www.sqlite.org/
Group:          System/Database
Source0:        sqlite-autoconf-%tarversion.tar.gz
Source1:        baselibs.conf
Source1001: 	sqlite.manifest
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(pkg-config)
Requires:       libsqlite = %{version}
Provides:       sqlite3

%description
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database
server. SQLite is a server and the SQLite library reads and writes
directly to and from the database files on disk.

SQLite can be used via the sqlite command line tool or via any
application that supports the Qt database plug-ins.

%package -n libsqlite
Summary:        Shared libraries for the Embeddable SQL Database Engine
Group:          System/Database
Provides:       libsqlit3

%description -n libsqlite
This package contains the shared libraries for the Embeddable SQL
Database Engine.

SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database
server. SQLite is a server and the SQLite library reads and writes
directly to and from the database files on disk.

SQLite can be used via the sqlite command line tool or via any
application that supports the Qt database plug-ins.

%package devel
Summary:        Embeddable SQL Database Engine
Group:          Development/Libraries
Requires:       glibc-devel
Requires:       libsqlite = %{version}
Requires:       sqlite
Provides:       sqlite3-devel = %{version}
Obsoletes:      sqlite3-devel < %{version}

%description devel
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process.

SQLite is not a client library used to connect to a big database
server; SQLite is the server. The SQLite library reads and writes
directly to and from the database files on disk.

SQLite can be used via the sqlite command-line tool or via any
application which supports the Qt database plug-ins.

%prep
%setup -q -n sqlite-autoconf-%tarversion
cp %{SOURCE1001} .

%build
CFLAGS=`echo %{optflags} |sed -e 's/-ffast-math//g'`
chmod +x autogen.sh
%autogen
%configure --disable-static --enable-threadsafe
make

%install
%make_install

%post -n libsqlite -p /sbin/ldconfig

%postun -n libsqlite -p /sbin/ldconfig

%files
#%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/sqlite3

%files -n libsqlite
#%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libsqlite*.so.*

%files devel
#%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libsqlite*.so
%{_libdir}/pkgconfig/sqlite3.pc

%docs_package
