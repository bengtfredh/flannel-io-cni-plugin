Packager: Bengt Fredh <bengt@fredhs.net>

%define name flannel-io-cni-plugin
# renovate: datasource=github-releases depName=flannel-io/cni-plugin
%define upstream_version 1.9.0-flannel1
%define version %(echo %{upstream_version} | cut -d- -f1)
%define releasebuild 1
%define release %(echo %{upstream_version} | cut -d- -f2).%{releasebuild}%{?dist}

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
License: Apache-2.0
URL: https://github.com/flannel-io/cni-plugin
ExclusiveArch: x86_64 aarch64
Requires: containernetworking-plugins
Source0: https://github.com/flannel-io/cni-plugin/releases/download/v%{upstream_version}/cni-plugin-flannel-linux-amd64-v%{upstream_version}.tgz
Source1: https://github.com/flannel-io/cni-plugin/releases/download/v%{upstream_version}/cni-plugin-flannel-linux-arm64-v%{upstream_version}.tgz

%global debug_package %{nil}

%description
Plugin designed to work in conjunction with flannel

%prep
%setup -c -T
tar zxvf $RPM_SOURCE_DIR/cni-plugin-flannel-linux-%{archbuild}-v%{upstream_version}.tgz

%build

%install
install -d -p %{buildroot}%{_libexecdir}/cni/
install -p -m 0755 flannel-%{archbuild} %{buildroot}%{_libexecdir}/cni/flannel

%files
%dir %{_libexecdir}/cni
%{_libexecdir}/cni/flannel

%changelog
%autochangelog
