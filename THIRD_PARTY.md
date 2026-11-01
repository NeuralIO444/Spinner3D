# Third-party crates used by Spinner3D Rust modules

All crates must be compatible with GPL-3.0-or-later. Enforced by `cargo-deny` in CI.

| Crate | License | Purpose |
|-------|---------|---------|
| (none yet) | | spinner-hello is pure Rust with no external dependencies |

## Adapted from SculptForge (GPL-3)

| Component | Source | Notes |
|-----------|--------|-------|
| Brush recipes (`.sfbrush`) | islandmed/SculptForge `src/core/BrushRecipe.h` | Schema and validation adapted into `scripts/startup/spinner/brush_recipes/`. No executable brush code is loaded. |
