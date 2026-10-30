# Spinner3D Maximum Rust Port — Tracking

Strangler pattern: each module wraps existing C/C++ behind a stable C interface, then swaps in the Rust version behind `WITH_SPINNER_RUST_<MODULE>`. Delete the old code only after parity.

## Phases

| Phase | Scope | Status |
|-------|-------|--------|
| R0 | Cargo workspace, Corrosion, spinner-hello, CI | Done (`spinner/rust-r0`, `spinner/rust-qa`) |
| R1 | spinner-stroke, gesture, assets, pressure | Scaffolded + stroke shim wired |
| R2 | meshcore, remesh, repair, decimate, project | meshcore / remesh / repair scaffolds done |
| R3 | I/O (OBJ/STL/PLY) | Not started |
| R4 | Geometry kernels (SDF, B-rep) | Not started |
| R5 | Sculpt internals (brush kernels, PBVH) | Not started |
| R6 | Sidecar processes (spinner-ai, spinner-bake) | Not started |

## Rules

- `#![deny(unsafe_op_in_unsafe_fn)]`
- unsafe only in `*-ffi` crates
- every export catches panics (`catch_unwind`)
- GPL-3 compatible crates only (`cargo-deny`)
- determinism via golden-file / replay tests
- ≤ 5% slower than C++ baseline (`criterion`)
- Windows (MSVC), macOS (arm64 + x86_64), Linux

## Stays C/C++

See `NOT_PORTED.md`.
