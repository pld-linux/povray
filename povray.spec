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
# pvm.patch is instead of that source, and its based on it
#Source2:	pvmpov-3.1e2.tgz
Patch0:		%{name}-makefile_and_config.patch
Patch1:		%{name}-pvm.patch
URL:		http://www.povray.org/
BuildRequires:	zlib-devel
BuildRequires:	libpng-devel >= 1.0.8
%{!?_without_x:BuildRequires:XFree86-devel}
%{!?_without_pvm:BuildRequires:pvm-devel}
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

%{!?_without_x:%package X11}
%{!?_without_x:Summary:	X Window povray executable}
%{!?_without_x:Summary(pl):	povray pod X Window}
%{!?_without_x:Group:		Applications/Graphics}
%{!?_without_x:Group(de):	Applikationen/Grafik}
%{!?_without_x:Group(pl):	Aplikacje/Grafika}
%{!?_without_x:Requires:	%{name} = %{version}}

%{!?_without_x:%description X11}
%{!?_without_x:The Persistence of Vision(tm) Ray-Tracer X Window executable.}


%{!?_without_pvm:%package pvm}
%{!?_without_pvm:Summary:	PVM/unix povray executable}
%{!?_without_pvm:Group:		Applications/Graphics}
%{!?_without_pvm:Group(de):	Applikationen/Grafik}
%{!?_without_pvm:Group(pl):	Aplikacje/Grafika}
%{!?_without_pvm:Requires:	%{name} = %{version}}

%{!?_without_pvm:%description pvm}
%{!?_without_pvm:The Persistence of Vision(tm) Ray-Tracer PVM/unix executable.}


%{!?_without_pvm:%{!?_without_x:%package pvm-X11}}
%{!?_without_pvm:%{!?_without_x:Summary:	PVM/xwin povray executable}}
%{!?_without_pvm:%{!?_without_x:Group:		Applications/Graphics}}
%{!?_without_pvm:%{!?_without_x:Group(de):	Applikationen/Grafik}}
%{!?_without_pvm:%{!?_without_x:Group(pl):	Aplikacje/Grafika}}
%{!?_without_pvm:%{!?_without_x:Requires:	%{name} = %{version}}}

%{!?_without_pvm:%{!?_without_x:%description pvm-X11}}
%{!?_without_pvm:%{!?_without_x:The Persistence of Vision(tm) Ray-Tracer PVM/xwin executable.}}



%prep
%setup -q -n povray31 -b 1 
%patch0 -p1
%patch1 -p0

%build
cd source/unix
%{__make} newunix %{!?_without_x:newxwin} %{!?_without_pvm:newunix_pvm %{!?_without_x:newxwin_pvm}} OPT_FLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},/etc/skel,%{_mandir}/man1,%{_datadir}/povray31}

install source/unix/povray $RPM_BUILD_ROOT%{_bindir}
%{!?_without_x:install source/unix/x-povray $RPM_BUILD_ROOT%{_bindir}}
%{!?_without_pvm:install source/unix/pvmpov $RPM_BUILD_ROOT%{_bindir}}
%{!?_without_pvm:%{!?_without_x:install source/unix/x-pvmpov $RPM_BUILD_ROOT%{_bindir}}}
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

%{!?_without_x:%files X11}
%{!?_without_x:%defattr(644,root,root,755)}
%{!?_without_x:%attr(755,root,root) %{_bindir}/x-povray}

%{!?_without_pvm:%files pvm}
%{!?_without_pvm:%defattr(644,root,root,755)}
%{!?_without_pvm:%attr(755,root,root) %{_bindir}/pvmpov}

%{!?_without_pvm:%{!?_without_x:%files pvm-X11}}
%{!?_without_pvm:%{!?_without_x:%defattr(644,root,root,755)}}
%{!?_without_pvm:%{!?_without_x:%attr(755,root,root) %{_bindir}/x-pvmpov}}
