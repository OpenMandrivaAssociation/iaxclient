%define	snap	0
%define beta	3
%define rel	1

%if %beta
%define release		%mkrel 0.beta%{beta}.%{rel}
%define distname	%{name}-%{version}beta%{beta}.tar.gz
%define dirname		%{name}-%{version}beta%{beta}
%else
%define release		%mkrel %{rel}
%define distname	%{name}-%{version}.tar.gz
%define dirname		%{name}-%{version}
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
BuildRequires:	imagemagick
BuildRequires:	gd-devel
BuildRequires:	gsm-devel >= 1.0.10-8mdk
BuildRequires:	iax-devel >= 0.2.3-6mdk
BuildRequires:	libilbc-devel
BuildRequires:	libspeex-devel >= 1.1.6-1mdk
BuildRequires:	portaudio-devel >= 18.1-1mdk
BuildRequires:	portmixer-devel >= 18.1-1mdk
BuildRequires:	libwxgtk-devel
BuildRequires:	x11-server-xvfb
BuildRequires:	liboggz-devel
BuildRequires:	libvidcap-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Although asterisk supports other IP protocols (including SIP, and
with patches, H.323), IAX's simple, lightweight nature gives it
several advantages, particularly in that it can operate easily
through NAT and packet firewalls, and it is easily extensible and
simple to understand. 

%package -n	%{libname}
Summary:	Library to implement the IAX protocol
Group:          System/Libraries

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
Group:          Communications

%description	utils
IAX utilities:

 o iax2slin - Originate an IAX2 call, and send the audio from this
   call to stdout
 o testcall, testcall-jb: make a single test call with IAXCLIENT.
   IAX Support for talking to Asterisk and other Gnophone clients

%package -n	tkiaxphone
Summary:	Simple IAX phone client
Group:          Communications
Requires:	tk

%description -n	tkiaxphone
Simple IAX phone client

EXPERIMENTAL

%package -n	iaxcomm
Summary:	IaxComm, a portable IAX2 protocol telephony client
Group:          Communications
URL:		http://iaxclient.sourceforge.net/iaxcomm/
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description -n	iaxcomm
iaxComm is an Open Source softphone for the Asterisk PBX.

EXPERIMENTAL

%prep

%setup -q -n %{dirname}
%patch0 -p1 -b .headers
%patch1 -p1 -b .ffmpeg
%patch2 -p1 -b .literal
%patch3 -p1 -b .tkphone
%patch4 -p1

%build
autoreconf
export RPM_OPT_FLAGS="%{optflags} -fPIC"
%configure2_5x --with-gsm-includes=%{_includedir}/gsm \
		--with-wx-config=%{_bindir}/wx-config-ansi \
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

%if %mdkversion < 200900
%post -n iaxcomm
%update_menus
%update_desktop_database
%endif

%if %mdkversion < 200900
%postun -n iaxcomm
%clean_menus
%clean_desktop_database
%endif

%if %mdkversion < 200900
%post -n tkiaxphone
%update_menus
%update_desktop_database
%endif

%if %mdkversion < 200900
%postun -n tkiaxphone
%clean_menus
%clean_desktop_database
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

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
