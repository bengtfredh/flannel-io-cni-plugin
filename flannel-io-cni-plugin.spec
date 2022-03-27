Packager: Bengt Fredh <bengt@fredhs.net> 

%define version 1.0.1
%define build 1
%define release %{build}%{?dist}
%define srcdir ${RPM_SOURCE_DIR}/cni-plugin

Summary: Plugin designed to work in conjunction with flannel
Name: flannel-io-cni-plugin
Version: %{version}
Release: %{release}
License: APL
URL: https://github.com/flannel-io/cni-plugin
BuildRequires: golang git-core make
Requires: containernetworking-cni

%global debug_package %{nil}

%description
Plugin designed to work in conjunction with flannel

%prep
git clone https://github.com/flannel-io/cni-plugin.git %{srcdir}
cd %{srcdir}
git checkout v%{version}

%build
cd %{srcdir}
go mod vendor
make -d

%install
install -d -p %{buildroot}%{_libexecdir}/cni/
install -Dm644 %{srcdir}/bin/flannel %{buildroot}%{_libexecdir}/cni/

%files
%{_libexecdir}/cni/

%post

%preun

%changelog
* Sun Mar 27 2022 <bengt@fredhs.net> - 1.0.1-1
- First version
