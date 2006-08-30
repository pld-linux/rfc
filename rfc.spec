#
# Conditional build:
%bcond_with	ps		# build package with RFCs in PostScript format too
%bcond_without	pdf	# don't build package with RFCs in PDF format

Summary:	RFC documents
Summary(es):	Los documentos RFC
Summary(pl):	Dokumenty RFC
Name:		rfc
Version:	4498
Release:	2
License:	distributable
Group:		Documentation
Source0:	ftp://ftp.isi.edu/in-notes/tar/RFCs0001-0500.tar.gz
# Source0-md5:	99cec264ad50efa8b94d312f09b4f108
Source1:	ftp://ftp.isi.edu/in-notes/tar/RFCs0501-1000.tar.gz
# Source1-md5:	96d468b8ecb513e642ca0e9b4032a150
Source2:	ftp://ftp.isi.edu/in-notes/tar/RFCs1001-1500.tar.gz
# Source2-md5:	b3dc2d4fac7733014b537f914f09b78f
Source3:	ftp://ftp.isi.edu/in-notes/tar/RFCs1501-2000.tar.gz
# Source3-md5:	18bc03445190a9a9e331eb47b07f942e
Source4:	ftp://ftp.isi.edu/in-notes/tar/RFCs2001-2500.tar.gz
# Source4-md5:	ec09b758d25e39b1d4a415780ff0c329
Source5:	ftp://ftp.isi.edu/in-notes/tar/RFCs2501-3000.tar.gz
# Source5-md5:	0799d01a6776e69b5d3ec3b348013c79
Source6:	ftp://ftp.isi.edu/in-notes/tar/RFCs3001-3500.tar.gz
# Source6-md5:	55b806dc69f0c901552434556402b8a5
Source7:	ftp://ftp.isi.edu/in-notes/tar/RFCs3501-4000.tar.gz
# Source7-md5:	866c41972f9656635c81181b0b9e4dca
Source8:	ftp://ftp.isi.edu/in-notes/tar/RFCs4001-4500.tar.gz
# Source8-md5:	f747637be7b625724f4f1fa355dc9ec2
Source9:	RFCs-missing-from-tar.tar.bz2
# Source9-md5:	1276481102f218c981e0324180bafd9f
Patch0:		%{name}.patch
URL:		http://www.rfc.net/
%if %{with ps} || %{with pdf}
BuildRequires:	enscript
BuildRequires:	ghostscript
%endif
BuildRequires:	xpdf-tools
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RFC (Request For Comments) documents are actual and suggested Internet
standards.

%description -l es
Los documentos RFC (Request For Comments: petición de comentarios) son
los estándares actuales y sugeridos del Internet.

%description -l pl
Dokumenty RFC (Request For Comments) zawieraj± opis obowi±zuj±cych i
proponowanych standardów internetowych.

%package text-basic
Summary:	Commonly referenced RFC documents
Summary(es):	Documentos RFC repetidamente referidos
Summary(pl):	Najczê¶ciej wymieniane dokumenty RFC
Group:		Documentation
Requires:	%{name}-index >= %{version}
Obsoletes:	%{name}-text

%description text-basic
This is pure text version of basic RFC (Request For Comments)
documents, referenced by some other package documentation.

%description text-basic -l es
Ésta es la versión de texto puro de los documentos RFC (Request For
Comments: petición de comentarios), a los que se refiere la
documentación de algunos otros paquetes.

%description text-basic -l pl
Wersja tekstowa dokumentów podstawowych RFC (Request For Comments), do
których odnosi siê dokumentacja innych pakietów.

%package text
Summary:	RFC documents - pure text version
Summary(es):	Documentos RFC - versión de texto puro
Summary(pl):	Wersja czysto tekstowa dokumentów RFC
Group:		Documentation
Requires:	%{name}-index >= %{version}
Provides:	%{name}-text-basic
Obsoletes:	%{name}-text-basic

%description text
This is pure text version of RFC (Request For Comments) documents. The
set is incomplete. Some documents are available in PostScript and PDF
formats only.

