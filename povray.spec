#
# Conditional build:
# _without_x	- without X11 subpackage
# _without_pvm	- [temporarily disabled by default] without PVM support
#
Summary:	Persistence of Vision Ray Tracer
Summary(pl):	Persistence of Vision Ray Tracer
Name:		povray
Version:	3.50b
Release:	2
License:	distributable
Group:		Applications/Graphics
Source0:	ftp://ftp.povray.org/pub/povray/Official/Unix/povuni_s.tgz
Patch0:		%{name}-legal.patch
Patch1:		%{name}-types.patch
# pvm support not yet available - http://pvmpov.sourceforge.net/
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
Persistence of Vision(tm) Ray-Tracer tworzy tr�jwymiarowe,
fotorealistyczne obrazy za pomoc� techniki renderingu zwanej
ray-tracing. Program pobiera z pliku tekstowego informacje opisuj�ce
obiekty oraz �wiat�o przedstawianego �wiata, a nast�pnie generuje
rysunek z punktu widzenia kamery, kt�ra tak�e jest definiowana w w/w
pliku tekstowym. Ray-tracing nie pozwala na szybkie tworzenie obraz�w,
ale za to tw�rca otrzymuje wyskokiej jako�ci bitmapy z realistycznymi
efektami, tj. odbicia �wiat�a, cienie, perspektywa i inne.

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
Group:		Applications/Graphics
Requires:	%{name} = %{version}

%description pvm
The Persistence of Vision(tm) Ray-Tracer PVM/unix executable.

%description X11 -l pl
Plik wykonywalny The Persistence of Vision(tm) Ray-Tracer dla
PVM/unix.

%package pvm-X11
Summary:	PVM/xwin povray executable
Group:		Applications/Graphics
Requires:	%{name} = %{version}

%description pvm-X11
The Persistence of Vision(tm) Ray-Tracer PVM/xwin executable.

%description X11 -l pl
Plik wykonywalny The Persistence of Vision(tm) Ray-Tracer dla
PVM/xwin.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	--x-includes=%{_prefix}/X11R6/include \
	--x-libraries=%{_prefix}/X11R6/lib
%{__make}
install src/povray x-povray
%{__make} clean

%configure \
	--without-x
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_prefix}/X11R6/bin}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install x-povray $RPM_BUILD_ROOT%{_prefix}/X11R6/bin
install povray.ini $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/povray.ini $RPM_BUILD_ROOT%{_datadir}/povray-*/povray.ini

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README* povlegal.doc *.txt doc/html
%attr(755,root,root) %{_bindir}/povray
%{_libdir}/povray*
%{_mandir}/man?/*
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/povray.ini

%if %{!?_without_x:1}%{?_without_x:0}
%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/X11R6/bin/x-povray
%endif

#%if %{!?_without_pvm:1}%{?_without_pvm:0}
#%files pvm
#%defattr(644,root,root,755)
#%attr(755,root,root) %{_pvm_root}/bin/%{_pvm_arch}/pvmpov
#
#%if %{!?_without_x:1}%{?_without_x:0}
#%files pvm-X11
#%defattr(644,root,root,755)
#%attr(755,root,root) %{_pvm_root}/bin/%{_pvm_arch}/x-pvmpov
#%endif
#%endif
