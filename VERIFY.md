# Verification

## Source Hash
```
sha256sum guide/src/main.rs
```
Expected: see guide/guide.sha256

## Binary Hash
```
sha256sum guide/target/release/guide
```
Expected: see guide/guide.sha256

## Verify Build Reproducibility
```
cargo build --release
strip target/release/guide
sha256sum target/release/guide
```
Must match published hash.

## Open Source Proof
- Full source in guide/src/main.rs
- Zero external dependencies (Cargo.toml)
- Build yourself: `cargo build --release`
- Compare hashes

## No Malware Proof
- localhost only (127.0.0.1)
- no network calls
- no file access except daemon.flow output
- no system modifications
- all inputs sanitized
- all limits enforced

## Sign Your Build
```
gpg --detach-sign guide/target/release/guide
```

## Verify Signature
```
gpg --verify guide/target/release/guide.sig
```
