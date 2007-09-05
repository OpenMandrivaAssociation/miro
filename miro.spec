%define mozver %(rpm -q --queryformat %%{VERSION} mozilla-firefox)
%define date 2007-07-24

Name:		miro
Version:	0.9.9
Release:	%mkrel 1
Summary:	Miro Player

Group:		Video
License:	GPLv2+
URL:		http://www.getmiro.com/
Source0:	ftp://ftp.osuosl.org/pub/pculture.org/miro/src/Miro-%version.tar.gz
# gw from Debian: don't check for software updates
Patch1:		Democracy-0.9.9-no-autoupdate.patch
Patch2:		Miro-0.9.8-mime-package.patch
# gw https://develop.participatoryculture.org/trac/democracy/ticket/7270
Patch3:		dbus-fix.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	pygtk2.0-devel
BuildRequires:	libxine-devel 
BuildRequires:	python-pyrex
#BuildRequires:	libfame 
BuildRequires:	boost-devel
BuildRequires:	libxcb-devel libpthread-stubs
BuildRequires:	gtk2-devel
BuildRequires:	mozilla-firefox-devel
BuildRequires:	desktop-file-utils
BuildRequires:	libxv-devel
Requires:	pygtk2.0-libglade
Requires:	gnome-python-gtkmozembed gnome-python-gconf dbus-python
Requires:	python-pyrex
#Requires:	libfame 
Requires:	libmozilla-firefox = %mozver

Requires(post):		desktop-file-utils
Requires(postun):	desktop-file-utils

Provides:	democracy
Obsoletes:	democracy

%description
Internet TV player with integrated RSS and BitTorrent functionality.

%prep
%setup -q -n Miro-%version
%patch1 -p0 -b .no-autoupdate
%patch2 -p1 -b .mime
#%patch3 -p0

%build
cd platform/gtk-x11 && CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
cd platform/gtk-x11 && %{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
cd ../..
%find_lang miro

perl -pi -e 's,miro-72x72.png,%{name},g' $RPM_BUILD_ROOT%{_datadir}/applications/*

desktop-file-install --vendor="" \
  --remove-key="Encoding" \
  --remove-category="Application" \
  --add-category="Video" \
  --add-category="TV" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{24x24,72x72,128x128}/apps
cp -f %{buildroot}%{_datadir}/pixmaps/%{name}-24x24.png %{buildroot}%{_iconsdir}/hicolor/24x24/apps/%{name}.png
cp -f %{buildroot}%{_datadir}/pixmaps/%{name}-72x72.png %{buildroot}%{_iconsdir}/hicolor/72x72/apps/%{name}.png
cp -f %{buildroot}%{_datadir}/pixmaps/%{name}-128x128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

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
%{_mandir}/man1/*
%{_datadir}/mime/packages/*.xml
%{py_platsitedir}/miro*