%description text -l es
Ésta es la versión de texto puro de los documentos RFC (Request For
Comments: petición de comentarios). Este conjunto es incompleto, ya
que algunos documentos son disponibles sólo en los formatos PostScript
y PDF.

%description text -l pl
Wersja tekstowa dokumentów RFC (Request For Comments). Zbiór jest
niepe³ny, gdy¿ niektóre dokumenty s± dostêpne wy³±cznie w postaci
postscriptowej i PDF.

%package ps
Summary:	RFC documents - PostScript version
Summary(es):	Documentos RFC - versión PostScript
Summary(pl):	Wersja postscriptowa dokumentów RFC
Group:		Documentation
Requires:	%{name}-index >= %{version}

%description ps
PostScript version of RFC (Request For Comments) documents.

%description ps -l es
La versión PostScript de los documentos RFC (Request For Comments:
petición de comentarios).

%description ps -l pl
Wersja postscriptowa dokumentów RFC (Request For Comments).

%package pdf
Summary:	RFC documents - PDF version
Summary(es):	Documentos RFC - versión PDF
Summary(pl):	Wersja postscriptowa dokumentów RFC
Group:		Documentation
Requires:	%{name}-index >= %{version}

%description pdf
RFC (Request For Comments) documents in Adobe PDF format.

%description pdf -l es
Documentos RFC (Request For Comments: petición de comentarios) en
formato Adobe PDF.

%description pdf -l pl
Dokumenty RFC (Request For Comments) w formacie Adobe PDF.

%prep
%setup -q -c -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9
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

%if %{with ps}
for n in 1144 1305 ; do
	gs -q -dNOPAUSE -dBATCH -dSAFER -sDEVICE=pswrite \
		-sOutputFile=rfc$n.ps -c save pop -f rfc$n.pdf
done
%endif

# these were provided only in .ps/.pdf
for n in 1119 1124 1128 1129 1131 ; do
	echo -e '\nThe text below was generated from PDF by pdftotext.' >> rfc$n.txt
	echo -e '----------------------------------------------------------------------\n' >> rfc$n.txt
	pdftotext rfc$n.pdf - >> rfc$n.txt
done

# Generate .ps and .pdf versions when they are not provided
%if %{with ps} || %{with pdf}
for i in rfc[1-9]*.txt ; do
	BASE=`echo $i | sed "s/.txt$//"`
	PSFILE=$BASE.ps
	if [ ! -e $BASE.ps ] ; then
		# avoid stopping on errors ; .ps file may be correct
		# even after processing problems
		enscript --margin=54 -B -fCourier11 -p $BASE.ps $i 2>/dev/null ||:
	fi
%endif
%if %{with pdf}
	if [ ! -e $BASE.pdf ] ; then
		ps2pdf $BASE.ps $BASE.pdf 2>/dev/null
	fi
%endif
%if %{with ps} || %{with pdf}
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/{{0,1,2,3}{0,1,2,3,4,5,6,7,8,9},4{0,1,2,3,4}}00
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/{{0,1,2,3}{0,1,2,3,4,5,6,7,8,9},4{0,1,2,3,4}}00
install -d $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript/{{0,1,2,3}{0,1,2,3,4,5,6,7,8,9},4{0,1,2,3,4}}00

find . -name 'rfc[1-9]*.txt' -print | xargs gzip -9
%if %{with ps}
find . -name 'rfc[1-9]*.ps' -print | xargs gzip -9
%endif

# install rfc[1-9]*.txt* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text
for i in {0,1,2,3}{0,1,2,3,4,5,6,7,8,9} 4{0,1,2,3,4}; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.]*txt* \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/${i}00
done
install rfc[0-9].txt* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/text/0000

# install rfc*.pdf       $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf
%if %{with pdf}
for i in {0,1,2,3}{0,1,2,3,4,5,6,7,8,9} 4{0,1,2,3,4} ; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.-]*pdf \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/${i}00
done
install rfc[0-9].pdf $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/pdf/0000
%endif

