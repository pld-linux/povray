Summary:	Persistence of Vision Ray Tracer
Summary(pl):	Persistence of Vision Ray Tracer
Name:		povray
Version:	3.1g
Release: 4
Copyright:	distrituable
Group:		Applications/Graphics
Group(pl):	Aplikacje/Grafika
Source0:	ftp://ftp.povray.org/pub/povray/Official/Unix/povuni_s.tgz
Source1:	ftp://ftp.povray.org/pub/povray/Official/Unix/povuni_d.tgz
Patch0:		povray-makefile_and_config.patch
URL:		http://www.povray.org/
BuildRequires:	zlib-devel
BuildRequires:	libpng >= 1.0.8
BuildRequires:	XFree86-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Persistence of Vision(tm) Ray-Tracer creates three-dimensional,
photo-realistic images using a rendering technique called ray-tracing.
It reads in a text file containing information describing the objects
and lighting in a scene and generates an image of that scene from the
view point of a camera also described in the text file. Ray-tracing is
not a fast process by any means, but it produces very high quality
images with realistic reflections, shading, perspective and other
effects.

%description -l pl
Persistence of Vision(tm) Ray-Tracer tworzy trójwymiarowe,
fotorealistyczne obrazy za pomoc± techniki renderingu zwanej
ray-tracing. Program pobiera z pliku tekstowego informacje opisuj±ce
obiekty oraz ¶wiat³o przedstawianego ¶wiata, a nastêpnie generuje
rysunek z punktu widzenia kamery, która tak¿e jest definiowana w w/w
pliku tekstowym. Ray-tracing nie pozwala na szybkie tworzenie obrazów,
ale za to twórca otrzymuje wyskokiej jako¶ci bitmapy z realistycznymi
efektami, tj. odbicia ¶wiat³a, cienie, perspektywa i inne.

%package X11
Summary:	X Window povray executable
Group:		Applications/Graphics
Group(pl):	Aplikacje/Grafika
Requires:	%{name} = %{version}

%description X11
The Persistence of Vision(tm) Ray-Tracer X Window executable.

%prep
%setup -q -n povray31 -b 1

%patch0 -p1

%build
cd source/unix
%{__make} newunix newxwin OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/skel,%{_mandir}/man1,%{_datadir}/povray31}

install -s source/unix/{povray,x-povray} $RPM_BUILD_ROOT%{_bindir}
install source/unix/povrayrc $RPM_BUILD_ROOT/etc/skel/.povrayrc

install povray.1 $RPM_BUILD_ROOT%{_mandir}/man1

cp -r allscene include scenes $RPM_BUILD_ROOT%{_datadir}/povray31
install *.ini *.pov $RPM_BUILD_ROOT%{_datadir}/povray31

gzip -9nf gamma.gif.txt povlegal.doc povuser.txt \
	$RPM_BUILD_ROOT%{_mandir}/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc gamma.gif.txt.gz povuser.txt.gz gamma.gif povlegal.doc.gz
%attr(755,root,root) %{_bindir}/povray
%{_datadir}/povray31
/etc/skel/.povrayrc
%{_mandir}/man1/*

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/x-povray
