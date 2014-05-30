Name:           tzdata
Summary:        Timezone Descriptions
License:        BSD-3-Clause and SUSE-Public-Domain
Group:          Base/Configuration
Url:            http://www.gnu.org/software/libc/libc.html
Requires(pre):         filesystem, coreutils
# COMMON-BEGIN
Version:        2012e
Release:        0
Source:         ftp://ftp.iana.org/tz/releases/tzdata-%{version}.tar.gz
Source1001: 	tzdata.manifest
Provides:	timezone
# COMMON-END
%global AREA    Etc
%global ZONE    UTC

%description
These are configuration files that describe available time zones. You
can select an appropriate time zone for your system with YaST.



%prep
%setup -c 
cp %{SOURCE1001} .
# COMMON-PREP-BEGIN
# COMMON-PREP-END

%build
unset ${!LC_*}
LANG=POSIX
LC_ALL=POSIX
AREA=%{AREA}
ZONE=%{ZONE}
HOST=%{_host}
BUILD=%{_build}
export AREA LANG LC_ALL ZONE HOST BUILD RUNARM
make %{?_smp_mflags} TZDIR=%{_prefix}/share/zoneinfo CFLAGS="$RPM_OPT_FLAGS -DHAVE_GETTEXT=1 -DTZDEFAULT='\"/etc/localtime\"'" AWK=awk
make %{?_smp_mflags} TZDIR=zoneinfo AWK=awk zones
# Generate posixrules
qemu-arm -L /usr/%{_host} ./zic -y ./yearistype -d zoneinfo -p %{AREA}/%{ZONE}

%install
mkdir -p %{buildroot}%{_prefix}/share/zoneinfo
cp -a zoneinfo %{buildroot}%{_prefix}/share/zoneinfo/posix
cp -al %{buildroot}%{_prefix}/share/zoneinfo/posix/. %{buildroot}%{_prefix}/share/zoneinfo
cp -a zoneinfo-leaps %{buildroot}%{_prefix}/share/zoneinfo/right
mkdir -p %{buildroot}/etc
rm -f  %{buildroot}/etc/localtime
rm -f  %{buildroot}%{_prefix}/share/zoneinfo/posixrules
cp -fp %{buildroot}%{_prefix}/share/zoneinfo/%{AREA}/%{ZONE} %{buildroot}/etc/localtime
ln -sf /etc/localtime      %{buildroot}%{_prefix}/share/zoneinfo/posixrules
install -m 644 iso3166.tab %{buildroot}%{_prefix}/share/zoneinfo/iso3166.tab
install -m 644 zone.tab    %{buildroot}%{_prefix}/share/zoneinfo/zone.tab
install -D -m 755 tzselect %{buildroot}%{_bindir}/tzselect
install -D -m 755 zdump    %{buildroot}%{_sbindir}/zdump
install -D -m 755 zic      %{buildroot}%{_sbindir}/zic

%clean
rm -rf %{buildroot}

%post
if [ -f /etc/sysconfig/clock ];
then
    . /etc/sysconfig/clock
    if [ -n "$ZONE" -a -f /etc/localtime -a -f /usr/share/zoneinfo/$ZONE ]; then
	new=$(mktemp /etc/localtime.XXXXXXXX) || exit 1
	cp -l /usr/share/zoneinfo/$ZONE $new 2>/dev/null || cp -fp /usr/share/zoneinfo/$ZONE $new
	mv -f $new /etc/localtime
    else
	[ ! -f /etc/localtime ] || echo "WARNING: Not updating /etc/localtime with new zone file" >&2
    fi
fi

%files
#%manifest %{name}.manifest
%defattr(-,root,root)
%verify(not link md5 size mtime) %config(missingok,noreplace) /etc/localtime
%verify(not link md5 size mtime) %config(missingok,noreplace) %{_prefix}/share/zoneinfo/posixrules
%{_prefix}/share/zoneinfo
%{_bindir}/tzselect
%{_sbindir}/zdump
%{_sbindir}/zic

%changelog
