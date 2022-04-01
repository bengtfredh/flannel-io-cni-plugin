%global with_devel 1

%if 0%{?fedora}
%global with_debug 1
%else
%global with_debug 0
%endif

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) GO111MODULE=off go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld '" -a -v -x %{?**};
%endif

%global provider github
%global provider_tld com
%global project flannel-io
%global repo cni-plugin
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global git0 https://%{import_path}

%global built_tag v1.0.1
%global built_tag_strip %(b=%{built_tag}; echo ${b:1})
%global gen_version %(b=%{built_tag_strip}; echo ${b/-/"~"})
%define debug_package %{nil}

Name: %{project}-%{repo}
Version: %{gen_version}
Release: %autorelease
Summary: Libraries for writing CNI plugin
License: ASL 2.0
URL: %{git0}
Source0: %{git0}/archive/%{built_tag}.tar.gz
BuildRequires: golang >= 1.16.6
BuildRequires: go-rpm-macros
BuildRequires: git
BuildRequires: go-md2man
BuildRequires: go-rpm-macros
BuildRequires: systemd-devel
Requires: systemd

Provides: %{project}-cni = %{version}-%{release}
Provides: kubernetes-cni
Provides: flannel-cni
Requires: containernetworking-plugins

Provides: bundled(golang(github.com/Microsoft/go_winio)) = v0.4.17
Provides: bundled(golang(github.com/Microsoft/hcsshim)) = v0.8.20
Provides: bundled(golang(github.com/alexflint/go_filemutex)) = v1.1.0
Provides: bundled(golang(github.com/buger/jsonparser)) = v1.1.1
Provides: bundled(golang(github.com/containerd/cgroups)) = v1.0.1
Provides: bundled(golang(github.com/containernetworking/cni)) = v1.0.1
Provides: bundled(golang(github.com/coreos/go_iptables)) = v0.6.0
Provides: bundled(golang(github.com/coreos/go_systemd/v22)) = v22.3.2
Provides: bundled(golang(github.com/d2g/dhcp4)) = v0.0.0_20170904100407_a1d1b6c41b1c
Provides: bundled(golang(github.com/d2g/dhcp4client)) = v1.0.0
Provides: bundled(golang(github.com/d2g/dhcp4server)) = v0.0.0_20181031114812_7d4a0a7f59a5
Provides: bundled(golang(github.com/fsnotify/fsnotify)) = v1.4.9
Provides: bundled(golang(github.com/godbus/dbus/v5)) = v5.0.4
Provides: bundled(golang(github.com/gogo/protobuf)) = v1.3.2
Provides: bundled(golang(github.com/golang/groupcache)) = v0.0.0_20200121045136_8c9f03a8e57e
Provides: bundled(golang(github.com/mattn/go_shellwords)) = v1.0.12
Provides: bundled(golang(github.com/networkplumbing/go_nft)) = v0.2.0
Provides: bundled(golang(github.com/nxadm/tail)) = v1.4.8
Provides: bundled(golang(github.com/onsi/ginkgo)) = v1.16.4
Provides: bundled(golang(github.com/onsi/gomega)) = v1.15.0
Provides: bundled(golang(github.com/pkg/errors)) = v0.9.1
Provides: bundled(golang(github.com/safchain/ethtool)) = v0.0.0_20210803160452_9aa261dae9b1
Provides: bundled(golang(github.com/sirupsen/logrus)) = v1.8.1
Provides: bundled(golang(github.com/vishvananda/netlink)) = v1.1.1_0.20210330154013_f5de75959ad5
Provides: bundled(golang(github.com/vishvananda/netns)) = v0.0.0_20210104183010_2eb08e3e575f

%description
This plugin is designed to work in conjunction with flannel, a network fabric for containers. When flannel daemon is started, it outputs a /run/flannel/subnet.env

%prep
%autosetup -Sgit -n %{repo}-%{built_tag_strip}

%build
export ORG_PATH="%{provider}.%{provider_tld}/%{project}"
export REPO_PATH="$ORG_PATH/%{repo}"

if [ ! -h gopath/src/${REPO_PATH} ]; then
        mkdir -p gopath/src/${ORG_PATH}
        ln -s ../../../.. gopath/src/${REPO_PATH} || exit 255
fi

export GOPATH=$(pwd)/gopath
mkdir -p $(pwd)/bin

echo "Building plugin"
go mod vendor
make

%ifarch x86_64
mv dist/flannel-amd64 bin/flannel
%endif
%ifarch aarch64
mv dist/flannel-arm64 bin/flannel
%endif

%install
install -d -p %{buildroot}%{_libexecdir}/cni/
install -p -m 0755 bin/* %{buildroot}%{_libexecdir}/cni

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%dir %{_libexecdir}/cni
%{_libexecdir}/cni/*

%changelog
%autochangelog
