%define	snap 20060610

%define	major 0
%define libname	%mklibname iaxclient %{major}

Summary:	Library to implement the IAX protocol
Name:		iaxclient
Version:	1.0
Release:	%mkrel 0.%{snap}.3
License:	LGPL
Group:		System/Libraries
URL:            http://iaxclient.sourceforge.net/
Source0:        %{name}-%{version}-%{snap}.tar.bz2
Patch0:		iaxclient-1.0-20050410-headers.diff.bz2
#Patch1:		iaxclient-1.0-20050410-mdk.diff.bz2
Patch1:		iaxclient-1.0-20060610-mdk.diff
#Patch2:		iaxclient-1.0-20050410-progs.diff.bz2
Patch2:		iaxclient-1.0-20060610-progs.diff
BuildRequires:	ImageMagick
BuildRequires:	gd-devel
BuildRequires:	gsm-devel >= 1.0.10-8mdk
BuildRequires:	iax-devel >= 0.2.3-6mdk
BuildRequires:	libilbc-devel
BuildRequires:	libspeex-devel >= 1.1.6-1mdk
BuildRequires:	portaudio-devel >= 18.1-1mdk
BuildRequires:	portmixer-devel >= 18.1-1mdk
BuildRequires:	wxGTK2.6-devel
BuildRequires:	x11-server-xvfb
BuildConflicts:	%{name}-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Although asterisk supports other IP protocols (including SIP, and
with patches, H.323), IAX's simple, lightweight nature gives it
several advantages, particularly in that it can operate easily
through NAT and packet firewalls, and it is easily extensible and
simple to understand. 

Note: the 1.0 version does not exist yet, this source is taken
from CVS and no versioning info could be found.

%package -n	%{libname}
Summary:	Library to implement the IAX protocol
Group:          System/Libraries

%description -n	%{libname}
Although asterisk supports other IP protocols (including SIP, and
with patches, H.323), IAX's simple, lightweight nature gives it
several advantages, particularly in that it can operate easily
through NAT and packet firewalls, and it is easily extensible and
simple to understand. 

Note: the 1.0 version does not exist yet, this source is taken
from CVS and no versioning info could be found.

%package -n	%{libname}-devel
Summary:	IAXClient Library development files
Group:		Development/C
Obsoletes:	%{name}-devel lib%{name}-devel
Provides:	%{name}-devel lib%{name}-devel
Requires:	%{libname} = %{version}-%{release}

%description -n	%{libname}-devel
Although asterisk supports other IP protocols (including SIP, and
with patches, H.323), IAX's simple, lightweight nature gives it
several advantages, particularly in that it can operate easily
through NAT and packet firewalls, and it is easily extensible and
simple to understand. 

This package contains the development library and its header
files for the IAXClient Library.

Note: the 1.0 version does not exist yet, this source is taken
from CVS and no versioning info could be found.

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

%setup -q -n %{name}
%patch0 -p1 -b .headers
%patch1 -p1 -b .mdk
%patch2 -p1 -b .progs

%build

%make -C lib RPM_OPT_FLAGS="%{optflags} -fPIC"
ln -snf libiaxclient.so.%{major}.%{version} lib/libiaxclient.so.%{major}
ln -snf libiaxclient.so.%{major}.%{version} lib/libiaxclient.so

%make -C simpleclient/iax2slin RPM_OPT_FLAGS="%{optflags} -fPIC"
%make -C simpleclient/testcall RPM_OPT_FLAGS="%{optflags} -fPIC"

# these are gui's, should be broken out later on

# for some reason wxcs needs X
#XDISPLAY=$(i=2; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
#Xvfb :$XDISPLAY >& /dev/null &
#export DISPLAY=:$XDISPLAY
#DISPLAY=:$XDISPLAY %make -C simpleclient/iaxcomm RPM_OPT_FLAGS="%{optflags} -fPIC"
#kill $(cat /tmp/.X$XDISPLAY-lock)

%make -C simpleclient/iaxcomm RPM_OPT_FLAGS="%{optflags} -fPIC"

%make -C simpleclient/tkphone RPM_OPT_FLAGS="%{optflags} -fPIC"

# iaxphone and wx won't compile ;(
#%make -C simpleclient/iaxphone RPM_OPT_FLAGS="%{optflags} -fPIC"
#%make -C simpleclient/wx RPM_OPT_FLAGS="%{optflags} -fPIC"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_includedir}/iaxclient/spandsp
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}

