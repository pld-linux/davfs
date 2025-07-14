#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
#
%define		_rel	1

Summary:	Web-based Distributed Authoring and Versioning
Summary(pl.UTF-8):	Bazujące na WWW Rozproszone Autoryzowanie i Wersjonowanie
Name:		davfs
Version:	0.2.4
Release:	%{_rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/dav/%{name}-%{version}.tar.gz
# Source0-md5:	705a99583a118ef3325551d700e49caa
Patch0:		%{name}-path.patch
Patch1:		%{name}-is_socket_ready.patch
URL:		http://dav.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	autoconf
BuildRequires:	%{kgcc_package}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WebDAV is an acronym for Web-based Distributed Authoring and Version-
ing. Usually HTTP is a read only protocol, but if you install DAV on
your web server, it becomes writable. Furthermore, if you use DAVfs,
you can mount your web server onto your filesystem and can use it as a
normal disk.

%description -l pl.UTF-8
WebDAV to bazujące na WWW Rozproszone Autoryzowanie i Wersjonowanie.
Zazwyczaj protokół HTTP jest protokołem tylko do odczytu ale po
zainstalowaniu DAVa staje się on również zapisywalnym. Co więcej jeśli
używasz DAVfs to możesz montować swój serwer WWW jako system plików i
używać tak jak normalnego dysku.

%package -n kernel-fs-davfs
Summary:	DAVfs - Drivers
Summary(pl.UTF-8):	DAVfs - Sterowniki
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-fs-davfs
WebDAV is an acronym for Web-based Distributed Authoring and Version-
ing. Usually HTTP is a read only protocol, but if you install DAV on
your web server, it becomes writable. Furthermore, if you use DAVfs,
you can mount your web server onto your filesystem and can use it as a
normal disk.

%description -n kernel-fs-davfs -l pl.UTF-8
WebDAV to bazujące na WWW Rozproszone Autoryzowanie i Wersjonowanie.
Zazwyczaj protokół HTTP jest protokołem tylko do odczytu ale po
zainstalowaniu DAVa staje się on również zapisywalnym. Co więcej jeśli
używasz DAVfs to możesz montować swój serwer WWW jako system plików i
używać tak jak normalnego dysku.

%package -n kernel-smp-fs-davfs
Summary:	DAVfs - SMP Drivers
Summary(pl.UTF-8):	DAVfs - Sterowniki SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-fs-davfs
WebDAV is an acronym for Web-based Distributed Authoring and Version-
ing. Usually HTTP is a read only protocol, but if you install DAV on
your web server, it becomes writable. Furthermore, if you use DAVfs,
you can mount your web server onto your filesystem and can use it as a
normal disk.

%description -n kernel-smp-fs-davfs -l pl.UTF-8
WebDAV to bazujące na WWW Rozproszone Autoryzowanie i Wersjonowanie.
Zazwyczaj protokół HTTP jest protokołem tylko do odczytu ale po
zainstalowaniu DAVa staje się on również zapisywalnym. Co więcej jeśli
używasz DAVfs to możesz montować swój serwer WWW jako system plików i
używać tak jak normalnego dysku.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%configure2_13 \
	--with-ssl \
	--with-kernel=%{_kernelsrcdir}
%{__make}

%{__make} -C davfs clean all \
	CC=%{kgcc} \
	CFLAGS="-O2 -D__KERNEL__ -DMODULE -D__SMP__ -DCONFIG_X86_LOCAL_APIC \
	-I%{_kernelsrcdir}/include -Wall -Wstrict-prototypes -fomit-frame-pointer \
	-fno-strict-aliasing -pipe -fno-strength-reduce"
mv -f davfs/davfs.o davfs-smp.o

%{__make} -C davfs clean all \
	CC=%{kgcc} \
	CFLAGS="-O2 -D__KERNEL__ -DMODULE \
	-I%{_kernelsrcdir}/include -Wall -Wstrict-prototypes -fomit-frame-pointer \
	-fno-strict-aliasing -pipe -fno-strength-reduce"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,/etc/rc.d/init.d}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc

echo "all install:" > davfs/Makefile

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install davfs/davfs.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/davfs.o
install davfs-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/davfs.o
ln -sf %{_sbindir}/mount.davfs $RPM_BUILD_ROOT/sbin/mount.davfs

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-fs-davfs
%depmod %{_kernel_ver}

%postun -n kernel-fs-davfs
%depmod %{_kernel_ver}

%post -n kernel-smp-fs-davfs
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-fs-davfs
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc ChangeLog doc/*.html
%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_sbindir}/*

%files -n kernel-fs-davfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.o*

%files -n kernel-smp-fs-davfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*.o*
