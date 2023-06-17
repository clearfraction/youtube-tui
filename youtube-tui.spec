Name:           youtube-tui
Version:        0.7.2
Release:        1
URL:            https://github.com/Siriusmart/youtube-tui
Source0:        https://github.com/Siriusmart/youtube-tui/archive/refs/tags/v%{version}.tar.gz
Summary:        An aesthetically pleasing YouTube TUI written in Rust
License:        GPLv3
BuildRequires:  rustc
BuildRequires:  libxcb-dev
BuildRequires:  openssl-dev

 
%description
An aesthetically pleasing YouTube TUI written in Rust

%prep
%setup -q -n youtube-tui-%{version}
echo -e "[profile.release]\nlto = true\nincremental = false\n" Cargo.toml
cargo fetch --locked


%build
export RUSTFLAGS="$RUSTFLAGS -C target-cpu=westmere -C target-feature=+avx -C opt-level=3 -C codegen-units=1 -C panic=abort -Clink-arg=-Wl,-z,now,-z,relro,-z,max-page-size=0x4000,-z,separate-code"
cargo build --release --locked --offline --all-features


%install
install -D -m755 target/release/youtube-tui %{buildroot}/usr/bin/youtube-tui

%files
%defattr(-,root,root,-)
/usr/bin/youtube-tui
