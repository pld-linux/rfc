Summary:	RFC documents
Summary(pl):	Dokumenty RFC
Name:		rfc
Version:	3275
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
Source8:	ftp://ftp.isi.edu/in-notes/%{name}%{version}.txt
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

%package	text-basic
Summary:	Commonly referenced RFC documents
Summary(pl):	Najczê¶ciej wymieniane dokumenty RFC
Group:		Documentation
Requires:	%{name}-index = %{version}
Conflicts:	%{name}-text

%description text-basic
This is pure text version of basic RFC (Request For Comments) documents,
referenced by some other package documentation.

%description text-basic -l pl
Wersja tekstowa dokumentów podstawowych RFC (Request For Comments), do
których odnosi siê dokumentacja innych pakietów.


%package	text
Summary:	RFC documents - pure text version
Summary(pl):	Wersja czysto tekstowa dokumentów RFC
Group:		Documentation
Requires:	%{name}-index = %{version}
Conflicts:	%{name}-text-basic
Provides:	%{name}-text-basic

%description text
This is pure text version of RFC (Request For Comments) documents. The
set is incomplete. Some documents are available in PostScript and PDF
formats only.

%description text -l pl
Wersja tekstowa dokumentów RFC (Request For Comments). Zbiór jest
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
mv -f rfc1291.ps rfc1291.orig.ps # FIX! check again

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
	pstotext - < rfc$n.ps >> rfc$n.txt || :
done

# Generate .ps and .pdf versions when they are not provided
for i in rfc[1-9]*.txt ; do
	BASE=`echo $i | sed "s/.txt$//"`
	PSFILE=$BASE.ps
	if [ ! -e $BASE.ps ] ; then
		# avoid stopping on errors ; .ps file may be correct
		# even after processing problems
		enscript --margin=54 -B  -fCourier11 -p $BASE.ps $i 2>/dev/null || :
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
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.]*txt* \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/${i}00
done
install rfc[0-9].txt* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/0000

# install rfc*.pdf       $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf
for i in {0,1,2}{0,1,2,3,4,5,6,7,8,9} 30 31 32 ; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.-]*pdf \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/${i}00
done
install rfc[0-9].pdf $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/0000

# install rfc*.ps        $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript
for i in {0,1,2}{0,1,2,3,4,5,6,7,8,9} 30 31 32 ; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.-]*ps* \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript/${i}00
done
install rfc[0-9].ps* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript/0000

# install rfc*.html      $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/html
BASIC="rfc1032.txt rfc1033.txt rfc1034.txt rfc1035.txt rfc1101.txt"\
"      rfc1122.txt rfc1123.txt rfc1183.txt rfc1274.txt rfc1279.txt"\
"      rfc1308.txt rfc1309.txt rfc1321.txt rfc1348.txt rfc1413.txt"\
"      rfc1510.txt rfc1535.txt rfc1536.txt rfc1537.txt rfc1591.txt"\
"      rfc1611.txt rfc1612.txt rfc1617.txt rfc1706.txt rfc1712.txt"\
"      rfc1731.txt rfc1732.txt rfc1733.txt rfc1750.txt rfc1823.txt"\
"      rfc1876.txt rfc1982.txt rfc1995.txt rfc1996.txt rfc2052.txt"\
"      rfc2060.txt rfc2061.txt rfc2062.txt rfc2079.txt rfc2086.txt"\
"      rfc2087.txt rfc2088.txt rfc2095.txt rfc2104.txt rfc2119.txt"\
"      rfc2133.txt rfc2136.txt rfc2137.txt rfc2163.txt rfc2168.txt"\
"      rfc2177.txt rfc2180.txt rfc2181.txt rfc2192.txt rfc2193.txt"\
"      rfc2195.txt rfc2218.txt rfc2221.txt rfc2222.txt rfc2228.txt"\
"      rfc2230.txt rfc2234.txt rfc2245.txt rfc2246.txt rfc2247.txt"\
"      rfc2251.txt rfc2252.txt rfc2253.txt rfc2254.txt rfc2255.txt"\
"      rfc2256.txt rfc2279.txt rfc2307.txt rfc2308.txt rfc2317.txt"\
"      rfc2342.txt rfc2359.txt rfc2373.txt rfc2374.txt rfc2375.txt"\
"      rfc2377.txt rfc2418.txt rfc2487.txt rfc2535.txt rfc2536.txt"\
"      rfc2537.txt rfc2538.txt rfc2539.txt rfc2540.txt rfc2541.txt"\
"      rfc2553.txt rfc2595.txt rfc2596.txt rfc2671.txt rfc2672.txt"\
"      rfc2673.txt rfc2683.txt rfc2696.txt rfc2713.txt rfc2714.txt"\
"      rfc2782.txt rfc2798.txt rfc2825.txt rfc2826.txt rfc2828.txt"\
"      rfc2829.txt rfc2830.txt rfc2831.txt rfc2845.txt rfc2849.txt"\
"      rfc2874.txt rfc2891.txt rfc2915.txt rfc2929.txt rfc2930.txt"\
"      rfc2931.txt rfc3007.txt rfc3008.txt rfc3062.txt rfc3088.txt"\
"      rfc3090.txt rfc3110.txt rfc952.txt  rfc959.txt"

for i in $BASIC; do
	install $i* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text
done

%clean
rm -rf $RPM_BUILD_ROOT

%files text-basic
%defattr(644,root,root,755)
%dir %{_defaultdocdir}/RFC/text
%{_defaultdocdir}/RFC/text/rfc*.txt*

%files text
%defattr(644,root,root,755)
%dir %{_defaultdocdir}/RFC/text
%{_defaultdocdir}/RFC/text/[0-9]*

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