%if %{with ps}
# install rfc*.ps        $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript
for i in {0,1,2,3}{0,1,2,3,4,5,6,7,8,9} 4{0,1,2,3,4} ; do
	install rfc`echo $i|sed s/^0\*//g`[0-9][0-9][a.-]*ps* \
		$RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript/${i}00
done
install rfc[0-9].ps* $RPM_BUILD_ROOT%{_defaultdocdir}/RFC/postscript/0000
%endif

BASIC="rfc1032.txt rfc1033.txt rfc1034.txt rfc1035.txt rfc1101.txt"\
"      rfc1122.txt rfc1123.txt rfc1183.txt rfc1274.txt rfc1279.txt"\
"      rfc1308.txt rfc1309.txt rfc1321.txt rfc1348.txt rfc1413.txt"\
"      rfc1510.txt rfc1535.txt rfc1536.txt rfc1537.txt rfc1591.txt"\
"      rfc1611.txt rfc1612.txt rfc1617.txt rfc1706.txt rfc1712.txt"\
"      rfc1731.txt rfc1732.txt rfc1733.txt rfc1750.txt rfc1823.txt"\
"      rfc1876.txt rfc1939.txt rfc1982.txt rfc1995.txt rfc1996.txt"\
"      rfc2052.txt rfc2060.txt rfc2061.txt rfc2062.txt rfc2079.txt"\
"      rfc2086.txt rfc2087.txt rfc2088.txt rfc2095.txt rfc2104.txt"\
"      rfc2119.txt rfc2131.txt rfc2132.txt rfc2133.txt rfc2136.txt"\
"      rfc2137.txt rfc2163.txt rfc2168.txt rfc2177.txt rfc2180.txt"\
"      rfc2181.txt rfc2192.txt rfc2193.txt rfc2195.txt rfc2218.txt"\
"      rfc2221.txt rfc2222.txt rfc2228.txt rfc2230.txt rfc2234.txt"\
"      rfc2243.txt rfc2245.txt rfc2246.txt rfc2247.txt rfc2251.txt"\
"      rfc2252.txt rfc2253.txt rfc2254.txt rfc2255.txt rfc2256.txt"\
"      rfc2279.txt rfc2289.txt rfc2293.txt rfc2294.txt rfc2307.txt"\
"      rfc2308.txt rfc2317.txt rfc2342.txt rfc2359.txt rfc2373.txt"\
"      rfc2374.txt rfc2375.txt rfc2377.txt rfc2418.txt rfc2444.txt"\
"      rfc2485.txt rfc2487.txt rfc2489.txt rfc2535.txt rfc2536.txt"\
"      rfc2537.txt rfc2538.txt rfc2539.txt rfc2540.txt rfc2541.txt"\
"      rfc2553.txt rfc2587.txt rfc2589.txt rfc2595.txt rfc2596.txt"\
"      rfc2649.txt rfc2671.txt rfc2672.txt rfc2673.txt rfc2683.txt"\
"      rfc2696.txt rfc2713.txt rfc2714.txt rfc2782.txt rfc2798.txt"\
"      rfc2825.txt rfc2826.txt rfc2828.txt rfc2829.txt rfc2830.txt"\
"      rfc2831.txt rfc2845.txt rfc2849.txt rfc2874.txt rfc2891.txt"\
"      rfc2915.txt rfc2929.txt rfc2930.txt rfc2931.txt rfc2945.txt"\
"      rfc3007.txt rfc3008.txt rfc3045.txt rfc3062.txt rfc3088.txt"\
"      rfc3090.txt rfc3110.txt rfc3112.txt rfc3174.txt rfc3296.txt"\
"      rfc3315.txt rfc3377.txt rfc3383.txt rfc951.txt  rfc952.txt"\
"      rfc959.txt"

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

%if %{with ps}
%files ps
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/postscript
%endif

%if %{with pdf}
%files pdf
%defattr(644,root,root,755)
%{_defaultdocdir}/RFC/pdf
%endif
