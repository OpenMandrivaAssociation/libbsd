# libbsd is required by libICE, which in turn is used by
# wine -- hence the need for a 32bit package

%define major 0
%define libname %mklibname bsd %{major}
%define devname %mklibname -d bsd
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
%if %{with compat32}
%define lib32name libbsd%{major}
%define dev32name libbsd-devel
%endif

Summary:	Library providing BSD-compatible functions for portability
Name:		libbsd
Version:	0.12.2
Release:	1
License:	BSD and ISC and Copyright only and Public Domain
Group:		System/Libraries
Url:		https://libbsd.freedesktop.org/
Source0:	http://libbsd.freedesktop.org/releases/libbsd-%{version}.tar.xz
BuildRequires:	pkgconfig(libmd)
%if %{with compat32}
BuildRequires:	devel(libmd)
%endif
BuildSystem:	autotools

%description
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

%package -n %{libname}
Summary:	Library providing BSD-compatible functions for portability
Group:		System/Libraries

%description -n %{libname}
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

%package -n %{devname}
Summary:	Development files for libbsd
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	pkgconfig(libmd)
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}bsd0-devel < 0.4.1-2

%description -n %{devname}
Development files for the libbsd library.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Library providing BSD-compatible functions for portability (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

%package -n %{dev32name}
Summary:	Development files for libbsd (32-bit)
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}
Requires:	devel(libmd)
Provides:	devel(libbsd) = %{version}-%{release}

%description -n %{dev32name}
Development files for the libbsd library.
%endif

%files -n %{libname}
%{_libdir}/libbsd.so.%{major}*

%files -n %{devname}
%doc COPYING README TODO ChangeLog
%doc %{_mandir}/man3/*
%doc %{_mandir}/man7/*
%{_includedir}/bsd
%{_libdir}/libbsd.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libbsd.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libbsd.so
%{_prefix}/lib/*.a
%{_prefix}/lib/pkgconfig/*.pc
%endif
