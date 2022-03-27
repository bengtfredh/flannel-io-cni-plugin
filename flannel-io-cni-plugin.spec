Packager: Bengt Fredh <bengt@fredhs.net> 

%define version 1.0.1
%define build 1
%define release %{build}%{?dist}

Summary: Plugin designed to work in conjunction with flannel
Name: flannel-io-cni-plugin
Version: %{version}
Release: %{release}
License: APL
URL: https://github.com/flannel-io/cni-plugin
Requires: containernetworking-cni

%global debug_package %{nil}

%description
Plugin designed to work in conjunction with flannel

%prep
%ifarch x86_64
curl -o flannel https://github.com/flannel-io/cni-plugin/releases/download/v%{version}/flannel-amd64
%endif
%ifarch aarch64
curl -o flannel  https://github.com/flannel-io/cni-plugin/releases/download/v%{version}/flannel-arm64
%endif

%build

%install
install -d %{buildroot}/usr/libexec/cni
install -Dm644 ${RPM_SOURCE_DIR}/flannel %{buildroot}/usr/libexec/cni

%files
/usr/libexec/cni/

%post

%preun

%changelog
* Sun Mar 27 2022 <bengt@fredhs.net> - 1.0.1-1
- First version
