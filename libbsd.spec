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
Version:	0.11.8
Release:	1
License:	BSD and ISC and Copyright only and Public Domain
Group:		System/Libraries
Url:		http://libbsd.freedesktop.org/
Source0:	http://libbsd.freedesktop.org/releases/libbsd-%{version}.tar.xz
BuildRequires:	pkgconfig(libmd)
%if %{with compat32}
BuildRequires:	devel(libmd)
%endif

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

%prep
%autosetup -p1

export CONFIGURE_TOP=$(pwd)
%if %{with compat32}
mkdir build32
cd build32
%configure32
cd ..
%endif

mkdir build
cd build
%configure

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
rm -f %{buildroot}%{_prefix}/lib/*.a
%endif
%make_install -C build

# (tpg) strip LTO from "LLVM IR bitcode" files
check_convert_bitcode() {
    printf '%s\n' "Checking for LLVM IR bitcode"
    llvm_file_name=$(realpath ${1})
    llvm_file_type=$(file ${llvm_file_name})

    if printf '%s\n' "${llvm_file_type}" | grep -q "LLVM IR bitcode"; then
# recompile without LTO
    clang %{optflags} -fno-lto -Wno-unused-command-line-argument -x ir ${llvm_file_name} -c -o ${llvm_file_name}
    elif printf '%s\n' "${llvm_file_type}" | grep -q "current ar archive"; then
    printf '%s\n' "Unpacking ar archive ${llvm_file_name} to check for LLVM bitcode components."
# create archive stage for objects
    archive_stage=$(mktemp -d)
    archive=${llvm_file_name}
    cd ${archive_stage}
    ar x ${archive}
    for archived_file in $(find -not -type d); do
        check_convert_bitcode ${archived_file}
        printf '%s\n' "Repacking ${archived_file} into ${archive}."
        ar r ${archive} ${archived_file}
    done
    ranlib ${archive}
    cd ..
    fi
}

for i in $(find %{buildroot} -type f -name "*.[ao]"); do
    check_convert_bitcode ${i}
done

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
%{_prefix}/lib/pkgconfig/*.pc
%endif
