#
%bcond_without	gnutls		# build with GNU TLS instead of OpenSSL (use same as curl)
#
Summary:	A utility for getting files from RTMP servers
Name:		rtmpdump
Version:	2.3
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://rtmpdump.mplayerhq.hu/download/%{name}-%{version}.tgz
# Source0-md5:	eb961f31cd55f0acf5aad1a7b900ef59
Patch0:		%{name}-libtool.patch
URL:		http://rtmpdump.mplayerhq.hu/
%if %{with gnutls}
BuildRequires:	gnutls-devel
%else
BuildRequires:	openssl-devel
%endif
BuildRequires:	libtool
BuildRequires:	zlib-devel
Requires:	librtmp = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rtmpdump is a toolkit for RTMP streams. All forms of RTMP are
supported, including rtmp://, rtmpt://, rtmpe://, rtmpte:// and
rtmps://.

%package -n librtmp
Summary:	rtmp library
Group:		Libraries

%description -n librtmp
rtmp library.

%package -n librtmp-devel
Summary:	Header files and development documentation for rtmp library
Group:		Development/Libraries
Requires:	librtmp = %{version}-%{release}
Requires:	openssl-devel
Requires:	zlib-devel

%description -n librtmp-devel
Header files and development documentation for rtmp library.

%package -n librtmp-static
Summary:	Static version of rtmp library
Group:		Development/Libraries
Requires:	librtmp-devel = %{version}-%{release}

%description -n librtmp-static
Static version of rtmp library.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CRYPTO=%{?with_gnutls:GNUTLS}%{!?with_gnutls:OPENSSL} \
	libdir=%{_libdir} \
	CC="%{__cc}" \
	OPT="%{rpmcppflags} %{rpmcflags}" \
	XLDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{_libdir} \
	mandir=%{_mandir} \
	prefix=%{_prefix}

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
%attr(755,root,root) %ghost %{_libdir}/librtmp.so.0

%files -n librtmp-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librtmp.so
%{_libdir}/librtmp.la
%{_includedir}/librtmp
%{_pkgconfigdir}/librtmp.pc
%{_mandir}/man3/librtmp.3*

%files -n librtmp-static
%defattr(644,root,root,755)
%{_libdir}/librtmp.a
