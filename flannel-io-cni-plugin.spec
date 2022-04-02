Packager: Bengt Fredh <bengt@fredhs.net> 

%define name flannel-io-cni-plugin
%define version 1.0.1
%define releasebuild 1
%define release %{releasebuild}%{?dist}

%ifarch x86_64
%define archbuild amd64
%endif
%ifarch aarch64
%define archbuild arm64
%endif

Summary: Plugin designed to work in conjunction with flannel
Name: %{name}
Version: %{version}
Release: %{release}
License: APL 2.0
URL: https://github.com/flannel-io
Requires: containernetworking-plugins
Source0: https://github.com/flannel-io/cni-plugin/releases/download/v%{version}/cni-plugin-flannel-linux-amd64-v%{version}.tgz
Source1: https://github.com/flannel-io/cni-plugin/releases/download/v%{version}/cni-plugin-flannel-linux-arm64-v%{version}.tgz

%global debug_package %{nil}

%description
Plugin designed to work in conjunction with flannel

%prep
%setup -c -T
tar zxvf $RPM_SOURCE_DIR/cni-plugin-flannel-linux-%{archbuild}-v%{version}.tgz

%build

%install
install -d -p %{buildroot}%{_libexecdir}/cni/
install -p -m 0755 flannel-%{archbuild} %{buildroot}%{_libexecdir}/cni/flannel

%files
%dir %{_libexecdir}/cni
%{_libexecdir}/cni/*

%post

%preun

%changelog
%autochangelog

