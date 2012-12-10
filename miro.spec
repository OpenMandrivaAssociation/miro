# It's possible to backport Miro to 2011 and 2010.2
# but ffmpeg conversion needs to be checked
# In order to use Miro 5.0 in 2010.2 with ffmpeg 0.7.12 from MIB
# I had to make a patch that removes this commit's code:
# https://github.com/paulswartz/miro/commit/42365981a8c4236573419538a3e70cd22f5f5341
# So, it's better to avoid untested backports via build system

%define _files_listed_twice_terminate_build 0

Name:		miro
Version:	5.0.4
Release:	1
Summary:	Miro Player
Group:		Video
License:	GPLv2+
URL:		http://www.getmiro.com/
Source0:	ftp://ftp.osuosl.org/pub/pculture.org/miro/src/%{name}-%{version}.tar.gz
Patch0:		miro-5.0-ffmpeg0.11.patch
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(pygtk-2.0)
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	python-pyrex
BuildRequires:	pkgconfig(webkit-1.0)
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(x11)
BuildRequires:	imagemagick
BuildRequires:	python-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	pkgconfig(taglib)
Requires:	pygtk2.0
Requires:	python-webkitgtk
Requires:	gnome-python-gconf
Requires:	dbus-python
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
%patch0 -p0

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



%changelog
* Thu May 31 2012 Andrey Bondrov <abondrov@mandriva.org> 5.0-1
+ Revision: 801534
- Update BuildRequires and Requires
- New version 5.0

  + Alexander Khrukin <akhrukin@mandriva.org>
    - version update 4.0.6

* Fri Dec 30 2011 Götz Waschk <waschk@mandriva.org> 4.0.4-1
+ Revision: 748246
- new version

* Wed Dec 21 2011 Guilherme Moro <guilherme@mandriva.com> 4.0.3-2
+ Revision: 744207
- add Requires for ffmpeg2theora

* Fri Nov 11 2011 Götz Waschk <waschk@mandriva.org> 4.0.3-1
+ Revision: 730119
- new version
- build with ffmpeg0.7

* Mon Jun 20 2011 Funda Wang <fwang@mandriva.org> 4.0.1.1-2
+ Revision: 686159
- rebuild for new webkit

* Fri Jun 03 2011 Funda Wang <fwang@mandriva.org> 4.0.1.1-1
+ Revision: 682552
- new version 4.0.1.1

* Wed May 25 2011 Funda Wang <fwang@mandriva.org> 4.0.1-1
+ Revision: 678930
- new version 4.0.1

* Tue May 24 2011 Bogdano Arendartchuk <bogdano@mandriva.com> 4.0-2
+ Revision: 678231
- added requires for mutagen

* Mon May 23 2011 Funda Wang <fwang@mandriva.org> 4.0-1
+ Revision: 677496
- new version 4.0

* Tue Dec 07 2010 Funda Wang <fwang@mandriva.org> 3.5.1-1mdv2011.0
+ Revision: 613379
- update to new version 3.5.1

* Wed Nov 03 2010 Michael Scherer <misc@mandriva.org> 3.5-3mdv2011.0
+ Revision: 592729
- rebuild for python 2.7

  + Funda Wang <fwang@mandriva.org>
    - BR python-devel

* Fri Oct 22 2010 Funda Wang <fwang@mandriva.org> 3.5-2mdv2011.0
+ Revision: 587200
- adjust runtime requires
- simplify BRs

* Fri Oct 22 2010 Funda Wang <fwang@mandriva.org> 3.5-1mdv2011.0
+ Revision: 587193
- New version 3.5 (webkit based)

* Wed Sep 08 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 3.0.3-2mdv2011.0
+ Revision: 576818
- rebuild for new xulrunner 2.0b5

  + Ahmad Samir <ahmadsamir@mandriva.org>
    - rebuild for xulrunner1.9.2.8

* Tue Jul 27 2010 Funda Wang <fwang@mandriva.org> 3.0.3-1mdv2011.0
+ Revision: 561095
- new version 3.0.3

* Tue Jul 20 2010 Funda Wang <fwang@mandriva.org> 3.0.2-1mdv2011.0
+ Revision: 555066
- update to new version 3.0.2

* Mon Jun 28 2010 Frederic Crozat <fcrozat@mandriva.com> 3.0.1-4mdv2010.1
+ Revision: 549374
- rebuild with latest xulrunner

* Wed Apr 14 2010 Funda Wang <fwang@mandriva.org> 3.0.1-3mdv2010.1
+ Revision: 534633
- add network category as suggested by d-f-i
- use ldflags

* Wed Apr 14 2010 Funda Wang <fwang@mandriva.org> 3.0.1-1mdv2010.1
+ Revision: 534631
- update to new version 3.0.1

