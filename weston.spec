Summary:	The Weston Wayland Compositor
Name:		weston
Version:	1.6.0
Release:	4
Source0:	http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
License:	MIT
Group:		Graphics
Url:		http://wayland.freedesktop.org/
Patch0:		0001-libinput-device-use-the-new-merged-scroll-events.patch
Patch1:		0001-libinput-device-use-the-discrete-axis-value-for-whee.patch
BuildRequires:	pkgconfig(cairo) >= 1.10.0
BuildRequires:	pkgconfig(wayland-egl)
%ifarch	%arm aarch64
BuildRequires:	pkgconfig(cairo-egl) >= 1.11.3
%endif
BuildRequires:	pkgconfig(cairo-xcb)
BuildRequires:	pkgconfig(colord) >= 0.1.27
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(egl) >= 7.10
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libdrm) >= 2.4.30
BuildRequires:	pkgconfig(libinput)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(libudev) >= 136
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libva-x11)
BuildRequires:	pkgconfig(mtdev) >= 1.1.0
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(pixman-1) >= 0.25.2
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-cursor)
BuildRequires:	pkgconfig(wayland-server) >= %{version}
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(x11-xcb)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-dri2)
BuildRequires:	pkgconfig(xcb-shm)
BuildRequires:	pkgconfig(xcb-xfixes)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xkbcommon) >= 0.3.0
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pam-devel
BuildRequires:	jpeg-devel

%description
Weston is the reference implementation of a Wayland compositor, and a
useful compositor in its own right. Weston has various backends that
lets it run on Linux kernel modesetting and evdev input as well as
under X11.
There is also a quite capable terminal emulator (weston-terminal) and
an toy/example desktop shell. Finally, Weston also provides
integration with the Xorg server and can pull X clients into the
Wayland desktop and act as a X window manager.

%package demos
Summary:	Demo clients for Weston
Group:		Graphics

%description demos
This package contains a few example clients for Weston, from simple
clients that demonstrate certain aspects of the protocol to more
complete clients and a simplistic toolkit demo clients for Weston.


%package devel
Summary: Common headers for weston
License: MIT
%description devel
Common headers for weston

%prep
%setup -q
%apply_patches

%build
autoreconf -vfi
%configure \
	--disable-setuid-install \
        --enable-demo-clients-install \
        --enable-screen-sharing
%make

%install
%makeinstall_std
rm -f %{buildroot}%{_libdir}/%{name}/*.la

for d in $(find clients/ -type f -not -name Makefile -and -not -name '*.*' -and -not -name '%{name}-*'); do
    install -m755 $d %{buildroot}%{_bindir}/%{name}-$(basename $d)
done

%files
%{_bindir}/%{name}
%{_bindir}/wcap-decode
%attr(4755,root,root) %{_bindir}/%{name}-launch
%{_bindir}/%{name}-info
%{_bindir}/%{name}-terminal
%{_libexecdir}/%{name}-*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.svg
%{_mandir}/man*/*

%files demos
%{_bindir}/weston-calibrator
%{_bindir}/weston-clickdot
%{_bindir}/weston-cliptest
%{_bindir}/weston-dnd
%{_bindir}/weston-editor
%{_bindir}/weston-eventdemo
%{_bindir}/weston-flower
%{_bindir}/weston-fullscreen
%{_bindir}/weston-image
%{_bindir}/weston-multi-resource
%{_bindir}/weston-resizor
%{_bindir}/weston-scaler
%{_bindir}/weston-simple-egl
%{_bindir}/weston-simple-shm
%{_bindir}/weston-simple-touch
%{_bindir}/weston-smoke
%{_bindir}/weston-stacking
%{_bindir}/weston-subsurfaces
%{_bindir}/weston-transformed
%{_bindir}/weston-simple-damage

%files devel
%{_includedir}/weston/*.h
%{_libdir}/pkgconfig/weston.pc
