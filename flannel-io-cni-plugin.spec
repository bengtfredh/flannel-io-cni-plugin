Packager: Bengt Fredh <bengt@fredhs.net> 

%define name flannel-io-cni-plugin
%define version 1.0.1
%define releasebuild 1
%define release %{releasebuild}%{?dist}

Summary: Plugin designed to work in conjunction with flannel
Name: %{name}
Version: %{version}
Release: %{release}
License: APL 2.0
URL: https://github.com/flannel-io
Requires: containernetworking-plugins

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
chmod 0755 flannel

%build

%install
install -d -p %{buildroot}%{_libexecdir}/cni/
install -p -m 0755 ${RPM_BUILD_DIR}/%{name}/flannel %{buildroot}%{_libexecdir}/cni

%files
%dir %{_libexecdir}/cni
%{_libexecdir}/cni/*

%post

%preun

%changelog
%autochangelog

