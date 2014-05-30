Name:           perl-gettext
Version:        1.05
Release:        151
License:        Artistic-1.0 ; GPL-2.0+
%define cpan_name gettext
Summary:        Message handling functions
Url:            http://search.cpan.org/dist/gettext/
Group:          Development/Libraries/Perl
Source:         http://www.cpan.org/authors/id/P/PV/PVANDRY/gettext-%{version}.tar.gz
Source1001: 	perl-gettext.manifest
BuildRequires:  perl

%description
The gettext module permits access from perl to the gettext() family of
functions for retrieving message strings from databases constructed to
internationalize software.

gettext(), dgettext(), and dcgettext() attempt to retrieve a string
matching their 'msgid' parameter within the context of the current locale.
dcgettext() takes the message's category and the text domain as parameters
while dcgettext() defaults to the LC_MESSAGES category and gettext()
defaults to LC_MESSAGES and uses the current text domain. If the string is
not found in the database, then 'msgid' is returned.

textdomain() sets the current text domain and returns the previously active
domain.

_bindtextdomain(domain, dirname)_ instructs the retrieval functions to look
for the databases belonging to domain 'domain' in the directory 'dirname'

%prep
%setup -q -n %{cpan_name}-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%check
make test

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
#%manifest %{name}.manifest
%defattr(644,root,root,755)

%changelog
