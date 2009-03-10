%if %mdvver < 200900
%define mozver %(rpm -q --queryformat %%{VERSION} mozilla-firefox)
%else
%define xulrunner 1.9
%define libname %mklibname xulrunner %xulrunner
%define xulver %(rpm -q --queryformat %%{VERSION} %libname)
%endif
Name:		miro
Version:	2.0.1
Release:	%mkrel 2
Summary:	Miro Player
Group:		Video
License:	GPLv2+
URL:		http://www.getmiro.com/
Source0:	ftp://ftp.osuosl.org/pub/pculture.org/miro/src/Miro-%version.tar.gz
# gw os.getlogin() fails in the build system
Patch4: miro-2.0-work-around-python-problem.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	pygtk2.0-devel
BuildRequires:	libxine-devel 
BuildRequires:	python-pyrex
BuildRequires:	openssl-devel
%if %mdvver >= 200900
BuildRequires:	xcb-devel
%else
BuildRequires:	libxcb-devel
BuildRequires:	libpthread-stubs
%endif
BuildRequires:	gtk2-devel
%if %mdvver < 200900
BuildRequires:	mozilla-firefox-devel
%else
BuildRequires:	xulrunner-devel-unstable >= %xulrunner
%endif
BuildRequires:	desktop-file-utils
BuildRequires:	libxv-devel
BuildRequires:	imagemagick
%if %mdvver > 200810
BuildRequires:	libtorrent-rasterbar-devel
BuildRequires:	python-libtorrent-rasterbar
Requires:	python-libtorrent-rasterbar
%else
BuildRequires:  libboost-devel
%endif
Requires:	pygtk2.0-libglade
Requires:	gnome-python-gtkmozembed
Requires:	gnome-python-gconf
Requires:	dbus-python
Requires:	python-pyrex
Requires:	gstreamer0.10-python
Requires:	gstreamer0.10-plugins-base
%if %mdvver < 200900
Requires:	libmozilla-firefox = %mozver
%else
#gw as Fedora does:
Requires: %libname = %xulver
%endif

Requires(post):		desktop-file-utils
Requires(postun):	desktop-file-utils

Provides:	democracy
Obsoletes:	democracy

%description
Internet TV player with integrated RSS and BitTorrent functionality.

%prep
%setup -q -n Miro-%version
%patch4 -p1
#gw fix wrong libdir
perl -pi -e "s^lib/miro^%_lib/miro^" ./platform/gtk-x11/plat/renderers/xinerenderer.py platform/gtk-x11/setup.py



%build
cd platform/gtk-x11 && CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
cd platform/gtk-x11 && %{__python} setup.py install -O1 --skip-build --root %{buildroot}
cd ../..
%find_lang miro

perl -pi -e 's,miro-72x72.png,%{name},g' %{buildroot}%{_datadir}/applications/*

desktop-file-install --vendor="" \
  --remove-key="Encoding" \
  --remove-category="Application" \
  --add-category="Video" \
  --add-category="TV" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{24x24,48x48,72x72,128x128}/apps
cp -f %{buildroot}%{_datadir}/pixmaps/%{name}-24x24.png %{buildroot}%{_iconsdir}/hicolor/24x24/apps/%{name}.png
cp -f %{buildroot}%{_datadir}/pixmaps/%{name}-72x72.png %{buildroot}%{_iconsdir}/hicolor/72x72/apps/%{name}.png
cp -f %{buildroot}%{_datadir}/pixmaps/%{name}-128x128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png
convert -scale 48x48 %{buildroot}%{_datadir}/pixmaps/%{name}-72x72.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

gunzip %buildroot%{_mandir}/man1/*.gz

%clean
rm -rf %{buildroot}

%post
%update_desktop_database
%update_mime_database
%update_icon_cache hicolor

%postun
%clean_desktop_database
%clean_mime_database
%clean_icon_cache hicolor

%files -f miro.lang
%defattr(-,root,root,-)
%doc README CREDITS
%attr(755,root,root) %_bindir/*
%{_datadir}/miro
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_datadir}/pixmaps/*.png
%dir %_libdir/miro/
%_libdir/miro/xine_extractor
%{_mandir}/man1/*
%{_datadir}/mime/packages/*.xml
%{py_platsitedir}/miro*

