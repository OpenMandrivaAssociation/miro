Name:		miro
Version:	3.5
Release:	%mkrel 3
Summary:	Miro Player
Group:		Video
License:	GPLv2+
URL:		http://www.getmiro.com/
Source0:	ftp://ftp.osuosl.org/pub/pculture.org/miro/src/%name-%version.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	python-gobject-devel
BuildRequires:	python-pyrex
BuildRequires:	webkitgtk-devel
BuildRequires:	desktop-file-utils
BuildRequires:	libx11-devel
BuildRequires:	imagemagick
%py_requires -d
Requires:	pygtk2.0
Requires:	python-webkitgtk
Requires:	gnome-python-gconf
Requires:	dbus-python
Requires:	gstreamer0.10-python
Requires:	gstreamer0.10-plugins-good
Requires:	python-libtorrent-rasterbar
Requires:	python-curl
Provides:	democracy
Obsoletes:	democracy

%description
Internet TV player with integrated RSS and BitTorrent functionality.

%prep
%setup -q -n %name-%version

%build
cd linux && CFLAGS="%{optflags}" LDFLAGS="%?ldflags" %{__python} setup.py build

%install
rm -rf %{buildroot}
cd linux && %{__python} setup.py install -O1 --skip-build --root %{buildroot}
cd ..
%find_lang miro

perl -pi -e 's,miro-72x72.png,%{name},g' %{buildroot}%{_datadir}/applications/*

desktop-file-install --vendor="" \
  --remove-key="Encoding" \
  --remove-category="Application" \
  --add-category="Video" \
  --add-category="Network" \
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
%{_mandir}/man1/*
%{_datadir}/mime/packages/*.xml
%{py_platsitedir}/miro*
