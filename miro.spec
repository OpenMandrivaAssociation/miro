#gw as Fedora does:
%define xulrunner 1.9
%define libname %mklibname xulrunner %xulrunner
%define xulver %(rpm -q --queryformat %%{VERSION} %libname)

Name:		miro
Version:	2.5.2
Release:	%mkrel 4
Summary:	Miro Player
Group:		Video
License:	GPLv2+
URL:		http://www.getmiro.com/
Source0:	ftp://ftp.osuosl.org/pub/pculture.org/miro/src/Miro-%version.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	pygtk2.0-devel
BuildRequires:	libxine-devel 
BuildRequires:	python-pyrex
BuildRequires:	openssl-devel
BuildRequires:	libgsf-devel
%if %mdvver >= 200900
BuildRequires:	xcb-devel
%else
BuildRequires:	libxcb-devel
BuildRequires:	libpthread-stubs
%endif
BuildRequires:	gtk2-devel
%if %mdvver >= 201000
BuildRequires:	xulrunner-devel >= %xulver
%else
BuildRequires:	xulrunner-devel-unstable >= %xulver
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
%if %mdvver >= 201000
Requires: libxulrunner = %{xulrunner_version}
%else
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
%{_datadir}/pixmaps/*.xpm
%dir %_libdir/miro/
%_libdir/miro/xine_extractor
%{_mandir}/man1/*
%{_datadir}/mime/packages/*.xml
%{py_platsitedir}/miro*

