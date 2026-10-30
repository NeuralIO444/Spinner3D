# Spinner3D Rust FFI ABI

## Version
`spinner_stroke_abi_version()` returns `2`.

## spinner_stroke_smooth_1euro
```c
int spinner_stroke_smooth_1euro(
    const float *points, uint32_t len,
    float cutoff, float beta,
    float d_cutoff, float dt,
    float *out, uint32_t out_len);
```
- `len == 0` is valid (returns 0).
- `out_len` must be >= `len * 2`.
- Pointers must be aligned for `float`.
- Overlapping `points` and `out` is rejected.
- Returns: 0 ok, -1 null, -2 panic, -3 overflow, -4 align, -5 overlap, -6 bad param, -7 out too small.

## License
See `deny.toml` for the SPDX allowlist.

## Core crates
- `spinner-stroke-core`, `spinner-gesture-core`, `spinner-pressure-core` have `#![forbid(unsafe_code)]`.
- FFI crates depend on the cores and contain only the pointer checks and exports.

## Headers
Run `./gen_headers.sh` (requires cbindgen) to regenerate `include/*.h`.
