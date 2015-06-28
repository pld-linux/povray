#
# Conditional build:
%bcond_without	x	# - without X11 subpackage
%bcond_with	pvm	# - with PVM support
%bcond_with	svga	# - with svgalib support (doesn't work on many platforms)
#
Summary:	Persistence of Vision Ray Tracer
Summary(pl.UTF-8):	Persistence of Vision Ray Tracer
Name:		povray
Version:	3.7.0.0
Release:	1
Epoch:		1
License:	distributable
Group:		Applications/Graphics
Source0:	https://github.com/POV-Ray/povray/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c9473256677808e9e3246e6eb8f69a75
Source1:	%{name}-ax_boost_base.m4
Patch0:		boost-1.50.patch
URL:		http://www.povray.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.4.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
%{?with_pvm:BuildRequires:	pvm-devel >= 3.4.3-24}
%{?with_svga:BuildRequires:	svgalib-devel}
%{?with_x:BuildRequires:	xorg-lib-libX11-devel}
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with pvm}
%define		_pvmarch	%(/usr/bin/pvmgetarch)
%define		_pvmroot	/usr/%{_lib}/pvm3
%endif

%description
The Persistence of Vision(tm) Ray-Tracer creates three-dimensional,
photo-realistic images using a rendering technique called ray-tracing.
It reads in a text file containing information describing the objects
and lighting in a scene and generates an image of that scene from the
view point of a camera also described in the text file. Ray-tracing is
not a fast process by any means, but it produces very high quality
images with realistic reflections, shading, perspective and other
effects.

%description -l pl.UTF-8
Persistence of Vision(tm) Ray-Tracer tworzy trójwymiarowe,
fotorealistyczne obrazy za pomocą techniki renderingu zwanej
ray-tracing. Program pobiera z pliku tekstowego informacje opisujące
obiekty oraz światło przedstawianego świata, a następnie generuje
rysunek z punktu widzenia kamery, która także jest definiowana w w/w
pliku tekstowym. Ray-tracing nie pozwala na szybkie tworzenie obrazów,
ale za to twórca otrzymuje wyskokiej jakości bitmapy z realistycznymi
efektami, tj. odbicia światła, cienie, perspektywa i inne.

%package X11
Summary:	X Window povray executable
Summary(pl.UTF-8):	povray pod X Window
Group:		Applications/Graphics
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description X11
The Persistence of Vision(tm) Ray-Tracer X Window executable.

%description X11 -l pl.UTF-8
Plik wykonywalny The Persistence of Vision(tm) Ray-Tracer dla X
Window.

%package pvm
Summary:	PVM/Unix povray executable
Summary(pl.UTF-8):	Plik wykonywalny povray dla PVM/Unix
Group:		Applications/Graphics
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description pvm
The Persistence of Vision(tm) Ray-Tracer PVM/Unix executable.

%description pvm -l pl.UTF-8
Plik wykonywalny The Persistence of Vision(tm) Ray-Tracer dla
PVM/Unix.

%package pvm-X11
Summary:	PVM/xwin povray executable
Summary(pl.UTF-8):	Plik wykonywalny povray dla PVM/xwin
Group:		Applications/Graphics
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description pvm-X11
The Persistence of Vision(tm) Ray-Tracer PVM/xwin executable.

%description pvm-X11 -l pl.UTF-8
Plik wykonywalny The Persistence of Vision(tm) Ray-Tracer dla
PVM/xwin.

%prep
%setup -q
cp %{SOURCE1} unix/config/ax_boost_base.m4
%patch0 -p1

%build
cd unix
./prebuild.sh
cd ..

%{__automake}
COMPILED_BY="PLD/Linux Team";export COMPILED_BY;
%if %{with x} && %{with pvm}
%configure \
	--libdir=%{_datadir} \
	--enable-pvm \
	--with-pvm-arch=%{_pvmarch} \
	--with-pvm-libs=%{_libdir}
%{__make}
install unix/povray x-pvmpov
%endif

%if %{with pvm}
%{__make} clean

%configure \
	--libdir=%{_datadir} \
	--enable-pvm \
	--with-pvm-arch=%{_pvmarch} \
	--with-pvm-libs=%{_libdir} \
	--without-x
%{__make}
install unix/povray pvmpov
%endif

%if %{with x}
%configure \
	--libdir=%{_datadir}
%{__make}
install unix/povray x-povray
%{__make} clean
%endif

%configure \
	--libdir=%{_datadir} \
	--without-x
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_datadir}}
%if %{with pvm}
install -d $RPM_BUILD_ROOT%{_pvmroot}/bin/%{_pvmarch}
%endif

%{__make} install \
	INSTALL="install -c -D" \
	mkdir_p="mkdir -p" \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with x}
install x-povray $RPM_BUILD_ROOT%{_bindir}
%endif

%if %{with x} && %{with pvm}
install x-pvmpov $RPM_BUILD_ROOT%{_bindir}/x-pvmpov
ln -s %{_bindir}/x-pvmpov $RPM_BUILD_ROOT%{_pvmroot}/bin/%{_pvmarch}/x-pvmpov
%endif

%if %{with pvm}
install pvmpov $RPM_BUILD_ROOT%{_bindir}/pvmpov
ln -s %{_bindir}/pvmpov $RPM_BUILD_ROOT%{_pvmroot}/bin/%{_pvmarch}/pvmpov
%endif

##install povray.ini $RPM_BUILD_ROOT%{_sysconfdir}
##install povray.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README* changes.txt
%attr(755,root,root) %{_bindir}/povray
%{_datadir}/povray*
%{_docdir}/povray*
%{_mandir}/man?/*
%dir %{_sysconfdir}/povray
%dir %{_sysconfdir}/povray/3.7
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/3.7/povray.*
## %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/povray.*

%if %{with x}
%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/x-povray
%endif

%if %{with pvm}
%files pvm
%defattr(644,root,root,755)
%attr(755,root,root) %{_pvmroot}/bin/%{_pvmarch}/pvmpov
%attr(755,root,root) %{_bindir}/pvmpov
%endif

%if %{with pvm} && %{with x}
%files pvm-X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_pvmroot}/bin/%{_pvmarch}/x-pvmpov
%attr(755,root,root) %{_bindir}/x-pvmpov
%endif
