# It's possible to backport Miro to 2011 and 2010.2
# but ffmpeg conversion needs to be checked
# In order to use Miro 5.0 in 2010.2 with ffmpeg 0.7.12 from MIB
# I had to make a patch that removes this commit's code:
# https://github.com/paulswartz/miro/commit/42365981a8c4236573419538a3e70cd22f5f5341
# So, it's better to avoid untested backports via build system

%define _files_listed_twice_terminate_build 0

Name:		miro
Version:	6.0
Release:	1
Summary:	Miro Player
Group:		Video
License:	GPLv2+
URL:		http://www.getmiro.com/
Source0:	ftp://ftp.osuosl.org/pub/pculture.org/miro/src/%{name}-%{version}.tar.gz
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(pygtk-2.0)
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	python-pyrex
BuildRequires:	pkgconfig(webkit-1.0)
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(x11)
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(python)
BuildRequires:	ffmpeg-devel
BuildRequires:	pkgconfig(taglib)
Requires:	pygtk2.0
Requires:	python-webkitgtk
Requires:	gnome-python-gconf
Requires:	python-dbus
Requires:	gstreamer0.10-python
Requires:	gstreamer0.10-plugins-good
Requires:	python-libtorrent-rasterbar
Requires:	python-curl
Requires:	mutagen
Requires:	ffmpeg
Requires:	ffmpeg2theora

%description
Internet TV player with integrated RSS and BitTorrent functionality.

%prep
%setup -q

%build
cd linux && CFLAGS="%{optflags}" LDFLAGS="%?ldflags" %__python setup.py build

%install
cd linux && %__python setup.py install -O1 --skip-build --root %{buildroot}
cd ..

%find_lang miro

desktop-file-install --vendor="" \
  --remove-key="Encoding" \
  --remove-category="Application" \
  --add-category="Video" \
  --add-category="Network" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*


# Some binaries that we don't seem to need
%__rm -rf %{buildroot}%{_bindir}/codegen*

%files -f miro.lang
%doc README CREDITS
%attr(755,root,root) %{_bindir}/*
%{_datadir}/miro
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_datadir}/pixmaps/*.xpm
%{_mandir}/man1/*
%{_datadir}/mime/packages/*.xml
%{py_platsitedir}/miro*
