%define abi 9
%define major 0

# As of 8.0.0 and 9.0.0, pipewire 0.3 is not supported. Only 0.2 but we ship new one, so this feature need to be disable for now.
%global pipewire 1

%define _disable_ld_no_undefined 1

Summary:	The Weston Wayland Compositor
Name:		weston
Version:	9.0.0
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
BuildRequires:	meson
BuildRequires:	pkgconfig(cairo) >= 1.10.0
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(cairo-egl) >= 1.11.3
BuildRequires:	pkgconfig(cairo-xcb)
BuildRequires:	pkgconfig(colord) >= 0.1.27
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(egl) >= 1.3
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
BuildRequires:	pkgconfig(freerdp2)
BuildRequires:	pkgconfig(libevdev)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-allocators-1.0)
%if %{pipewire}
BuildRequires:	pkgconfig(libpipewire-0.3)
%endif
BuildRequires:	pam-devel
BuildRequires:	jpeg-devel
Requires:	xkeyboard-config

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
%autosetup -p1

%build
%meson \
    -Dtest-junit-xml=false \
%if %{pipewire}
    -Dpipewire=false \
%endif
%ifnarch %{armx}
    -Dsimple-dmabuf-drm=intel
%else
    -Dsimple-dmabuf-drm="freedreno,etnaviv"
%endif
   

%meson_build

%install
%meson_install
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
%dir %{_sysconfdir}/xdg/%{name}
%config(noreplace) %{_sysconfdir}/xdg/%{name}/%{name}.ini
%{_userunitdir}/%{name}.service
%{_userpresetdir}/86-%{name}.preset
%{_bindir}/%{name}
%{_bindir}/%{name}-debug
%{_bindir}/%{name}-content_protection
%{_libdir}/weston/libexec_weston.so.0*
%{_bindir}/wcap-decode
%attr(4755,root,root) %{_bindir}/%{name}-launch
%{_bindir}/%{name}-info
%{_bindir}/%{name}-terminal
%{_bindir}/%{name}-touch-calibrator
%{_bindir}/%{name}-screenshooter
%{_bindir}/%{name}-simple-dmabuf-egl
%{_libexecdir}/%{name}-*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%dir %{_libdir}/lib%{name}-%{abi}
%{_libdir}/lib%{name}-%{abi}/drm-backend.so
%{_libdir}/lib%{name}-%{abi}/fbdev-backend.so
%{_libdir}/lib%{name}-%{abi}/gl-renderer.so
%{_libdir}/lib%{name}-%{abi}/headless-backend.so
%if %{pipewire}
#{_libdir}/lib%{name}-%{abi}/pipewire-plugin.so
%else
%{_libdir}/lib%{name}-%{abi}/pipewire-plugin.so
%endif
%{_libdir}/libweston-8/rdp-backend.so
%{_libdir}/lib%{name}-%{abi}/remoting-plugin.so
%{_libdir}/lib%{name}-%{abi}/wayland-backend.so
%{_libdir}/lib%{name}-%{abi}/x11-backend.so
%{_libdir}/lib%{name}-%{abi}/xwayland.so
%dir %{_datadir}/%{name}
%{_datadir}/wayland-sessions/%{name}.desktop
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.svg
%{_mandir}/man*/*

%files demos
%{_bindir}/%{name}-calibrator
%{_bindir}/%{name}-clickdot
%{_bindir}/%{name}-cliptest
%{_bindir}/%{name}-confine
%{_bindir}/%{name}-dnd
%{_bindir}/%{name}-editor
%{_bindir}/%{name}-eventdemo
%{_bindir}/%{name}-flower
%{_bindir}/%{name}-fullscreen
%{_bindir}/%{name}-image
%{_bindir}/%{name}-multi-resource
%{_bindir}/%{name}-resizor
%{_bindir}/%{name}-scaler
%{_bindir}/%{name}-simple-dmabuf-v4l
%{_bindir}/%{name}-simple-egl
%{_bindir}/%{name}-simple-shm
%{_bindir}/%{name}-simple-touch
%{_bindir}/%{name}-smoke
%{_bindir}/%{name}-stacking
%{_bindir}/%{name}-subsurfaces
%{_bindir}/%{name}-transformed
%{_bindir}/%{name}-simple-damage
%{_bindir}/%{name}-presentation-shm

%files devel
%{_includedir}/%{name}
%{_includedir}/lib%{name}-%{abi}
%{_datadir}/pkgconfig/lib%{name}-%{abi}-protocols.pc
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/lib%{name}-%{abi}.pc
%{_libdir}/pkgconfig/lib%{name}-desktop-%{abi}.pc
%{_libdir}/lib*.so
%{_datadir}/libweston-%{abi}
