Packager: Bengt Fredh <bengt@fredhs.net> 

%define name flannel-io-cni-plugin
%define sourcename cni-plugin
%define version 1.2.0
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
Source0: https://github.com/flannel-io/cni-plugin/archive/refs/tags/v%{version}.tar.gz
BuildRequires: git-core golang go-rpm-macros tree

%global debug_package %{nil}

%description
Plugin designed to work in conjunction with flannel

%prep
pwd
tree
%autosetup -Sgit -v -n %{sourcename}-%{version}
pwd
tree

%build
export ORG_PATH="github.com/flannel-io"
export REPO_PATH="$ORG_PATH/cni-plugin"

if [ ! -h gopath/src/${REPO_PATH} ]; then
        mkdir -p gopath/src/${ORG_PATH}
        ln -s ../../../.. gopath/src/${REPO_PATH} || exit 255
fi
 
export GOPATH=$(pwd)/gopath
mkdir -p $(pwd)/bin

make build_linux

pwd
tree

%install
pwd
tree
install -d -p %{buildroot}%{_libexecdir}/cni/
install -p -m 0755 flannel-%{archbuild} %{buildroot}%{_libexecdir}/cni/flannel

%files
%dir %{_libexecdir}/cni
%{_libexecdir}/cni/*

%post

%preun

%changelog
%autochangelog

