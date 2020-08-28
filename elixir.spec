%global debug_package %{nil}
Name:                elixir
Version:             1.8.1
Release:             1
Summary:             A modern approach to programming for the Erlang VM
License:             ASL 2.0
URL:                 http://elixir-lang.org/
Source0:             https://github.com/elixir-lang/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:             https://github.com/elixir-lang/%{name}/releases/download/v%{version}/Docs.zip#/%{name}-%{version}-doc.zip
BuildRequires:       erlang-rebar git sed
Requires:            erlang-compiler erlang-crypto erlang-erts erlang-inets erlang-kernel
Requires:            erlang-parsetools erlang-public_key erlang-stdlib erlang-tools
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
sed -i 's/$(Q)//g' Makefile

%build
export LANG=C.UTF-8
export REBAR=/usr/bin/rebar
export ERL_LIBS=/usr/share/erlang/lib/
export REBAR_DEPS_PREFER_LIBS=TRUE
make compile
make build_man

%check
export LANG=C.UTF-8
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
License:             ASL 2.0
Summary:             Documentation for the elixir language and tools
%description doc
HTML documentation for eex, elixir, iex, logger and mix.

%files doc
%license docs/LICENSE
%doc docs/doc/eex docs/doc/elixir docs/doc/iex docs/doc/logger docs/doc/mix

%changelog
* Fri Aug 28 2020 wutao <wutao61@huawei.com> - 1.8.1-1
- Package init