* Mon Apr 05 2010 Ahmad Samir <ahmadsamir@mandriva.org> 3.0-3mdv2010.1
+ Revision: 531515
- rebuild for new xulrunner

* Mon Mar 29 2010 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 3.0-2mdv2010.1
+ Revision: 528660
- Force setting XPCOM_RUNTIME_PATH/MOZILLA_LIB_PATH in setup.py to avoid
  build not detecting properly xpcom (avoids crash on start with current
  miro)

* Fri Mar 26 2010 Götz Waschk <waschk@mandriva.org> 3.0-1mdv2010.1
+ Revision: 527858
- new version
- remove obsolete deps
- update file list

* Wed Mar 24 2010 Götz Waschk <waschk@mandriva.org> 2.5.4-6mdv2010.1
+ Revision: 527114
- rebuild for new xulrunner

* Mon Feb 08 2010 Anssi Hannula <anssi@mandriva.org> 2.5.4-5mdv2010.1
+ Revision: 501882
- rebuild for new boost

* Wed Feb 03 2010 Funda Wang <fwang@mandriva.org> 2.5.4-4mdv2010.1
+ Revision: 500306
- rebuild for new boost

* Sun Jan 10 2010 Götz Waschk <waschk@mandriva.org> 2.5.4-3mdv2010.1
+ Revision: 488678
- rebuild for new xulrunner

* Wed Dec 16 2009 Götz Waschk <waschk@mandriva.org> 2.5.4-2mdv2010.1
+ Revision: 479453
- rebuild for new xulrunner

* Sun Dec 06 2009 Funda Wang <fwang@mandriva.org> 2.5.4-1mdv2010.1
+ Revision: 474199
- new version 2.5.4

* Thu Nov 12 2009 Götz Waschk <waschk@mandriva.org> 2.5.3-1mdv2010.1
+ Revision: 465170
- new version

* Mon Sep 21 2009 Thierry Vignaud <tv@mandriva.org> 2.5.2-5mdv2010.0
+ Revision: 446473
- fix percent-in-dependency error

* Mon Sep 14 2009 Götz Waschk <waschk@mandriva.org> 2.5.2-4mdv2010.0
+ Revision: 439653
- fix build deps
- rebuild for new xulrunner

* Tue Aug 18 2009 Götz Waschk <waschk@mandriva.org> 2.5.2-3mdv2010.0
+ Revision: 417751
- update runtime deps for new xulrunner
- update build deps for new xulrunner
- drop patch, no longer needed

* Tue Aug 04 2009 Götz Waschk <waschk@mandriva.org> 2.5.2-2mdv2010.0
+ Revision: 409368
- rebuild for new xulrunner

* Fri Jul 31 2009 Frederik Himpe <fhimpe@mandriva.org> 2.5.2-1mdv2010.0
+ Revision: 405212
- update to new version 2.5.2

* Sat Jul 25 2009 Frederik Himpe <fhimpe@mandriva.org> 2.5.1-1mdv2010.0
+ Revision: 399842
- Update to new version 2.5.1
- No need anymore to copy icon images to right directory, it's done now
  automatically by Miro's installer

* Fri Jul 24 2009 Götz Waschk <waschk@mandriva.org> 2.0.5-2mdv2010.0
+ Revision: 399188
- rebuild for new xulrunner

* Sat Jun 27 2009 Frederik Himpe <fhimpe@mandriva.org> 2.0.5-1mdv2010.0
+ Revision: 389802
- Update to new version 2.0.5
- BuildRequires libgsf-devel now

* Sun Jun 14 2009 Colin Guthrie <cguthrie@mandriva.org> 2.0.4-3mdv2010.0
+ Revision: 385839
- Rebuild against new xulrunner

  + Götz Waschk <waschk@mandriva.org>
    - build against xulrunner on 2008.1

* Fri May 01 2009 Funda Wang <fwang@mandriva.org> 2.0.4-1mdv2010.0
+ Revision: 369880
- new version 2.0.4

* Sat Mar 28 2009 Gustavo De Nardin <gustavodn@mandriva.com> 2.0.3-2mdv2009.1
+ Revision: 361845
- rebuild for xulrunner 1.9.0.8

* Sat Mar 14 2009 Frederik Himpe <fhimpe@mandriva.org> 2.0.3-1mdv2009.1
+ Revision: 354855
- update to new version 2.0.3

* Thu Mar 12 2009 Götz Waschk <waschk@mandriva.org> 2.0.2-2mdv2009.1
+ Revision: 354134
- rebuild for new xulrunner

* Tue Mar 10 2009 Götz Waschk <waschk@mandriva.org> 2.0.2-1mdv2009.1
+ Revision: 353382
- new version
- update file list

* Tue Mar 10 2009 Götz Waschk <waschk@mandriva.org> 2.0.1-2mdv2009.1
+ Revision: 353374
- rebuild

