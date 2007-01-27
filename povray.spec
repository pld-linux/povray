#
# Conditional build:
%bcond_without	x	# - without X11 subpackage
%bcond_with	pvm		# - with PVM support
%bcond_with	svga	# - with svgalib support (doesn't work on many platforms)
#
%define		_src_pov_ver	3.6.1

Summary:	Persistence of Vision Ray Tracer
Summary(pl):	Persistence of Vision Ray Tracer
Name:		povray
Version:	3.6.1
Release:	1
Epoch:		1
License:	distributable
Group:		Applications/Graphics
Source0:	http://www.povray.org/ftp/pub/povray/Official/Unix/%{name}-%{_src_pov_ver}.tar.bz2
# Source0-md5:	b5789bb7eeaed0809c5c82d0efda571d
# based on sources from CVS at http://pvmpov.sourceforge.net/
# Source0:	%{name}-%{version}-%{snap}.tar.gz
Patch0:		%{name}-legal.patch
Patch1:		%{name}-64bit.patch
Patch2:		%{name}-X-libs.patch
Patch3:		%{name}-lib64.patch
Patch4:		%{name}-no_svgalib.patch
Patch5:		%{name}-m4.patch
URL:		http://www.povray.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.0.8
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
Requires:	%{name} = %{version}-%{release}

%description X11
The Persistence of Vision(tm) Ray-Tracer X Window executable.

%description X11 -l pl
Plik wykonywalny The Persistence of Vision(tm) Ray-Tracer dla X
Window.

%package pvm
Summary:	PVM/unix povray executable
Summary(pl):	Plik wykonywalny povray dla PVM/unix
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description pvm
The Persistence of Vision(tm) Ray-Tracer PVM/unix executable.

%description pvm -l pl
Plik wykonywalny The Persistence of Vision(tm) Ray-Tracer dla
PVM/unix.

%package pvm-X11
Summary:	PVM/xwin povray executable
Summary(pl):	Plik wykonywalny povray dla PVM/xwin
Group:		Applications/Graphics
Requires:	%{name} = %{version}-%{release}

%description pvm-X11
The Persistence of Vision(tm) Ray-Tracer PVM/xwin executable.

%description pvm-X11 -l pl
Plik wykonywalny The Persistence of Vision(tm) Ray-Tracer dla
PVM/xwin.

%prep
%setup -q
##%patch1 -p1
##%patch2 -p1
%if "%{_lib}" == "lib64"
##%patch3 -p1
%endif
%if !%{with svga}
##%patch4 -p1
%endif
%patch5 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
COMPILED_BY="PLD/Linux Team";export COMPILED_BY;
%if %{with x} && %{with pvm}
%configure \
	--libdir=%{_datadir} \
	--enable-pvm \
	--with-pvm-arch=%{_pvmarch} \
	--with-pvm-libs=%{_libdir} \
	--x-includes=/usr/X11R6/include \
	--x-libraries=/usr/X11R6/%{_lib}
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
	--libdir=%{_datadir} \
	--x-includes=/usr/X11R6/include \
	--x-libraries=/usr/X11R6/%{_lib}
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
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/usr/X11R6/bin}
%if %{with pvm}
install -d $RPM_BUILD_ROOT%{_pvmroot}/bin/%{_pvmarch}
%endif

%{__make} install \
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
%doc AUTHORS ChangeLog NEWS README* doc/povlegal.doc doc/*.txt doc/html
%attr(755,root,root) %{_bindir}/povray
%{_datadir}/povray*
%{_docdir}/povray*
%{_mandir}/man?/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/3.6/povray.*
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
