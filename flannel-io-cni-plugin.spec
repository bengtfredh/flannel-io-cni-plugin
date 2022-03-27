Packager: Bengt Fredh <bengt@fredhs.net> 

%define name flannel-io-cni-plugin
%define version 1.0.1
%define build 1
%define release %{build}%{?dist}

Summary: Plugin designed to work in conjunction with flannel
Name: %{name}
Version: %{version}
Release: %{release}
License: APL 2.0
URL: https://github.com/flannel-io/cni-plugin
Requires: containernetworking-cni

%global debug_package %{nil}

%description
Plugin designed to work in conjunction with flannel

%prep
mkdir %{name}
cd %{name}
%build
%ifarch x86_64
curl -o flannel https://github.com/flannel-io/cni-plugin/releases/download/v%{version}/flannel-amd64
%endif
%ifarch aarch64
curl -o flannel  https://github.com/flannel-io/cni-plugin/releases/download/v%{version}/flannel-arm64
%endif
%setup -c -T

%build

%install
mkdir %{buildroot}/usr/libexec/cni -p
install -Dm644 ${RPM_BUILD_DIR}/%{name}/flannel %{buildroot}/usr/libexec/cni

%files
/usr/libexec/cni/

%post

%preun

%changelog
* Sun Mar 27 2022 <bengt@fredhs.net> - 1.0.1-1
- First version
