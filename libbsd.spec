%define debug_package %nil
%define major 0
%define libname %mklibname bsd %{major}
%define devname %mklibname -d bsd

Summary:	Library providing BSD-compatible functions for portability
Name:		libbsd
Version:	0.10.0
Release:	1
License:	BSD and ISC and Copyright only and Public Domain
Group:		System/Libraries
Url:		http://libbsd.freedesktop.org/
Source0:	http://libbsd.freedesktop.org/releases/libbsd-%{version}.tar.xz

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
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}bsd0-devel < 0.4.1-2

%description -n %{devname}
Development files for the libbsd library.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install

%files -n %{libname}
%{_libdir}/libbsd.so.%{major}*

%files -n %{devname}
%doc COPYING README TODO ChangeLog
%{_mandir}/man3/*
%{_mandir}/man7/*
%{_includedir}/bsd
%{_libdir}/libbsd.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libbsd-ctor.a