* Thu Feb 12 2009 Frederik Himpe <fhimpe@mandriva.org> 2.0.1-1mdv2009.1
+ Revision: 339897
- update to new version 2.0.1

  + Götz Waschk <waschk@mandriva.org>
    - use bundled libtorrent on 2008.1

* Wed Feb 11 2009 Götz Waschk <waschk@mandriva.org> 2.0-1mdv2009.1
+ Revision: 339378
- new version
- drop patches 0,1,5,6,7,8
- rediff patch 4
- fix installation
- update file list

* Tue Feb 03 2009 Funda Wang <fwang@mandriva.org> 1.2.8-9mdv2009.1
+ Revision: 337068
- rebuild for new xulrunner

* Sat Dec 27 2008 Adam Williamson <awilliamson@mandriva.org> 1.2.8-8mdv2009.1
+ Revision: 319598
- rebuild with python 2.6

* Wed Dec 24 2008 Funda Wang <fwang@mandriva.org> 1.2.8-6mdv2009.1
+ Revision: 318247
- rebuild for new xulrunner

* Sun Dec 21 2008 Funda Wang <fwang@mandriva.org> 1.2.8-5mdv2009.1
+ Revision: 316920
- rebuild for new boost

  + Adam Williamson <awilliamson@mandriva.org>
    - drop boost requirements and boost patch: boost was only used for libtorrent
      and we're on system libtorrent now

* Tue Dec 16 2008 Adam Williamson <awilliamson@mandriva.org> 1.2.8-3mdv2009.1
+ Revision: 314964
- adjust buildrequires and requires to use system libtorrent
- add libtorrent14.patch: from upstream SVN, work with libtorrent 0.14+
- add system_libtorrent.patch: from upstream SVN, check for and use system
  libtorrent(-rasterbar) if present
- add disable_heart.patch: disables iheartmiro as it causes miro to hang at
  start if not already configured
- rediff work-around-python-problem.patch for fuzz=0

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Fri Nov 14 2008 Götz Waschk <waschk@mandriva.org> 1.2.8-2mdv2009.1
+ Revision: 303096
- rebuild for new xulrunner

* Sun Oct 26 2008 Funda Wang <fwang@mandriva.org> 1.2.8-1mdv2009.1
+ Revision: 297423
- New version 1.2.8
- rebuild for new xulrunner

* Mon Sep 29 2008 Götz Waschk <waschk@mandriva.org> 1.2.7-3mdv2009.0
+ Revision: 289234
- rebuild for new xulrunner

* Fri Sep 26 2008 Tiago Salem <salem@mandriva.com.br> 1.2.7-2mdv2009.0
+ Revision: 288700
- rebuild for the new xulrunner

* Fri Sep 26 2008 Götz Waschk <waschk@mandriva.org> 1.2.7-1mdv2009.0
+ Revision: 288629
- fix build with new boost
- fix xcb build deps

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - rebuild against new boost

  + Frederik Himpe <fhimpe@mandriva.org>
    - Update to new version 1.2.6

* Wed Jul 30 2008 Götz Waschk <waschk@mandriva.org> 1.2.4-5mdv2009.0
+ Revision: 255044
- build with xulrunner

* Wed Jul 16 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.4-4mdv2009.0
+ Revision: 236422
- rebuilt for mozilla-firefox-2.0.0.16

* Wed Jul 09 2008 Götz Waschk <waschk@mandriva.org> 1.2.4-3mdv2009.0
+ Revision: 232950
+ rebuild (emptylog)

* Thu Jul 03 2008 Tiago Salem <salem@mandriva.com.br> 1.2.4-2mdv2009.0
+ Revision: 231253
- Rebuild for firefox 2.0.0.15

  + Funda Wang <fwang@mandriva.org>
    - Add patch to build against gcc4.3
    - New version 1.2.4

* Wed Apr 23 2008 Frederik Himpe <fhimpe@mandriva.org> 1.2.3-1mdv2009.0
+ Revision: 196969
- New upstream version
- Fix path of xinerenderer.py for substitution of libxecdir

* Mon Mar 31 2008 Adam Williamson <awilliamson@mandriva.org> 1.2.1-1mdv2008.1
+ Revision: 191277
- include a 48x48 icon, this is required by fd.o spec
- rediff no-autoupdate.patch
- use new-style macros consistently
- new release 1.2.1

* Wed Mar 26 2008 Tiago Salem <salem@mandriva.com.br> 1.1.2-2mdv2008.1
+ Revision: 190336
- Rebuild for Firefox 2.0.0.13

* Wed Feb 13 2008 Götz Waschk <waschk@mandriva.org> 1.1.2-1mdv2008.1
+ Revision: 166941
- new version

