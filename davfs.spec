
# conditional build
# _without_dist_kernel          without kernel from distribution

%define		_rel	1

Summary:	Web-based Distributed Authoring and Versioning
Summary(pl):	Bazuj�ce na WWW Rozproszone Autoryzowanie i Wersjonowanie
Name:		davfs
Version:	0.2.4
Release:	%{_rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://prdownloads.sourceforge.net/dav/%{name}-%{version}.tar.gz
Patch0:		%{name}-path.patch
Patch1:		%{name}-is_socket_ready.patch
URL:		http://dav.sourceforge.net/
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	autoconf
BuildRequires:	%{kgcc_package}
BuildRequires:	openssl-devel >= 0.9.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
WebDAV is an acronym for Web-based Distributed Authoring and Version-
ing. Usually http is a read only protocol, but if you install DAV on
your web server, it becomes writable. Furthermore, if you use DAVfs,
you can mount your web server onto your filesystem and can use it as a
normal disk.

%description -l pl
WebDAV to bazuj�ce na WWW Rozproszone Autoryzowanie i Wersjonowanie.
Zazwyczaj protok� http jest protoko�em tylko do odczytu ale po
zainstalowaniu DAVa staje si� on r�wnie� zapisywalnym. Co wi�cej je�li
u�ywasz DAVfs to mo�esz montowa� sw�j serwer www jako system plik�w i
u�ywa� tak jak normalnego dysku.

%package -n kernel-fs-davfs
Summary:	DAVfs - Drivers
Summary(pl):	DAVfs - Sterowniki
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}

%description -n kernel-fs-davfs
WebDAV is an acronym for Web-based Distributed Authoring and Version-
ing. Usually http is a read only protocol, but if you install DAV on
your web server, it becomes writable. Furthermore, if you use DAVfs,
you can mount your web server onto your filesystem and can use it as a
normal disk.

%description -n kernel-fs-davfs -l pl
WebDAV to bazuj�ce na WWW Rozproszone Autoryzowanie i Wersjonowanie.
Zazwyczaj protok� http jest protoko�em tylko do odczytu ale po
zainstalowaniu DAVa staje si� on r�wnie� zapisywalnym. Co wi�cej je�li
u�ywasz DAVfs to mo�esz montowa� sw�j serwer www jako system plik�w i
u�ywa� tak jak normalnego dysku.

%package -n kernel-smp-fs-davfs
Summary:	DAVfs - SMP Drivers
Summary(pl):	DAVfs - Sterowniki SMP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}

%description -n kernel-smp-fs-davfs
WebDAV is an acronym for Web-based Distributed Authoring and Version-
ing. Usually http is a read only protocol, but if you install DAV on
your web server, it becomes writable. Furthermore, if you use DAVfs,
you can mount your web server onto your filesystem and can use it as a
normal disk.

%description -n kernel-smp-fs-davfs -l pl
WebDAV to bazuj�ce na WWW Rozproszone Autoryzowanie i Wersjonowanie.
Zazwyczaj protok� http jest protoko�em tylko do odczytu ale po
zainstalowaniu DAVa staje si� on r�wnie� zapisywalnym. Co wi�cej je�li
u�ywasz DAVfs to mo�esz montowa� sw�j serwer www jako system plik�w i
u�ywa� tak jak normalnego dysku.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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

%post   -n kernel-fs-davfs
/sbin/depmod -a

%postun -n kernel-fs-davfs
/sbin/depmod -a

%post   -n kernel-smp-fs-davfs
/sbin/depmod -a

%postun -n kernel-smp-fs-davfs
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc ChangeLog doc/*.html
%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_sbindir}/*

%files -n kernel-fs-davfs
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/%{_kernel_ver}/misc/*.o

%files -n kernel-smp-fs-davfs
%defattr(644,root,root,755)
%attr(600,root,root) /lib/modules/%{_kernel_ver}smp/misc/*.o
