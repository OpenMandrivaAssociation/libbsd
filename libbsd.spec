%define name	%mklibname bsd
%define devel	%mklibname -d bsd

Name:		%name
Version:	0.3.0
Release:	%mkrel 1
Summary:	Library providing BSD-compatible functions for portability
URL:		http://libbsd.freedesktop.org/

Source0:	http://libbsd.freedesktop.org/releases/libbsd-%{version}.tar.gz

License:	BSD and ISC and Copyright only and Public Domain
Group:		System Environment/Libraries

%description
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

%package -n %devel
Summary:	Development files for libbsd
Group:		Development/Libraries
Requires:	%name = %{version}-%{release}
Requires:	pkgconfig
Provides:	libbsd-devel = %{version}-%{release}

%description -n %devel
Development files for the libbsd library.

%prep
%setup -q -n libbsd-%version

# fix encoding of flopen.3 man page
for f in src/flopen.3; do
  iconv -f iso8859-1 -t utf-8 $f >$f.conv
  touch -r $f $f.conv
  mv $f.conv $f
done

%build
make CFLAGS="%{optflags}" %{?_smp_mflags} \
     libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix}

%install
make libdir=%{_libdir} \
     usrlibdir=%{_libdir} \
     exec_prefix=%{_prefix} \
     DESTDIR=%{buildroot} \
     install

# don't want static library
rm %{buildroot}%{_libdir}/libbsd.a

# Move nlist.h into bsd directory to avoid conflict with elfutils-libelf.
mv %{buildroot}%{_includedir}/nlist.h %{buildroot}%{_includedir}/bsd/

%files
%doc COPYING README TODO ChangeLog
%{_libdir}/libbsd.so.*

%files -n %devel
%{_mandir}/man3/*.3.?z
%{_mandir}/man3/*.3bsd.?z
%{_includedir}/*.h
%{_includedir}/bsd
%{_libdir}/libbsd.so
%{_libdir}/pkgconfig/libbsd.pc
%{_libdir}/pkgconfig/libbsd-overlay.pc
