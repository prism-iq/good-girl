# Build

## Linux
```
cd guide
cargo build --release
strip target/release/guide
```
Output: `guide/target/release/guide` (440KB)

## Windows
```
cd guide
cargo build --release --target x86_64-pc-windows-gnu
```
Output: `guide/target/x86_64-pc-windows-gnu/release/guide.exe`

Requires: mingw-w64 toolchain

Or build natively on Windows:
```
cargo build --release
```

## macOS
```
cd guide
cargo build --release
strip target/release/guide
```

## Verify
```
sha256sum target/release/guide
# compare with guide/guide.sha256
```

## Sign (optional)
```
gpg --detach-sign target/release/guide
```
