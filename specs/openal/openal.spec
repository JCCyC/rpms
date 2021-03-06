# $Id$
# Authority: dries


%{?el3:%define _without_alsa 1}

%define real_name openal-soft

Summary: Open Audio Library
Name: openal
Version: 1.8.466
Release: 1%{?dist}
License: LGPL
Group: System Environment/Libraries
URL: http://www.openal.org/

#http://connect.creativelabs.com/openal/Downloads/openal-soft-1.8.466.bz2
Source0: http://connect.creativelabs.com/openal/Downloads/openal-soft-%{version}.bz2
#Source0: http://www.openal.org/openal_webstf/downloads/openal-%{version}.tar.gz
Source1: openalrc
Patch0: openal-0.0.8-arch.patch
Patch1: openal-0.0.8-no-undefined.patch
Patch2: openal-0.0.8-pkgconfig.patch
Patch3: openal-0.0.8-pause.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: esound-devel
BuildRequires: libogg-devel
BuildRequires: libvorbis-devel
BuildRequires: SDL-devel
BuildRequires: texinfo
%{!?_without_alsa:BuildRequires: alsa-lib-devel}
%{!?_without_arts:BuildRequires: arts-devel}

%description
OpenAL is an audio library designed in the spirit of OpenGL--machine
independent, cross platform, and data format neutral, with a clean,
simple C-based API.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -n %{real_name}-%{version}
#patch2
#patch3 -p1
#patch0 -p1

### Fix reference to /usr/lib instead of %%{_libdir}
%{__perl} -pi -e 's|/lib\b|/%{_lib}|g' admin/pkgconfig/Makefile.in

%build
cmake all
%configure \
    --disable-smpeg \
%{!?_without_alsa:--enable-alsa} \
%{!?_without_arts:--enable-arts} \
    --enable-capture \
    --enable-esd \
    --enable-sdl \
    --enable-vorbis
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%{__install} -Dp -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/openalrc

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NOTES PLATFORM README
%config(noreplace) %{_sysconfdir}/openalrc
%{_libdir}/libopenal.so.*

%files devel
%defattr(-, root, root, 0755)
%{_bindir}/openal-config
%{_includedir}/AL/
%{_libdir}/libopenal.a
%exclude %{_libdir}/libopenal.la
%{_libdir}/libopenal.so
%{_libdir}/pkgconfig/openal.pc

%changelog
* Sun Jul 12 2009 Dag Wieers <dag@wieers.com> - 1.8.466-1
- Updated to release 1.8.466.

* Tue Feb 20 2007 Dag Wieers <dag@wieers.com> - 0.0.8-2
- Added patches to build on x86_64.

* Sat Dec 31 2005 Dries Verachtert <dries@ulyssis.org> - 0.0.8-1
- Updated to release 0.0.8.
- Source doesn't contain an openal.info file anymore.
- --enable-alsa added.
- Spec cleanup.

* Mon Feb 09 2004 Dag Wieers <dag@wieers.com> - 0.0.0-0.20031006
- Initial package. (using DAR)
