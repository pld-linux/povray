Summary:	Persistence of Vision Ray Tracer
Summary(pl):	Persistence of Vision Ray Tracer
Name:		povray
Version:	3.1g
Release:	4
Copyright:	distrituable
Group:		Applications/Graphics
Group(de):	Applikationen/Grafik
Group(pl):	Aplikacje/Grafika
Source0:	ftp://ftp.povray.org/pub/povray/Official/Unix/povuni_s.tgz
Source1:	ftp://ftp.povray.org/pub/povray/Official/Unix/povuni_d.tgz
Source2:	pvmpov-3.1e2.tgz
Patch0:		%{name}-makefile_and_config.patch
Patch1:		patchek
URL:		http://www.povray.org/
BuildRequires:	zlib-devel
BuildRequires:	libpng >= 1.0.8
%{!?_with_pvm:BuildRequires:XFree86-devel}
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
Summary(pl):	povray pod X Window
Group:		Applications/Graphics
Group(de):	Applikationen/Grafik
Group(pl):	Aplikacje/Grafika
Requires:	%{name} = %{version}

%description X11
The Persistence of Vision(tm) Ray-Tracer X Window executable.


%package pvm
Summary:	PVM/newunix povray executable
Group:		Applications/Graphics
Group(de):	Applikationen/Grafik
Group(pl):	Aplikacje/Grafika
Requires:	%{name} = %{version}

%description pvm
The Persistence of Vision(tm) Ray-Tracer PVM/newunix executable.

%prep
%setup -q -n povray31 -b 1 
%patch0 -p1
%patch1 -p1

%build
cd source/unix
%{__make} newunix newxwin OPT_FLAGS="%{rpmcflags}"
tar zxf %{SOURCE2}
patch -p1 < pvmpov3_1e_2/pvmpov.patch
install pvmpov3_1e_2/povray31/source/pvm/pvm.* source/
install source/unix/povray source/unix/povray.ori
%{__make} newunix OPT_FLAGS="%{rpmcflags}"
install source/unix/povray source/unix/pvmpov
install source/unix/povray.ori source/unix/povray

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/skel,%{_mandir}/man1,%{_datadir}/povray31}

install source/unix/{povray,x-povray,pvmpov} $RPM_BUILD_ROOT%{_bindir}
install source/unix/povrayrc $RPM_BUILD_ROOT/etc/skel/.povrayrc

install povray.1 $RPM_BUILD_ROOT%{_mandir}/man1

cp -r allscene include scenes $RPM_BUILD_ROOT%{_datadir}/povray31
install *.ini *.pov $RPM_BUILD_ROOT%{_datadir}/povray31

gzip -9nf gamma.gif.txt povlegal.doc povuser.txt

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

%files pvm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pvmpov
