# Spinner3D Feature List

Spinner3D is a Blender 5.3 fork focused on hard-surface modeling and ZBrush-style sculpting.
This list tracks what is shipped, in progress, and planned.

Status key: ✅ done · 🚧 in progress · 📋 planned · 💡 candidate (from SculptForge or elsewhere)

## Hard-surface foundation

| Feature | Status | Notes |
|---------|--------|-------|
| Hard Surface stack operator (Bevel + Weighted Normal + Shade Auto Smooth) | ✅ | Idempotent, face strength + influence |
| Manifold boolean default with Exact fallback | ✅ | DNA/RNA + MOD_boolean.cc |
| Bool Tool bundled | ✅ | GPL-3 |
| CAD Sketcher + pinned py-slvs wheels | ✅ | All platforms |
| QRemeshify (macOS dylibs) | ✅ | “Remesh: Hard-Surface Quads” |
| Hard Surface workspace preset | ✅ | Matcap, cavity, snapping |
| Instant Meshes subprocess wrapper | ✅ | Preferences binary path |
| Manifold fallback Python test | ✅ | |
| Spinner3D icon / branding | ✅ | |

## Sculpt Z workspace

| Feature | Status | Notes |
|---------|--------|-------|
| Workspace create/switch with matcap + cavity | ✅ | |
| Brush presets from Blender brushes | ✅ | |
| Dynamesh-style voxel remesh, subdiv, isolate | ✅ | |
| Side shelf (Enter / Back to Spinner) | ✅ | |
| Radial size/strength, spacebar palette | 📋 | |
| Navigation modal (empty-space orbit, last-stroke pivot) | 📋 | |

## Rust port (strangler pattern)

Each module wraps C/C++ behind a stable C interface and swaps in behind `WITH_SPINNER_RUST_<MODULE>` (default OFF).

| Phase | Scope | Status |
|-------|-------|--------|
| R0 | Cargo workspace, Corrosion, spinner-hello, CI, deny.toml | ✅ |
| R1 | spinner-stroke (1€), gesture, assets, pressure | 🚧 stroke shim wired; golden + criterion in #17 |
| R2 | meshcore, remesh, repair, decimate, project | 🚧 scaffolds in #15, #16 |
| R3 | I/O (OBJ/STL/PLY) | 📋 #11 |
| R4 | Geometry kernels (SDF, B-rep) | 📋 #12 |
| R5 | Sculpt internals (brush kernels, PBVH) | 📋 #13 |
| R6 | Sidecar processes (spinner-ai, spinner-bake) | 📋 #14 |

### Rust rules

- `#![deny(unsafe_op_in_unsafe_fn)]`, unsafe only in `*-ffi`
- every export catches panics (`catch_unwind`)
- GPL-3 compatible crates only (`cargo-deny`)
- determinism via golden-file / replay tests
- ≤ 5% slower than C++ baseline (`criterion`)
- Windows (MSVC), macOS (arm64 + x86_64), Linux

## SculptForge loot candidates (GPL-3)

| Feature | Status | Source | Notes |
|---------|--------|--------|-------|
| Brush recipes (`.sfbrush`) | 💡 | `src/core/BrushRecipe.h` | Data-driven brushes: direction, plane, pinch, drag, pattern, hardness |
| ZSpheres | 💡 | `src/core/ZSpheres.h` | Organic base mesh from connected spheres → watertight quads |
| Dyntopo (Sculptris Pro) | 💡 | `src/core/Dyntopo.h` | Local remesh under brush, keeps boundaries / polygroups / symmetry |
| Voxel remesh (DynaMesh) | 💡 | `src/core/Voxel.h` | Shell → grid → flood-fill → surface nets |
| Incremental BVH | 💡 | `src/core/BVH.h` | Refit for brush queries; feeds R5 |
| Mask / polygroup gestures | 💡 | `docs/zbrush-parity.md` | Ctrl+click blur/sharpen, lasso, invert, isolate |
| VDM stamps | 💡 | `src/core/Vdm.h` | Vector displacement (horns, ears, overhangs) |
| QRemesh Guides | 💡 | `src/core/QRemeshGuides.h` | Quad remesh with guide curves |
| GoZ import/export | 💡 | `src/io/GozIO.*` | Binary GoZ + bridge |
| Blender bridge pattern | 💡 | `addons/blender/` | Two-way GoZ + JSON manifest, object identity |

## Stays C/C++

Window manager / UI / editors, Python API, Depsgraph, Draw/GPU (EEVEE, Workbench), Undo, DNA/RNA, .blend I/O.
See `docs/rust/NOT_PORTED.md`.

## Tracking

- Issues: #10 (R2), #11 (R3), #12 (R4), #13 (R5), #14 (R6)
- Open PRs: #15 (meshcore), #16 (remesh-repair), #17 (stroke-bench)
- Plan: `docs/rust/PLAN.md`
