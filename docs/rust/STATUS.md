# Rust Port Status (2026-10-30)

## Branches on GitHub

| Branch | Contents |
|--------|----------|
| `spinner/rust-r0` | Workspace, Corrosion, hello, CI, NOT_PORTED.md |
| `spinner/rust-qa` | Clippy fixes, deny.toml, stroke shim behind flag |
| `spinner/rust-stroke` | 1€ smoother |
| `spinner/rust-gesture` | Tap/drag classifier |
| `spinner/rust-assets` | CLI validator |
| `spinner/rust-pressure` | Bezier pressure curve |
| `spinner/rust-meshcore` | Half-edge scaffold + Mutex + shim |
| `spinner/rust-remesh-repair` | Remesh + repair scaffolds + shims |
| `spinner/rust-stroke-bench` | Golden test + criterion bench |

## Open gaps

- No Rust PRs yet (forms were shown earlier).
- No golden expected-output files (self-compare only).
- No C++ baseline for the ≤5% budget.
- No per-module CI that fails on regression.
- R3–R6 not started.
