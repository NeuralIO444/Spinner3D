# Third-Party Components

All entries below are GPL-3 compatible (GPL-3, GPL-2-or-later, LGPL, Apache-2.0, BSD, MIT, or MPL-2). Upstream copyright notices are preserved. No third-party branding appears in the Spinner3D UI.

## Rust crates

All crates must be compatible with GPL-3.0-or-later. Enforced by `cargo-deny` in CI.

| Crate | License | Purpose |
|-------|---------|---------|
| (none yet) | | spinner-hello is pure Rust with no external dependencies |

## Bundled add-ons and tools

| Project | Version / Commit | License | URL | Notes |
|---------|------------------|---------|-----|-------|
| Bool Tool | v2.1 (2026-07-14) | GPL-3.0-or-later | https://github.com/nickberckley/bool_tool | Bundle under `scripts/addons_core/` or extensions path. Cutters go into a hidden `Cutters` collection. |
| CAD Sketcher | 0.32.2 (bundled) | GPL-3.0-or-later | https://github.com/hlorus/CAD_Sketcher | Bundled under scripts/addons_core/CAD_Sketcher/ with pinned py-slvs (slvs) wheels for win/mac/linux, Python 3.11+3.13. No runtime pip. |
| py-slvs / SolveSpace bindings | (bundled with CAD Sketcher) | GPL-3 | https://github.com/realthunder/slvs_py | Pinned wheels; do not fetch at runtime. |
| QRemeshify | 1.1.0 (macOS) | GPL-3.0 | https://github.com/ksami/QRemeshify | Bundled under scripts/addons_core/QRemeshify/ with macOS dylibs only (liblib_quadwild.dylib, liblib_quadpatches.dylib). Expose as “Remesh: Hard-Surface Quads”. |
| QuadWild / bi-MDF | (used by QRemeshify) | GPL-3 | https://github.com/mlivesu/QuadWild | Upstream library. |
| Instant Meshes | (optional, not bundled) | BSD | https://github.com/wjakob/instant-meshes | Subprocess remesh wrapper. Binary path set in Preferences. No binary shipped. |
| Manifold | (already in Blender) | (upstream) | https://github.com/elalish/manifold | Make default boolean solver with Exact fallback. |

## Rejected for v1

| Project | Reason |
|---------|--------|
| MACHIN3tools (current) | Current releases are commercial (Gumroad / Superhive). Older free versions exist on some GitHub mirrors but are not the maintained GPL-3 distribution and may lack current license clarity. Not bundled. |
| libigl | MPL-2, but not required for v1 tasks (repair / distance queries deferred). |
| Hard Ops / BoxCutter / MESHmachine / DECALmachine | Proprietary / commercial. |

## How to add a new component

1. Confirm license is GPL-3 compatible.
2. Record version/commit, license, and URL in this file.
3. Place code under `scripts/addons_core/`, `scripts/startup/spinner/`, or `extern/` as appropriate.
4. Keep upstream copyright headers.
5. Open a PR against the relevant Spinner3D branch.
