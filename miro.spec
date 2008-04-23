%define mozver %(rpm -q --queryformat %%{VERSION} mozilla-firefox)

Name:		miro
Version:	1.2.3
Release:	%mkrel 1
Summary:	Miro Player
Group:		Video
License:	GPLv2+
URL:		http://www.getmiro.com/
Source0:	ftp://ftp.osuosl.org/pub/pculture.org/miro/src/Miro-%version.tar.gz
# gw from Debian: don't check for software updates
# AdamW: rediffed for 1.2.1 - 2008/03
Patch1:		Miro-1.2.1-no-autoupdate.patch
# gw os.getlogin() fails in the build system
Patch4: Miro-0.9.9.9-work-around-python-problem.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	pygtk2.0-devel
BuildRequires:	libxine-devel 
BuildRequires:	python-pyrex
#BuildRequires:	libfame 
BuildRequires:	boost-devel
BuildRequires:	openssl-devel
BuildRequires:	libxcb-devel libpthread-stubs
BuildRequires:	gtk2-devel
BuildRequires:	mozilla-firefox-devel
BuildRequires:	desktop-file-utils
BuildRequires:	libxv-devel
BuildRequires:	ImageMagick
Requires:	pygtk2.0-libglade
Requires:	gnome-python-gtkmozembed gnome-python-gconf dbus-python
Requires:	python-pyrex
#Requires:	libfame 
Requires: gstreamer0.10-python
Requires: gstreamer0.10-plugins-base
Requires:	libmozilla-firefox = %mozver

Requires(post):		desktop-file-utils
Requires(postun):	desktop-file-utils

Provides:	democracy
Obsoletes:	democracy

%description
Internet TV player with integrated RSS and BitTorrent functionality.

%prep
%setup -q -n Miro-%version
%patch1 -p1 -b .no-autoupdate
%patch4 -p1
#gw fix wrong libexec dir
perl -pi -e "s^libexec^%_lib^" ./platform/gtk-x11/platform/renderers/xinerenderer.py platform/gtk-x11/setup.py



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
%_libexecdir/xine_extractor
%{_mandir}/man1/*
%{_datadir}/mime/packages/*.xml
%{py_platsitedir}/miro*

