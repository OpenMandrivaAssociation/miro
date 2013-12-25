Summary:	Miro Player
Name:		miro
Version:	6.0
Release:	4
License:	GPLv2+
Group:		Video
Url:		http://www.getmiro.com/
Source0:	ftp://ftp.osuosl.org/pub/pculture.org/miro/src/%{name}-%{version}.tar.gz
Patch0:		miro-6.0-charrefs.patch
Patch1:		miro-6.0-sqlite-fixes.patch
Patch2:		miro-6.0-video-controls.patch
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	python-pyrex
BuildRequires:	boost-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	pkgconfig(pygtk-2.0)
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(taglib)
BuildRequires:	pkgconfig(webkit-1.0)
BuildRequires:	pkgconfig(x11)
Requires:	gnome-python-gconf
Requires:	dbus-python
Requires:	ffmpeg
Requires:	ffmpeg2theora
Requires:	gstreamer0.10-python
Requires:	gstreamer0.10-plugins-good
Requires:	mutagen
Requires:	pygtk2.0
Requires:	python-curl
Requires:	python-libtorrent-rasterbar
Requires:	python-webkitgtk

%description
Internet TV player with integrated RSS and BitTorrent functionality.

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

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p2
%patch1 -p2
%patch2 -p2

%build
pushd linux
CFLAGS="%{optflags}" LDFLAGS="%{ldflags}" python setup.py build
popd

%install
pushd linux
python setup.py install -O1 --skip-build --root %{buildroot}
popd

%find_lang miro
sed -i '/.*testdata.*/d' miro.lang

desktop-file-install --vendor="" \
	--remove-key="Encoding" \
	--remove-category="Application" \
	--add-category="Video" \
	--add-category="Network" \
	--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Some binaries that we don't seem to need
rm -rf %{buildroot}%{_bindir}/codegen*

