Packager: Bengt Fredh <bengt@fredhs.net>

%define name flannel-io-cni-plugin
# renovate: datasource=github-releases depName=flannel-io/cni-plugin
%define upstream_version 1.9.1-flannel1
%define version %(echo %{upstream_version} | cut -d- -f1)
%define releasebuild 1
%define release %(echo %{upstream_version} | cut -d- -f2).%{releasebuild}%{?dist}

Summary: Plugin designed to work in conjunction with flannel
Name: %{name}
Version: %{version}
Release: %{release}
License: Apache-2.0
URL: https://github.com/flannel-io/cni-plugin
ExclusiveArch: x86_64 aarch64
Requires: containernetworking-plugins
Source0: https://github.com/flannel-io/cni-plugin/releases/download/v%{upstream_version}/flannel-amd64
Source1: https://github.com/flannel-io/cni-plugin/releases/download/v%{upstream_version}/flannel-arm64

%global debug_package %{nil}

%description
Plugin designed to work in conjunction with flannel

%prep
%setup -c -T

%build

%install
install -d -p %{buildroot}%{_libexecdir}/cni/
%ifarch x86_64
install -p -m 0755 %{SOURCE0} %{buildroot}%{_libexecdir}/cni/flannel
%endif
%ifarch aarch64
install -p -m 0755 %{SOURCE1} %{buildroot}%{_libexecdir}/cni/flannel
%endif

%files
%dir %{_libexecdir}/cni
%{_libexecdir}/cni/flannel

%changelog
%autochangelog
