%define	snap	0
%define	beta	3
%define	rel	4

%if %beta
%define release		%mkrel 0.beta%{beta}.%{rel}
%define distname	%{name}-%{version}beta%{beta}.tar.gz
%define fname		%{name}-%{version}beta%{beta}
%else
%define release		%mkrel %{rel}
%define distname	%{name}-%{version}.tar.gz
%define fname		%{name}-%{version}
%endif

%define	major		1
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Summary:	Library to implement the IAX protocol
Name:		iaxclient
Version:	2.1
Release:	%{release}
License:	LGPLv2+
Group:		System/Libraries
URL:		http://iaxclient.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{distname}
Patch0:		iaxclient-1.0-20050410-headers.diff
# Fix header location and linkage for ffmpeg - AdamW 2008/12
Patch1:		iaxclient-2.1-ffmpeg.patch
# Fix some string literal errors - AdamW 2008/12
Patch2:		iaxclient-2.1-literal.patch
# From upstream SVN: make tkphone build - AdamW 2008/12
Patch3:		iaxclient-2.1-tkphone.patch
# Make the dumb thing run - AdamW 2008/12
Patch4:		iaxclient-2.1-tkiaxphone.patch
# Fedora patches
Patch100:	iaxclient-2.1beta3-wxGTK28.patch
Patch102:	iaxclient-2.1beta3-tcl-includedir.patch
Patch103:	iaxclient-2.1beta3-tcl-libdir.patch
Patch104:	iaxclient-2.1beta3-tcl-nodoc.patch
Patch105:	iaxclient-2.1beta3-theora-detection.patch

BuildRequires:	imagemagick
BuildRequires:	gd-devel
BuildRequires:	gsm-devel
BuildRequires:	iax-devel
BuildRequires:	libilbc-devel
BuildRequires:	pkgconfig(speex)
BuildRequires:	portaudio-devel
BuildRequires:	portmixer-devel
BuildRequires:	wxgtku-devel
BuildRequires:	x11-server-xvfb
BuildRequires:	liboggz-devel
BuildRequires:	libvidcap-devel
BuildRequires:	libtheora-devel

%description
Although asterisk supports other IP protocols (including SIP, and
with patches, H.323), IAX's simple, lightweight nature gives it
several advantages, particularly in that it can operate easily
through NAT and packet firewalls, and it is easily extensible and
simple to understand.

%package -n	%{libname}
Summary:	Library to implement the IAX protocol
Group:		System/Libraries

%description -n	%{libname}
Although asterisk supports other IP protocols (including SIP, and
with patches, H.323), IAX's simple, lightweight nature gives it
several advantages, particularly in that it can operate easily
through NAT and packet firewalls, and it is easily extensible and
simple to understand. 

%package -n	%{develname}
Summary:	IAXClient Library development files
Group:		Development/C
Obsoletes:	%{name}-devel < %{version}-%{release}
Obsoletes:	%{mklibname iaxclient 0 -d} < %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{develname}
Although asterisk supports other IP protocols (including SIP, and
with patches, H.323), IAX's simple, lightweight nature gives it
several advantages, particularly in that it can operate easily
through NAT and packet firewalls, and it is easily extensible and
simple to understand. 

This package contains the development library and its header
files for the IAXClient Library.

%package	utils
Summary:	IAX utilities
Group:		Communications

%description	utils
IAX utilities:

 o iax2slin - Originate an IAX2 call, and send the audio from this
   call to stdout
 o testcall, testcall-jb: make a single test call with IAXCLIENT.
   IAX Support for talking to Asterisk and other Gnophone clients

%package -n	tkiaxphone
Summary:	Simple IAX phone client
Group:		Communications
Requires:	tk

%description -n	tkiaxphone
Simple IAX phone client

EXPERIMENTAL

%package -n	iaxcomm
Summary:	IaxComm, a portable IAX2 protocol telephony client
Group:		Communications
URL:		http://iaxclient.sourceforge.net/iaxcomm/
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description -n	iaxcomm
iaxComm is an Open Source softphone for the Asterisk PBX.

EXPERIMENTAL

%prep

%setup -q -n %{fname}
%patch0 -p1 -b .headers
%patch1 -p1 -b .ffmpeg
%patch2 -p1 -b .literal
%patch3 -p1 -b .tkphone
%patch4 -p1

%patch100 -p1 -b .wxGTK28
%patch102 -p1 -b .includedir
%patch103 -p1 -b .libdir
%patch104 -p1 -b .nodoc
%patch105 -p1 -b .theoradetect

%build
autoreconf -fis
export RPM_OPT_FLAGS="%{optflags} -fPIC"
%configure2_5x --with-gsm-includes=%{_includedir}/gsm \
		--with-wx-config=%{_bindir}/wx-config-unicode \
		--enable-clients="iaxcomm stresstest testcall tkphone vtestcall"
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
%makeinstall_std

rm -f %{buildroot}%{_bindir}/tkiaxphone

cat > %{buildroot}%{_bindir}/tkiaxphone << EOF
#!/bin/sh
%{_libdir}/iaxclient/tkphone/tkiaxphone
EOF

