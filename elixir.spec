%global debug_package %{nil}
%global __with_rebar 1
%global __with_rebar3 0
Name:           elixir
Version:        1.12.0
Release:        1
Summary:        A modern approach to programming for the Erlang VM
License:        ASL 2.0
URL:            http://elixir-lang.org/
Source0:        https://github.com/elixir-lang/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/elixir-lang/%{name}/releases/download/v%{version}/Docs.zip#/%{name}-%{version}-doc.zip
BuildRequires: erlang-compiler erlang-crypto erlang-dialyzer erlang-erts erlang-eunit
BuildRequires: erlang-inets erlang-kernel erlang-parsetools erlang-public_key
%if %{__with_rebar}
BuildRequires: erlang-rebar
%endif
%if %{__with_rebar3}
BuildRequires: erlang-rebar3
%endif
BuildRequires: erlang-sasl make
BuildRequires: erlang-stdlib erlang-tools erlang-xmerl git sed
Requires: erlang-compiler erlang-crypto erlang-erts erlang-inets erlang-kernel
Requires: erlang-parsetools erlang-public_key erlang-stdlib erlang-tools erlang-sasl

%description
Elixir is a programming language built on top of the Erlang VM.
As Erlang, it is a functional language built to support distributed,
fault-tolerant, non-stop applications with hot code swapping.

%prep
%setup -q -T -c -n %{name}-%{version}/docs -a 1
find -name ".build" -exec rm \{\} \;
%setup -q -D
find -name '*.bat' -exec rm \{\} \;
rm lib/elixir/test/elixir/io/ansi_test.exs
find . -name .gitignore -delete
find . -name .gitkeep -delete
sed -i '/^Q\s*:=/d' Makefile
rm -f ./lib/mix/test/fixtures/rebar ./lib/mix/test/fixtures/rebar3
%if %{__with_rebar}
# Do nothing
%else
rm -f ./lib/mix/test/mix/rebar_test.exs
touch ./lib/mix/test/fixtures/rebar
%endif
%if %{__with_rebar3}
# Do nothing
%else
rm -f ./lib/mix/test/mix/rebar_test.exs
touch ./lib/mix/test/fixtures/rebar3
%endif

%build
export LANG=C.UTF-8
%if %{__with_rebar}
export REBAR=/usr/bin/rebar
export REBAR_DEPS_PREFER_LIBS=TRUE
%endif
%if %{__with_rebar3}
export REBAR3=/usr/bin/rebar3
%endif
export ERL_LIBS=/usr/share/erlang/lib/
make compile
make build_man

%check
export LANG=C.UTF-8
%if %{__with_rebar}
export REBAR=/usr/bin/rebar
export REBAR_DEPS_PREFER_LIBS=TRUE
%endif
%if %{__with_rebar3}
export REBAR3=/usr/bin/rebar3
%endif
export ERL_LIBS=/usr/share/erlang/lib/
make test

%install
mkdir -p %{buildroot}/%{_datadir}/%{name}/%{version}
cp -ra bin lib %{buildroot}/%{_datadir}/%{name}/%{version}
mkdir -p %{buildroot}/%{_bindir}
ln -s %{_datadir}/%{name}/%{version}/bin/{elixir,elixirc,iex,mix} %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_mandir}/man1
cp -a man/elixir.1 man/elixirc.1 man/iex.1 man/mix.1 %{buildroot}/%{_mandir}/man1

%files
%license LICENSE
%{_bindir}/elixir
%{_bindir}/elixirc
%{_bindir}/iex
%{_bindir}/mix
%{_datadir}/%{name}
%{_mandir}/man1/elixir.1*
%{_mandir}/man1/elixirc.1*
%{_mandir}/man1/iex.1*
%{_mandir}/man1/mix.1*

%package doc
License: ASL 2.0
Summary: Documentation for the elixir language and tools

%description doc
HTML documentation for eex, elixir, iex, logger and mix.

%files doc
%license docs/LICENSE
%doc docs/doc/eex docs/doc/elixir docs/doc/iex docs/doc/logger docs/doc/mix

%changelog
* Tue Jan 18 2022 Ge Wang <wangge20@huawei.com> - 1.12.0-1
- Update to version 1.12.0

* Sat Sep 19 2020 huanghaitao <huanghaitao8@huawei.com> - 1.9.0-1
- Update to fix test errors

* Fri Aug 28 2020 wutao <wutao61@huawei.com> - 1.8.1-1
- Package init