* Sat Feb 09 2008 Funda Wang <fwang@mandriva.org> 1.1-2mdv2008.1
+ Revision: 164644
- rebuild for new FF

* Fri Jan 11 2008 Götz Waschk <waschk@mandriva.org> 1.1-1mdv2008.1
+ Revision: 147896
- fix buildrequires
- new version
- depend on gstreamer

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Dec 12 2007 Götz Waschk <waschk@mandriva.org> 1.0-2mdv2008.1
+ Revision: 117691
- rebuild for new firefox

* Wed Nov 14 2007 Götz Waschk <waschk@mandriva.org> 1.0-1mdv2008.1
+ Revision: 108820
- new version

* Mon Nov 05 2007 Götz Waschk <waschk@mandriva.org> 0.9.9.9-3mdv2008.1
+ Revision: 106070
- rebuild for new firefox

* Fri Nov 02 2007 Götz Waschk <waschk@mandriva.org> 0.9.9.9-2mdv2008.1
+ Revision: 105177
- drop patch 0 and build with new boost

* Thu Nov 01 2007 Götz Waschk <waschk@mandriva.org> 0.9.9.9-1mdv2008.1
+ Revision: 104454
- new version
- rediff patches 1,4
- drop patch 2
- fix installation of xine_extractor
- update file list

* Sun Oct 21 2007 Götz Waschk <waschk@mandriva.org> 0.9.9.1-3mdv2008.1
+ Revision: 100867
- build against boost_python-gcc42

* Fri Oct 19 2007 Götz Waschk <waschk@mandriva.org> 0.9.9.1-2mdv2008.1
+ Revision: 100434
- rebuild for new firefox

* Fri Sep 07 2007 Götz Waschk <waschk@mandriva.org> 0.9.9.1-1mdv2008.1
+ Revision: 81464
- update patch 2

* Fri Sep 07 2007 Götz Waschk <waschk@mandriva.org> 0.9.9.1-1mdv2008.0
+ Revision: 81452
- new version

* Wed Sep 05 2007 Götz Waschk <waschk@mandriva.org> 0.9.9-2mdv2008.0
+ Revision: 80323
- drop patch 3, fixes bug #33185

* Wed Sep 05 2007 Götz Waschk <waschk@mandriva.org> 0.9.9-1mdv2008.0
+ Revision: 79986
- reenable patch 3
- patch to fix build system problem with python

  + Funda Wang <fwang@mandriva.org>
    - BR libxv
    - Rediff dbus patch
    - rediff no autoupdate patch
    - New version 0.9.9

* Wed Sep 05 2007 Adam Williamson <awilliamson@mandriva.org> 0.9.8.1-2mdv2008.0
+ Revision: 79656
- have to keep the icons in /usr/share/pixmaps as the app uses them directly
- fix double quote mark
- fd.o icons
- drop creation of miro.real as this seems to be done upstream now, so duplicating it was preventing the app from running (see http://forum.mandriva.com/viewtopic.php?p=365287)
- fix menu entry issues: categories, deprecated key, icon name
- use Fedora license policy
- spec clean

  + Götz Waschk <waschk@mandriva.org>
    - remove mdk-folders patch

* Thu Aug 02 2007 Götz Waschk <waschk@mandriva.org> 0.9.8.1-1mdv2008.0
+ Revision: 58199
- new version

* Tue Jul 31 2007 Götz Waschk <waschk@mandriva.org> 0.9.8-5mdv2008.0
+ Revision: 57234
- rebuild

* Thu Jul 19 2007 Götz Waschk <waschk@mandriva.org> 0.9.8-4mdv2008.0
+ Revision: 53539
- add missing deps
- readd wrapper, it ist still needed

* Thu Jul 19 2007 Götz Waschk <waschk@mandriva.org> 0.9.8-3mdv2008.0
+ Revision: 53509
- fix dbus exception on startup

* Thu Jul 19 2007 Götz Waschk <waschk@mandriva.org> 0.9.8-2mdv2008.0
+ Revision: 53446
- fix mime package
- remove wrapper script

* Wed Jul 18 2007 Götz Waschk <waschk@mandriva.org> 0.9.8-1mdv2008.0
+ Revision: 53269
- new version
- rediff patch 0
- import democracy as miro

* Fri Jun 15 2007 Götz Waschk <waschk@mandriva.org> 0.9.6-3mdv2008.0
+ Revision: 39941
- rebuild for new ff

  + Anssi Hannula <anssi@mandriva.org>
    - rebuild with correct optflags

  + Frederic Crozat <fcrozat@mandriva.com>
    - Release 0.9.6
    - Remove patches 2, 3, 4 (merged upstream)

* Wed Apr 25 2007 Götz Waschk <waschk@mandriva.org> 0.9.5.3-1mdv2008.0
+ Revision: 18190
- Import democracy