ln -s %{_libdir}/iaxclient/tkphone/iaxcli %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert simpleclient/iaxcomm/rc/logo.xpm -geometry 48x48 %{buildroot}%{_iconsdir}/hicolor/48x48/apps/iaxcomm.png
convert simpleclient/iaxcomm/rc/logo.xpm -geometry 48x48 %{buildroot}%{_iconsdir}/hicolor/48x48/apps/tkiaxphone.png
convert simpleclient/iaxcomm/rc/logo.xpm -geometry 32x32 %{buildroot}%{_iconsdir}/hicolor/32x32/apps/iaxcomm.png
convert simpleclient/iaxcomm/rc/logo.xpm -geometry 32x32 %{buildroot}%{_iconsdir}/hicolor/32x32/apps/tkiaxphone.png
convert simpleclient/iaxcomm/rc/logo.xpm -geometry 16x16 %{buildroot}%{_iconsdir}/hicolor/16x16/apps/iaxcomm.png
convert simpleclient/iaxcomm/rc/logo.xpm -geometry 16x16 %{buildroot}%{_iconsdir}/hicolor/16x16/apps/tkiaxphone.png

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-iaxcomm.desktop << EOF
[Desktop Entry]
Name=iaxComm
Comment=Portable IAX2 protocol telephony client
Exec=%{_bindir}/iaxcomm
Icon=iaxcomm
Terminal=false
Type=Application
Categories=Network;Telephony;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-tkiaxphone.desktop << EOF
[Desktop Entry]
Name=TkIaxPhone
Comment=Simple IAX phone client
Exec=%{_bindir}/tkiaxphone
Icon=iaxcomm
Terminal=false
Type=Application
Categories=Network;Telephony;
EOF

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/iaxclient.h
%{_libdir}/pkgconfig/iaxclient.pc
%{_libdir}/*.so
%{_libdir}/*.*a

%files utils
%defattr(-,root,root)
%{_bindir}/stresstest
%{_bindir}/testcall
%{_bindir}/vtestcall

%files -n tkiaxphone
%defattr(-,root,root)
%doc simpleclient/tkphone/License simpleclient/tkphone/README
%{_libdir}/iaxclient
%attr(0755,root,root) %{_bindir}/tkiaxphone
%{_bindir}/iaxcli
%{_iconsdir}/hicolor/*/apps/tkiaxphone.png
%{_datadir}/applications/mandriva-tkiaxphone.desktop

%files -n iaxcomm
%defattr(-,root,root)
%doc simpleclient/iaxcomm/QUICKSTART simpleclient/iaxcomm/README
%{_bindir}/iaxcomm
%{_datadir}/iaxcomm
%{_iconsdir}/hicolor/*/apps/iaxcomm.png
%{_datadir}/applications/mandriva-iaxcomm.desktop


%changelog
* Wed Jan 18 2012 Andrey Bondrov <abondrov@mandriva.org> 2.1-0.beta3.4mdv2011.0
+ Revision: 762078
- Update ffmpeg patch to support ffmpeg 0.9
- Clean up BuildRequires (drop versions as they are too old anyway)
- Rebuild against utf8 version of wxGTK2.8, update patch 2

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 2.1-0.beta3.2mdv2010.1
+ Revision: 462638
- Rebuild for new liboggz2
- Fix build by forcing autoreconf run
- Add Fedora patches

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sun Dec 28 2008 Adam Williamson <awilliamson@mandriva.org> 2.1-0.beta3.1mdv2009.1
+ Revision: 320249
- buildrequires libtheora-devel
- adjust file lists
- protect major in file list
- new major 1
- add a menu entry for tkiaxphone
- fd.o icons
- make a little wrapper script to run tkiaxphone
- tweak the list of clients (windows one we obviously don't want, and the
  other disabled ones don't build)
- now has a proper autofoo build system: use it, and drop all the manual crap
- new devel policy
- drop now incorrect description notes
- br liboggz-devel and libvidcap-devel (new deps)
- adjust dependencies to build against wx 2.8 (non-unicode - code is not
  unicode-safe)
- drop old unnecessary patches
- add tkiaxphone.patch: make tkiaxphone actually work
- add tkphone.patch: from upstream SVN, make tkphone build
- add literal.patch: fix string literal errors
- add ffmpeg.patch: fix headers and linking for ffmpeg
- bunzip2 patch
- new license policy
- spec conditionals for beta build
- new release 2.1 beta 3

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - summary is not licence tag
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Pascal Terjan <pterjan@mandriva.org>
    - Import iaxclient



* Sun Sep 17 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.20060610.3mdv2007.0
- fix silly typo

* Sun Sep 17 2006 Oden Eriksson <oeriksson@mandriva.com> 1.0-0.20060610.2mdv2007.0
- fix xdg menu

* Sat Jun 10 2006 Stefan van der Eijk <stefan@eijk.nu> 1.0-0.20060610.1mdk
- new SVN snapshot 20060610 (revision 571)
- rediffed patch 1 & 2
- BuildRequires

* Mon Apr 11 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0-0.20050410.3mdk
- more header files fixes
- file pernission fixes

* Mon Apr 11 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0-0.20050410.2mdk
- added one forgotten header file

* Mon Apr 11 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0-0.20050410.1mdk
- new CVS snapshot 20050410
- added the utils, tkiaxphone and iaxcomm sub packages

* Mon Sep 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.0-0.20040912.1mdk
- initial mandrake package
