# $Revision: 1.1 $
Summary:       Persistence of Vision Ray Tracer
Summary(pl):   Persistence of Vision Ray Tracer
Name:          povray
Version:       3.1g
Release:       1
Copyright:     distrituable
Group:         Applications/Graphics
Group(pl):     Aplikacje/Grafika
Source0:       povuni_s.tgz
Source1:       povuni_d.tgz
Patch0:        povray31-makefile_and_config.patch
URL:           http://www.povray.org/
BuildRequires: zlib-devel
BuildRequires: libpng-devel
BuildRoot:    /tmp/%{name}-%{version}-root

%define		_prefix		/usr/X11R6
%define		_infodir	/usr/share/info
%define		_mandir		/usr/X11R6/man
%define		_sysconfdir	/etc/X11

%description
From the user manual:

The Persistence of Vision(tm) Ray-Tracer creates three-dimensional,
photo-realistic images using a rendering technique called ray-tracing. It reads
in a text file containing information describing the objects and lighting in a
scene and generates an image of that scene from the view point of a camera also
described in the text file. Ray-tracing is not a fast process by any means,
but it produces very high quality images with realistic reflections, shading,
perspective and other effects.

%description -l pl
Z podr�cznika u�ytkownika:

Persistence of Vision(tm) Ray-Tracer tworzy tr�jwymiarowe, fotorealistyczne
obrazy za pomoc� techniki renderingu zwanej ray-tracing. Program pobiera z
pliku tekstowego informacje opisuj�ce obiekty oraz �wiat�o przedstawianego
�wiata, a nast�pnie generuje rysunek z punktu widzenia kamery, kt�ra tak�e jest
definiowana w w/w pliku tekstowym. Ray-tracing nie pozwala na szybkie tworzenie
obraz�w, ale za to tw�rca otrzymuje wyskokiej jako�ci bitmapy z realistycznymi
efektami, tj. odbicia �wiat�a, cienie, perspektywa i inne.

%prep
%setup -q -n povray31
pushd ..
tar zxf %{SOURCE1}
popd

%patch0 -p1

%build
pushd source/unix
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DCPU=`echo %{_target_cpu} | sed 's/^i\([3-9]86\)$/\1/'`"
make newunix
make newxwin
popd

%install
pushd source/unix
install -d $RPM_BUILD_ROOT/usr/bin
install -d $RPM_BUILD_ROOT/etc/skel
install -s -m 755 povray x-povray $RPM_BUILD_ROOT/usr/bin
install -m 644 povrayrc $RPM_BUILD_ROOT/etc/skel/.povrayrc
popd

gzip -9nf gamma.gif.txt povray.1 povlegal.doc
bzip2 povuser.txt

install -d $RPM_BUILD_ROOT/usr/share/man/man1
install -m 644 povray.1.gz $RPM_BUILD_ROOT/usr/share/man/man1

install -d $RPM_BUILD_ROOT/usr/share/povray31
find . -type f -exec chmod 644 {} \;
cp -r allscene include scenes $RPM_BUILD_ROOT/usr/share/povray31
install -m 644 *.ini $RPM_BUILD_ROOT/usr/share/povray31
install -m 644 *.pov $RPM_BUILD_ROOT/usr/share/povray31

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc gamma.gif.txt.gz povuser.txt.bz2 gamma.gif povlegal.doc.gz
/usr/bin/x-povray
/usr/bin/povray
/usr/share/povray31
/etc/skel/.povrayrc