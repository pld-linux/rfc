Summary:	RFC documents
Summary(pl):	Dokumenty RFC
Name:		rfc
Version:	3240
Release:	1
License:	distributable
Group:		Documentation
Source0:	ftp://ftp.isi.edu/in-notes/tar/RFCs0001-0500.tar.gz
Source1:	ftp://ftp.isi.edu/in-notes/tar/RFCs0501-1000.tar.gz
Source2:	ftp://ftp.isi.edu/in-notes/tar/RFCs1001-1500.tar.gz
Source3:	ftp://ftp.isi.edu/in-notes/tar/RFCs1501-2000.tar.gz
Source4:	ftp://ftp.isi.edu/in-notes/tar/RFCs2001-2500.tar.gz
Source5:	ftp://ftp.isi.edu/in-notes/tar/RFCs2501-3000.tar.gz
Source6:	ftp://ftp.isi.edu/in-notes/tar/RFCs3001-latest.tar.gz
Source7:	ftp://ftp.isi.edu/in-notes/%{name}-index.txt
URL:		http://www.rfc.net/
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RFC (Request For Comments) documents are actual and suggested Internet
standards.

%description -l pl
Dokumenty RFC (Request For Comments) zawieraj± opis obowi±zuj±cych i
proponowanych standardów internetowych.

%prep
%setup -q -c -a1 -a2 -a3 -a4 -a5 -a6

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/{{0,1,2}{0,1,2,3,4,5,6,7,8,9},30,31,32,33}00
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf
# install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/{postscript,html}

find . -name 'rfc[1-9]*.txt' -print | xargs gzip -9

install %{SOURCE7} $RPM_BUILD_ROOT%{_defaultdocdir}/RFC

# install rfc[1-9]*.txt* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text
for i in {0,1,2}{0,1,2,3,4,5,6,7,8,9} 30 31 32 ; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9].txt* \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/${i}00
done
install rfc[0-9].txt* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/0000

install rfc*.pdf       $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf
# install rfc*.html      $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/html
# install rfc*.ps        $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC
