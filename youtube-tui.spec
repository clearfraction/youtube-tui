Name:           youtube-tui
Version:        %(unset https_proxy && curl -s https://api.github.com/repos/Siriusmart/youtube-tui/releases/latest | grep -oP '"tag_name": "v\K(.*)(?=")')
Release:        1
URL:            https://github.com/Siriusmart/youtube-tui
Source0:        https://github.com/Siriusmart/youtube-tui/archive/refs/tags/v%{version}.tar.gz
Source1:        https://github.com/libsixel/libsixel/archive/refs/tags/v1.10.3.tar.gz
Summary:        An aesthetically pleasing YouTube TUI written in Rust
License:        GPLv3
BuildRequires:  rustc
BuildRequires:  libxcb-dev
BuildRequires:  openssl-dev
BuildRequires:  meson
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gdlib)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(zlib)
 
%description
An aesthetically pleasing YouTube TUI written in Rust

%prep
%setup -q -n youtube-tui-%{version} -a 1
echo -e "[profile.release]\nlto = true\nincremental = false\n" Cargo.toml
cargo fetch --locked


%build
export CFLAGS="$CFLAGS -Ofast -fno-lto -falign-functions=32 -fno-semantic-interposition -fstack-protector-strong -fzero-call-used-regs=used -mno-vzeroupper -mprefer-vector-width=256  "
export FCFLAGS="$CFLAGS -Ofast -fno-lto -falign-functions=32 -fno-semantic-interposition -fstack-protector-strong -fzero-call-used-regs=used -mno-vzeroupper -mprefer-vector-width=256  "
export FFLAGS="$CFLAGS -Ofast -fno-lto -falign-functions=32 -fno-semantic-interposition -fstack-protector-strong -fzero-call-used-regs=used -mno-vzeroupper -mprefer-vector-width=256  "
export CXXFLAGS="$CXXFLAGS -Ofast -fno-lto -falign-functions=32 -fno-semantic-interposition -fstack-protector-strong -fzero-call-used-regs=used -mno-vzeroupper -mprefer-vector-width=256  "
export RUSTFLAGS="$RUSTFLAGS -C target-cpu=westmere -C target-feature=+avx -C opt-level=3 -C codegen-units=1 -C panic=abort -Clink-arg=-Wl,-z,now,-z,relro,-z,max-page-size=0x4000,-z,separate-code "
pushd libsixel*
meson --libdir=lib64 --prefix=/usr --buildtype=plain \
  -Dgdk-pixbuf2=enabled \
  -Dlibcurl=enabled \
  -Dtests=disabled builddir
ninja -v -C builddir
DESTDIR=/ ninja -C builddir install
popd
cargo build --release --locked --offline --all-features


%install
install -D -m755 target/release/youtube-tui %{buildroot}/usr/bin/youtube-tui
install -D -m755 /usr/lib64/libsixel.so.* -t %{buildroot}/usr/lib64


%files
%defattr(-,root,root,-)
/usr/bin/youtube-tui
/usr/lib64/libsixel.so.*
