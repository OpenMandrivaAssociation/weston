%define abi 5
%define major 0

%define _disable_lto 1

Summary:	The Weston Wayland Compositor
Name:		weston
Version:	5.0.0
Release:	1
Source0:	http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
Source1:	weston.ini
Source2:	weston.service
License:	MIT
Group:		Graphics
Url:		http://wayland.freedesktop.org/
# not move me
#Patch0:		0001-ENGR00314805-1-Add-Vivante-EGL-support.patch
#Patch1:		0002-ENGR00314805-2-Add-Vivante-GAL2D-support.patch
#Patch2:		0003-Distorted-line-and-shadow-if-use-2d-com.patch
#Patch3:		0005-Enable-GAL2D-compositor-in-SoloLite.patch
#Patch4:		0006-Change-GAL2D-compositor-to-be-default-i.patch
Patch10:	weston-3.0.0-toolkits-use-wayland.patch
BuildRequires:	pkgconfig(cairo) >= 1.10.0
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(cairo-egl) >= 1.11.3
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
BuildRequires:	pkgconfig(libudev) >= 136
#BuildRequires:	pkgconfig(libunwind)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libva-x11)
BuildRequires:	pkgconfig(mtdev) >= 1.1.0
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(pixman-1) >= 0.25.2
BuildRequires:	pkgconfig(poppler-glib)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-cursor)
BuildRequires:	pkgconfig(wayland-server) >= 1.14.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(x11-xcb)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-dri2)
BuildRequires:	pkgconfig(xcb-shm)
BuildRequires:	pkgconfig(xcb-xfixes)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xkbcommon) >= 0.3.0
BuildRequires:	pkgconfig(libsystemd)
#BuildRequires:	pkgconfig(freerdp2)
BuildRequires:	pam-devel
BuildRequires:	jpeg-devel

%libpackage weston-%{abi} %{major}
%libpackage weston-desktop-%{abi} %{major}

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
%configure \
    --disable-setuid-install \
    --enable-xwayland \
    --enable-demo-clients-install \
    --enable-screen-sharing \
    --enable-drm-compositor \
    --enable-wayland-compositor \
    --disable-xwayland-test \
    --disable-rdp-compositor \
    --enable-vaapi-recorder \
    --enable-clients \
    --enable-systemd-login \
    --enable-weston-launch \
    --enable-systemd-notify

%make

%install
%makeinstall_std
rm -f %{buildroot}%{_libdir}/%{name}/*.la

for d in $(find clients/ -type f -not -name Makefile -and -not -name '*.*' -and -not -name '%{name}-*'); do
    install -m755 $d %{buildroot}%{_bindir}/%{name}-$(basename $d)
done

mkdir -p %{buildroot}%{_sysconfdir}/xdg/weston
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/weston/weston.ini


install -d %{buildroot}%{_userpresetdir}
cat > %{buildroot}%{_userpresetdir}/86-weston.preset << EOF
enable weston.service
EOF

mkdir -p %{buildroot}%{_userunitdir}/
install -m 644 %{SOURCE2} %{buildroot}%{_userunitdir}/weston.service

%files
%config(noreplace) %{_sysconfdir}/xdg/weston/weston.ini
%{_userunitdir}/weston.service
%{_userpresetdir}/86-weston.preset
%{_bindir}/%{name}
%{_bindir}/wcap-decode
%attr(4755,root,root) %{_bindir}/%{name}-launch
%{_bindir}/%{name}-info
%{_bindir}/%{name}-terminal
%{_libexecdir}/%{name}-*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%dir %{_libdir}/libweston-%{abi}
%{_libdir}/libweston-%{abi}/drm-backend.so
%{_libdir}/libweston-%{abi}/fbdev-backend.so
%{_libdir}/libweston-%{abi}/gl-renderer.so
%{_libdir}/libweston-%{abi}/headless-backend.so
%{_libdir}/libweston-%{abi}/wayland-backend.so
%{_libdir}/libweston-%{abi}/x11-backend.so
%{_libdir}/libweston-%{abi}/xwayland.so
%dir %{_datadir}/%{name}
%{_datadir}/wayland-sessions/weston.desktop
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.svg
%{_mandir}/man*/*

%files demos
%{_bindir}/weston-calibrator
%{_bindir}/weston-clickdot
%{_bindir}/weston-cliptest
%{_bindir}/weston-confine
%{_bindir}/weston-dnd
%{_bindir}/weston-editor
%{_bindir}/weston-eventdemo
%{_bindir}/weston-flower
%{_bindir}/weston-fullscreen
%{_bindir}/weston-image
%{_bindir}/weston-multi-resource
%{_bindir}/weston-resizor
%{_bindir}/weston-scaler
%{_bindir}/weston-simple-dmabuf-drm
%{_bindir}/weston-simple-dmabuf-v4l
%{_bindir}/weston-simple-egl
%{_bindir}/weston-simple-shm
%{_bindir}/weston-simple-touch
%{_bindir}/weston-smoke
%{_bindir}/weston-stacking
%{_bindir}/weston-subsurfaces
%{_bindir}/weston-transformed
%{_bindir}/weston-simple-damage
%{_bindir}/weston-presentation-shm

%files devel
%{_includedir}/weston
%{_includedir}/libweston-%{abi}
%{_libdir}/pkgconfig/weston.pc
%{_libdir}/pkgconfig/libweston-%{abi}.pc
%{_libdir}/pkgconfig/libweston-desktop-%{abi}.pc
%{_libdir}/lib*.so