# install the shared lib
install -m0755 lib/libiaxclient.so.%{major}.%{version} %{buildroot}%{_libdir}/
ln -snf libiaxclient.so.%{major}.%{version} %{buildroot}%{_libdir}/libiaxclient.so.%{major}
ln -snf libiaxclient.so.%{major}.%{version} %{buildroot}%{_libdir}/libiaxclient.so

# install the static lib
install -m0644 lib/libiaxclient.a %{buildroot}%{_libdir}/

# install the headers
install -m0644 lib/audio_encode.h %{buildroot}%{_includedir}/iaxclient/
install -m0644 lib/audio_file.h %{buildroot}%{_includedir}/iaxclient/
install -m0644 lib/audio_portaudio.h %{buildroot}%{_includedir}/iaxclient/
install -m0644 lib/codec_alaw.h %{buildroot}%{_includedir}/iaxclient/
install -m0644 lib/codec_gsm.h %{buildroot}%{_includedir}/iaxclient/
install -m0644 lib/codec_ilbc.h %{buildroot}%{_includedir}/iaxclient/
install -m0644 lib/codec_speex.h %{buildroot}%{_includedir}/iaxclient/
install -m0644 lib/codec_ulaw.h %{buildroot}%{_includedir}/iaxclient/
install -m0644 lib/iaxclient.h %{buildroot}%{_includedir}/iaxclient/
install -m0644 lib/iaxclient_lib.h %{buildroot}%{_includedir}/iaxclient/
install -m0644 lib/jitterbuf.h %{buildroot}%{_includedir}/iaxclient/
install -m0644 lib/spandsp/plc.h %{buildroot}%{_includedir}/iaxclient/spandsp/

# install the binaries
install -m0755 simpleclient/iax2slin/iax2slin %{buildroot}%{_bindir}/
install -m0755 simpleclient/testcall/testcall %{buildroot}%{_bindir}/
install -m0755 simpleclient/testcall/testcall-jb %{buildroot}%{_bindir}/

# these are gui's, should be broken out later on
install -m0755 simpleclient/iaxcomm/iaxcomm %{buildroot}%{_bindir}/
install -m0755 simpleclient/tkphone/iaxcli %{buildroot}%{_bindir}/
install -m0755 simpleclient/tkphone/monitor.ui.tcl %{buildroot}%{_bindir}/
install -m0755 simpleclient/tkphone/phone.ui.tcl %{buildroot}%{_bindir}/
install -m0755 simpleclient/tkphone/pref.ui.tcl %{buildroot}%{_bindir}/
install -m0755 simpleclient/tkphone/tkiaxphone %{buildroot}%{_bindir}/

# fix some menu entries and stuff...
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_liconsdir}

convert simpleclient/iaxcomm/rc/logo.xpm -geometry 48x48 %{buildroot}%{_liconsdir}/iaxcomm.png
convert simpleclient/iaxcomm/rc/logo.xpm -geometry 32x32 %{buildroot}%{_iconsdir}/iaxcomm.png
convert simpleclient/iaxcomm/rc/logo.xpm -geometry 16x16 %{buildroot}%{_miconsdir}/iaxcomm.png


# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=iaxComm
Comment=iaxComm, a portable IAX2 protocol telephony client
Exec=%{_bindir}/iaxcomm
Icon=iaxcomm
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet-VideoConference;Network;Telephony;
EOF


%post -n iaxcomm
%update_menus
%update_desktop_database

%postun -n iaxcomm
%clean_menus
%clean_desktop_database

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
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc lib/TODO
%{_includedir}/iaxclient
%{_libdir}/*.so
%{_libdir}/*.a

%files utils
%defattr(-,root,root)
%{_bindir}/iax2slin
%{_bindir}/testcall
%{_bindir}/testcall-jb

%files -n tkiaxphone
%defattr(-,root,root)
%doc simpleclient/tkphone/License simpleclient/tkphone/README
%{_bindir}/iaxcli
%{_bindir}/monitor.ui.tcl
%{_bindir}/phone.ui.tcl
%{_bindir}/pref.ui.tcl
%{_bindir}/tkiaxphone

%files -n iaxcomm
%defattr(-,root,root)
%doc simpleclient/iaxcomm/QUICKSTART simpleclient/iaxcomm/README
%{_bindir}/iaxcomm
%{_liconsdir}/iaxcomm.png
%{_iconsdir}/iaxcomm.png
%{_miconsdir}/iaxcomm.png
%{_datadir}/applications/*.desktop
