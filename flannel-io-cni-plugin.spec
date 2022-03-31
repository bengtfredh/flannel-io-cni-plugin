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

find / -iname "flannel*"

%install
install -d -p %{buildroot}%{_libexecdir}/cni/
install -p -m 0755 bin/* %{buildroot}/%{_libexecdir}/cni

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%dir %{_libexecdir}/cni
%{_libexecdir}/cni/*

%changelog
%autochangelog
