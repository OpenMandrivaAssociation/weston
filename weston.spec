%global optflags %{optflags} -Wno-error=implicit-function-declaration -Wno-error=int-conversion
%global build_ldflags %{build_ldflags} -Wl,-z,undefs -Wl,--allow-shlib-undefined

%define abi 14
%define major 0

%bcond_without pipewire

Summary:	The Weston Wayland Compositor
Name:		weston
Version:	14.0.2
Release:	2
License:	MIT
Group:		Graphics
Url:		https://wayland.freedesktop.org/
Source0:	https://gitlab.freedesktop.org/wayland/weston/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz
Source1:	weston.ini
Source2:	weston.socket
Source3:	weston.service
# not move me
Patch0:		weston-3.0.0-toolkits-use-wayland.patch
BuildRequires:	meson
BuildRequires:	pkgconfig(cairo) >= 1.10.0
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-protocols)
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
BuildRequires:	pkgconfig(xcb-cursor)
BuildRequires:	pkgconfig(xcb-dri2)
BuildRequires:	pkgconfig(xcb-shm)
BuildRequires:	pkgconfig(xcb-xfixes)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xkbcommon) >= 0.3.0
BuildRequires:	pkgconfig(libsystemd)
# FIXME re-enable when weston is ported to freerdp 3
#BuildRequires:	pkgconfig(freerdp2)
BuildRequires:	pkgconfig(libevdev)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-allocators-1.0)
BuildRequires:	pkgconfig(neatvnc)
%if %{with pipewire}
BuildRequires:	pkgconfig(libpipewire-0.3)
%endif
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libseat)
BuildRequires:	pkgconfig(libdisplay-info)
Requires:	xkeyboard-config
Requires:	dri-drivers
Requires:	seatd
Recommends:	falkon-core
Obsoletes:	%{mklibname weston-desktop-10 0} < 13.0.0
Obsoletes:	%{mklibname weston-10} < 13.0.0
Obsoletes:	%{mklibname weston-10 0} < 13.0.0
Obsoletes:	%{mklibname weston-11} < 13.0.0
Obsoletes:	%{mklibname weston-11 0} < 13.0.0

%libpackage weston-%{abi} %{major}

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
Requires:	%{name}

%description demos
This package contains a few example clients for Weston, from simple
clients that demonstrate certain aspects of the protocol to more
complete clients and a simplistic toolkit demo clients for Weston.

%package devel
Summary:	Common headers for weston
License:	MIT
Group:		Development/Others

%description devel
Common headers for weston.

%prep
%autosetup -p1

%build
# FIXME re-enable backend-rdp when weston is ported to freerdp 3
# FIXME re-enable backend-vnc when weston is ported to current neatvnc
%meson \
    -Dtest-junit-xml=false \
    -Dbackend-rdp=false \
    -Dbackend-vnc=false \
%if %{with pipewire}
    -Dpipewire=true \
    -Dbackend-pipewire=true
%else
    -Dpipewire=false \
    -Dbackend-pipewire=false
%endif

%meson_build

%install
%meson_install
rm -f %{buildroot}%{_libdir}/%{name}/*.la

mkdir -p %{buildroot}%{_sysconfdir}/xdg/weston
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/weston/weston.ini

mkdir -p %{buildroot}%{_userunitdir}
install -m644 %{SOURCE2} %{buildroot}%{_userunitdir}/%{name}.socket
install -m644 %{SOURCE3} %{buildroot}%{_userunitdir}/%{name}.service

%post
%systemd_user_post %{name}.service

%postun
%systemd_user_postun %{name}.service

%files
%dir %{_sysconfdir}/xdg/%{name}
%config(noreplace) %{_sysconfdir}/xdg/%{name}/%{name}.ini
#config %{_sysconfdir}/pam.d/weston-remote-access
%{_userunitdir}/%{name}.s*
%{_bindir}/%{name}
%{_bindir}/%{name}-debug
%{_bindir}/%{name}-content_protection
%{_bindir}/weston-simple-dmabuf-feedback
%{_bindir}/wcap-decode
%{_bindir}/%{name}-tablet
%{_bindir}/%{name}-terminal
%{_bindir}/%{name}-touch-calibrator
%{_bindir}/%{name}-screenshooter
%{_bindir}/%{name}-simple-dmabuf-egl
%{_libexecdir}/%{name}-*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libexec_weston.so.0*
%{_libdir}/%{name}/*.so
%dir %{_libdir}/lib%{name}-%{abi}
%{_libdir}/lib%{name}-%{abi}/drm-backend.so
%{_libdir}/lib%{name}-%{abi}/gl-renderer.so
%{_libdir}/lib%{name}-%{abi}/headless-backend.so
%if %{with pipewire}
%{_libdir}/lib%{name}-%{abi}/pipewire-plugin.so
%{_libdir}/libweston-%{abi}/pipewire-backend.so
%endif
%{_libdir}/lib%{name}-%{abi}/color-lcms.so
%{_libdir}/lib%{name}-%{abi}/remoting-plugin.so
%{_libdir}/lib%{name}-%{abi}/wayland-backend.so
%{_libdir}/lib%{name}-%{abi}/x11-backend.so
%{_libdir}/lib%{name}-%{abi}/xwayland.so
%dir %{_datadir}/%{name}
%{_datadir}/wayland-sessions/%{name}.desktop
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.svg
%doc %{_mandir}/man*/*

%files demos
%{_bindir}/weston-calibrator
%{_bindir}/weston-clickdot
%{_bindir}/weston-cliptest
%{_bindir}/weston-constraints
%{_bindir}/weston-dnd
%{_bindir}/weston-editor
%{_bindir}/weston-eventdemo
%{_bindir}/weston-flower
%{_bindir}/weston-fullscreen
%{_bindir}/weston-image
%{_bindir}/weston-multi-resource
%{_bindir}/weston-presentation-shm
%{_bindir}/weston-resizor
%{_bindir}/weston-scaler
%{_bindir}/weston-simple-damage
%{_bindir}/weston-content_protection
%{_bindir}/weston-simple-dmabuf-egl
%{_bindir}/weston-simple-dmabuf-v4l
%{_bindir}/weston-simple-egl
%{_bindir}/weston-simple-shm
%{_bindir}/weston-simple-touch
%{_bindir}/weston-smoke
%{_bindir}/weston-stacking
%{_bindir}/weston-subsurfaces
%{_bindir}/weston-touch-calibrator
%{_bindir}/weston-transformed

%files devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%dir %{_includedir}/lib%{name}-%{abi}
%{_includedir}/lib%{name}-%{abi}/*
%{_datadir}/pkgconfig/*.pc
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so
%{_datadir}/libweston-%{abi}/protocols/
