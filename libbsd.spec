%define name	%mklibname bsd
%define devel	%mklibname -d bsd

Name:		%name
Version:	0.4.1
Release:	1
Summary:	Library providing BSD-compatible functions for portability
URL:		http://libbsd.freedesktop.org/

Source0:	http://libbsd.freedesktop.org/releases/libbsd-%{version}.tar.gz

License:	BSD and ISC and Copyright only and Public Domain
Group:		System/Libraries

%description
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

%package -n %devel
Summary:	Development files for libbsd
Group:		Development/C
Requires:	%name = %{version}-%{release}
Requires:	pkgconfig
Provides:	libbsd-devel = %{version}-%{release}

%description -n %devel
Development files for the libbsd library.

%prep
%setup -q -n libbsd-%version

%build
%configure2_5x --disable-static
%make

%install
%makeinstall_std

%files
%doc COPYING README TODO ChangeLog
%{_libdir}/libbsd.so.*

%files -n %devel
%{_mandir}/man3/*.3.?z
%{_mandir}/man3/*.3bsd.?z
%{_includedir}/bsd
%{_libdir}/libbsd.so
%{_libdir}/pkgconfig/libbsd.pc
%{_libdir}/pkgconfig/libbsd-overlay.pc
