Summary:	RFC documents
Summary(pl):	Dokumenty RFC
Name:		rfc
Version:	3244
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
# Missing from RFCs0001-0500.tar.gz (newer)
# Temporarily this is not necessary.
# Source10:	RFCs-omited.tar.gz
Patch0:		%{name}.patch
URL:		http://www.rfc.net/
BuildRequires:	enscript
BuildRequires:	ghostscript
BuildRequires:	pstotext
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RFC (Request For Comments) documents are actual and suggested Internet
standards.

%description -l pl
Dokumenty RFC (Request For Comments) zawieraj± opis obowi±zuj±cych i
proponowanych standardów internetowych.

%package	index
Summary:	Index for RFC documents
Summary(pl):	Indeks dokumentów RFC
Group:		Documentation

%description index
Index file for RFC (Request For Comments) documents containing info
about document title, authors, status, size, etc.

%description index -l pl
Plik indeksowy dokumentów RFC (Request For Comments) zawieraj±cy
informacje takie, jak: tytu³, autorzy, status, rozmiar itp. dla
poszczególnych dokumentów.

%package	text
Summary:	RFC documents - pure text version
Summary(pl):	Wersja czysto tekstowa dokumentów RFC
Group:		Documentation
Requires:	%{name}-index = %{version}

%description text
This is pure text version of RFC (Request For Comments) documents. The
set is incomplete. Some documents are available in PostScript and PDF
formats only.

%description text -l pl
Wersja tekstowa dokumentów RFC (Request For Comments). Zbior jest
niepe³ny, gdy¿ niektóre dokumenty s± dostêpne wy³±cznie w postaci
postscriptowej i PDF.


%package	ps
Summary:	RFC documents - PostScript version
Summary(pl):	Wersja postscriptowa dokumentów RFC
Group:		Documentation
Requires:	%{name}-index = %{version}

%description ps
PostScript version of RFC (Request For Comments) documents.

%description ps -l pl
Wersja postscriptowa dokumentów RFC (Request For Comments).

%package	pdf
Summary:	RFC documents - pdf version
Summary(pl):	Wersja postscriptowa dokumentów RFC
Group:		Documentation
Requires:	%{name}-index = %{version}

%description pdf
RFC (Request For Comments) documents in Adobe PDF format.

%description pdf -l pl
Dokumenty RFC (Request For Comments) w formacie Adobe PDF.

%prep
%setup -q -c -a1 -a2 -a3 -a4 -a5 -a6
%patch0 -p0

%build
rm -f rfc2328.hastabs.txt

# These are broken/unreadable by gv
mv -f rfc1144.ps rfc1144.orig.ps
mv -f rfc1279.ps rfc1279.orig.ps
mv -f rfc1291.ps rfc1291.orig.ps

# These are unreadable because of character spacing problems
mv -f rfc1125.pdf rfc1125.orig.pdf
mv -f rfc1275.pdf rfc1275.orig.pdf

# These are pictures only
mv -f rfc525.ps rfc525-pict.ps
mv -f rfc546.ps rfc546-pict.ps
mv -f rfc525.pdf rfc525-pict.pdf
mv -f rfc546.pdf rfc546-pict.pdf

for n in 1144 1305 ; do
	gs -q -dNOPAUSE -dBATCH -dSAFER -sDEVICE=pswrite \
	   -sOutputFile=rfc$n.ps -c save pop -f rfc$n.pdf
done

# these were provided only in .ps
for n in 1119 1124 1128 1129 1131 ; do
	echo -e '\nThe text below was generated from PostScript by pstotext.' >> rfc$n.txt
	echo -e '----------------------------------------------------------------------\n' >> rfc$n.txt
	pstotext rfc$n.ps >> rfc$n.txt
done

# Generate .ps and .pdf versions when they are not provided
for i in rfc[1-9]*.txt ; do
	BASE=`echo $i | sed "s/.txt$//"`
	PSFILE=$BASE.ps
	if [ ! -e $BASE.ps ] ; then
		# avoid stopping on errors ; .ps file may be correct
		# even after processing problems
		sh -c "enscript --margin=54 -B  -fCourier11 -p $BASE.ps $i 2>/dev/null
		       exit 0"
	fi
	if [ ! -e $BASE.pdf ] ; then
		ps2pdf $BASE.ps $BASE.pdf 2>/dev/null
	fi
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/{{0,1,2}{0,1,2,3,4,5,6,7,8,9},30,31,32,33}00
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/{{0,1,2}{0,1,2,3,4,5,6,7,8,9},30,31,32,33}00
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript/{{0,1,2}{0,1,2,3,4,5,6,7,8,9},30,31,32,33}00

install %{SOURCE7} $RPM_BUILD_ROOT%{_defaultdocdir}/RFC

find . -name 'rfc[1-9]*.txt' -print | xargs gzip -9
find . -name 'rfc[1-9]*.ps'  -print | xargs gzip -9

# install rfc[1-9]*.txt* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text
for i in {0,1,2}{0,1,2,3,4,5,6,7,8,9} 30 31 32 ; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9].txt* \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/${i}00
done
install rfc[0-9].txt* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/0000

# install rfc*.pdf       $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf
for i in {0,1,2}{0,1,2,3,4,5,6,7,8,9} 30 31 32 ; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][.-]*pdf \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/${i}00
done
install rfc[0-9].pdf $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/0000

# install rfc*.ps        $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript
for i in {0,1,2}{0,1,2,3,4,5,6,7,8,9} 30 31 32 ; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][.-]*ps* \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript/${i}00
done
install rfc[0-9].ps* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript/0000

# install rfc*.html      $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/html

%clean
rm -rf $RPM_BUILD_ROOT

%files text
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/text

%files index
%defattr(644,root,root,755)
%dir %{_defaultdocdir}/RFC
%{_defaultdocdir}/RFC/rfc-index.txt

%files ps
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/postscript

%files pdf
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/pdf
