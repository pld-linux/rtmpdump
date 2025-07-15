#
# Conditional build:
%bcond_without	gnutls		# GNU TLS instead of OpenSSL (use same as curl)
#
Summary:	A utility for getting files from RTMP servers
Summary(pl.UTF-8):	Narzędzie do pobierania plików z sewerów RTMP
Name:		rtmpdump
Version:	2.6
%define	gitref	6f6bb1353fc84f4cc37138baa99f586750028a01
%define	snap	20240302
%define	rel	1
Release:	1.%{snap}.%{rel}
License:	GPL v2
Group:		Applications/Networking
#Source0:	http://rtmpdump.mplayerhq.hu/download/%{name}-%{version}.tgz
#Source0:	https://git.ffmpeg.org/gitweb/rtmpdump.git/snapshot/%{gitref}.tar.gz#/%{name}-%{smap}.tar.gz
# snapshots no longer allowed, use just git archive
Source0:	%{name}-%{snap}.tar.gz
# Source0-md5:	58095263a0dff40d8dcc374d8a15d6d7
Patch0:		%{name}-libtool.patch
URL:		http://rtmpdump.mplayerhq.hu/
%if %{with gnutls}
# nettle based
BuildRequires:	gnutls-devel >= 2.12
%else
BuildRequires:	openssl-devel >= 0.9.8
%endif
BuildRequires:	libtool
BuildRequires:	zlib-devel
Requires:	librtmp = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rtmpdump is a toolkit for RTMP streams. All forms of RTMP are
supported, including rtmp://, rtmpt://, rtmpe://, rtmpte:// and
rtmps://.

%description -l pl.UTF-8
rtmpdump to zestaw narzędzi do strumieni RTMP. Obsługiwane są
wszystkie postaci RTMP, w tym rtmp://, rtmpt://, rtmpe://, rtmpte://
oraz rtmps://.

%package -n librtmp
Summary:	RTMP library - RTMPDump Real-Time Messaging Protocol API
Summary(pl.UTF-8):	Biblioteka RTMP - API do obsługi protokołu Real-Time Messaging Protocol
License:	LGPL v2.1+
Group:		Libraries

%description -n librtmp
RTMP library - RTMPDump Real-Time Messaging Protocol API.

%description -n librtmp -l pl.UTF-8
Biblioteka RTMP - API do obsługi protokołu RTMP (Real-Time Messaging
Protocol).

%package -n librtmp-devel
Summary:	Header files for RTMP library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki RTMP
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	librtmp = %{version}-%{release}
%if %{with gnutls}
Requires:	gnutls-devel >= 2.12
%else
Requires:	openssl-devel >= 0.9.8
%endif
Requires:	zlib-devel

%description -n librtmp-devel
Header files for RTMP library.

%description -n librtmp-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki RTMP.

%package -n librtmp-static
Summary:	Static version of RTMP library
Summary(pl.UTF-8):	Statyczna wersja biblioteki RTMP
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	librtmp-devel = %{version}-%{release}

%description -n librtmp-static
Static version of RTMP library.

%description -n librtmp-static -l pl.UTF-8
Statyczna wersja biblioteki RTMP.

%prep
%setup -q -n %{name}-%{snap}
%patch -P0 -p1

%build
%{__make} \
	CRYPTO=%{?with_gnutls:GNUTLS}%{!?with_gnutls:OPENSSL} \
	libdir=%{_libdir} \
	CC="%{__cc}" \
	OPT="%{rpmcppflags} %{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{_libdir} \
	mandir=%{_mandir} \
	prefix=%{_prefix}

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/librtmp.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n librtmp -p /sbin/ldconfig
%postun -n librtmp -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/rtmpdump
%attr(755,root,root) %{_sbindir}/rtmpgw
%attr(755,root,root) %{_sbindir}/rtmpsrv
%attr(755,root,root) %{_sbindir}/rtmpsuck
%{_mandir}/man1/rtmpdump.1*
%{_mandir}/man8/rtmpgw.8*

%files -n librtmp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librtmp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librtmp.so.1

%files -n librtmp-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librtmp.so
%{_includedir}/librtmp
%{_pkgconfigdir}/librtmp.pc
%{_mandir}/man3/librtmp.3*

%files -n librtmp-static
%defattr(644,root,root,755)
%{_libdir}/librtmp.a
