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
%setup -c -T -n %{name}

%ifarch x86_64
curl -o flannel https://github.com/flannel-io/cni-plugin/releases/download/v%{version}/flannel-amd64
%endif
%ifarch aarch64
curl -o flannel https://github.com/flannel-io/cni-plugin/releases/download/v%{version}/flannel-arm64
%endif

%build

%install
mkdir %{buildroot}%{_libexecdir}/cni/bin -p
install -Dm644 ${RPM_BUILD_DIR}/%{name}/flannel -t %{buildroot}%{_libexecdir}/cni/bin/

%files
%{_libexecdir}/cni/bin/

%post

%preun

%changelog
* Sun Mar 27 2022 <bengt@fredhs.net> - 1.0.1-1
- First version
