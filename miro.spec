%define mozver %(rpm -q --queryformat %%{VERSION} mozilla-firefox)

Name:           miro
Version:        0.9.8
Release:        %mkrel 3
Summary:        Miro Player

Group:          Video
License:        GPL
URL:            http://www.getmiro.com/
Source0:        ftp://ftp.osuosl.org/pub/pculture.org/miro/src/Miro-%version.tar.bz2
# gw use the standard mdk folders, remove this once we move to xdg-user-dirs
Patch: Miro-0.9.8-mdk-folders.patch
# gw from Debian: don't check for software updates
Patch1: Democracy-0.9.5.3-no-autoupdate.patch
Patch2: Miro-0.9.8-mime-package.patch
# gw https://develop.participatoryculture.org/trac/democracy/ticket/7270
Patch3: dbus-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  pygtk2.0-devel
BuildRequires:  libxine-devel 
BuildRequires:  python-pyrex
#BuildRequires:  libfame 
BuildRequires:  boost-devel
BuildRequires:  libxcb-devel libpthread-stubs
BuildRequires:  gtk2-devel
BuildRequires:  mozilla-firefox-devel
BuildRequires: desktop-file-utils
Requires:	gnome-python-gtkmozembed gnome-python-gconf dbus-python
Requires: python-pyrex
#Requires: libfame 
Requires:	libmozilla-firefox = %mozver
Requires(post)  : desktop-file-utils
Requires(postun): desktop-file-utils
Provides: democracy
Obsoletes: democracy

%description
Internet TV player with integrated RSS and BitTorrent functionality.


%prep
%setup -q -n Miro-%version
%patch -p1 -b .mdk-folders
%patch1 -p0 -b .no-autoupdate
%patch2 -p1 -b .mime
%patch3 -p0

%build
cd platform/gtk-x11 && CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
cd platform/gtk-x11 && %{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
cd ../..
%find_lang miro

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*
#mv %buildroot%_bindir/miro %buildroot%_bindir/miro.real
#cat > %buildroot%_bindir/miro << EOF
##!/bin/sh
#LD_LIBRARY_PATH=%_libdir/firefox-%mozver miro.real "\$@"
#EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_mime_database

%postun
%clean_desktop_database
%clean_mime_database

%files -f miro.lang
%defattr(-,root,root,-)
%doc README CREDITS
%attr(755,root,root) %_bindir/*
%{_datadir}/miro
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_mandir}/man1/*
%{_datadir}/mime/packages/*.xml
%{py_platsitedir}/miro*
