
#
# todo:
#      patch for s#/usr/local#/usr# in povray.ini
#      (no)svga version
#

# Conditional build:
# _without_x	- without X11 subpackage
# _without_pvm	- without PVM support
#
%define		snap 20030110
Summary:	Persistence of Vision Ray Tracer
Summary(pl):	Persistence of Vision Ray Tracer
Name:		povray
Version:	3.50c
Release:	1
License:	distributable
Group:		Applications/Graphics
#Source0:	ftp://ftp.povray.org/pub/povray/Official/Unix/povuni_s.tgz
# based on sources from CVS at http://pvmpov.sourceforge.net/
Source0:	%{name}-%{version}-%{snap}.tar.gz
Source1:	%{name}-%{version}.md5sum
Patch0:		%{name}-legal.patch
Patch1:		%{name}-types.patch
URL:		http://www.povray.org/
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.0.8
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	zlib-devel
%{!?_without_x:BuildRequires:XFree86-devel}
#%{!?_without_pvm:BuildRequires:pvm-devel >= 3.4.3-24 }
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		%{_datadir}
%define		_pvmarch	%(/usr/bin/pvmgetarch)
%define		_pvmroot	/usr/lib/pvm3/

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
Requires:	%{name} = %{version}

%description X11
The Persistence of Vision(tm) Ray-Tracer X Window executable.

%description X11 -l pl
Plik wykonywalny The Persistence of Vision(tm) Ray-Tracer dla X
Window.

%package pvm
Summary:	PVM/unix povray executable
Summary(pl):	Plik wykonywalny povray dla PVM/unix
Group:		Applications/Graphics
Requires:	%{name} = %{version}

%description pvm
The Persistence of Vision(tm) Ray-Tracer PVM/unix executable.

%description X11 -l pl
Plik wykonywalny The Persistence of Vision(tm) Ray-Tracer dla
PVM/unix.

%package pvm-X11
Summary:	PVM/xwin povray executable
Summary(pl):	Plik wykonywalny povray dla PVM/xwin
Group:		Applications/Graphics
Requires:	%{name} = %{version}

%description pvm-X11
The Persistence of Vision(tm) Ray-Tracer PVM/xwin executable.

%description X11 -l pl
Plik wykonywalny The Persistence of Vision(tm) Ray-Tracer dla
PVM/xwin.

%prep
#cd %{_sourcedir}
#md5sum -c %{name}-%{version}.md5sum
#cd -
%setup -q
#%patch0 -p1
%ifarch alpha
%patch1 -p1
%endif

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%if %{!?_without_pvm:%{!?_without_x:1}%{?_without_x:0}}%{?_without_pvm:0}
%configure \
	--enable-pvm \
	--with-pvm-arch=%{_pvmarch} \
	--x-includes=%{_prefix}/X11R6/include \
	--x-libraries=%{_prefix}/X11R6/lib
%{__make}
install src/povray x-pvmpov
%endif

%if %{!?_without_pvm:1}%{?_without_pvm:0}
%{__make} clean

%configure \
	--enable-pvm \
	--with-pvm-arch=%{_pvmarch} \
	--without-x
%{__make}
install src/povray pvmpov
%endif

%if %{!?_without_x:1}%{?_without_x:0}
%configure \
	--x-includes=%{_prefix}/X11R6/include \
	--x-libraries=%{_prefix}/X11R6/lib
%{__make}
install src/povray x-povray
%{__make} clean
%endif

%configure \
	--without-x
%{__make}


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_prefix}/X11R6/bin} \
	$RPM_BUILD_ROOT%{_pvmroot}/bin/%{_pvmarch}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{!?_without_x:1}%{?_without_x:0}
install x-povray $RPM_BUILD_ROOT%{_prefix}/X11R6/bin
%endif

%if %{!?_without_pvm:%{!?_without_x:1}%{?_without_x:0}}%{?_without_pvm:0}
install x-pvmpov $RPM_BUILD_ROOT%{_pvmroot}/bin/%{_pvmarch}/x-pvmpov
%endif

%if %{!?_without_pvm:1}%{?_without_pvm:0}
install pvmpov $RPM_BUILD_ROOT%{_pvmroot}/bin/%{_pvmarch}/pvmpov
%endif

install povray.ini $RPM_BUILD_ROOT%{_sysconfdir}
install povray.conf $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/povray.ini $RPM_BUILD_ROOT%{_datadir}/povray-3.5/povray.ini

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README* povlegal.doc *.txt doc/html
%attr(755,root,root) %{_bindir}/povray
%{_libdir}/povray*
%{_mandir}/man?/*
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/povray.*

%if %{!?_without_x:1}%{?_without_x:0}
%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/X11R6/bin/x-povray
%endif

%if %{!?_without_pvm:1}%{?_without_pvm:0}
%files pvm
%defattr(644,root,root,755)
%attr(755,root,root) %{_pvmroot}/bin/%{_pvmarch}/pvmpov
%endif

%if %{!?_without_pvm:%{!?_without_x:1}%{?_without_x:0}}%{?_without_pvm:0}
%files pvm-X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_pvmroot}/bin/%{_pvmarch}/x-pvmpov
%endif
