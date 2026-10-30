# Spinner3D

Spinner3D is a hard-surface-oriented build of the Blender 5.3 codebase (GPL-3).

It keeps the core Blender engine and adds a small set of Python tools and recommended open-source extensions so hard-surface workflows (booleans, bevel stacks, quad remesh, constraint sketching) are available with minimal core changes.

## What is different from upstream Blender

- **Hard-surface operator** (`scripts/startup/spinner/hardsurface.py`): one-click Bevel (angle) + Weighted Normal + Smooth by Angle stack that is idempotent.
- **Manifold as preferred boolean solver** (planned small change in `MOD_boolean.cc` with Exact fallback).
- **Bundled / recommended open-source extensions** (see `THIRD_PARTY.md`):
  - Bool Tool (GPL-3)
  - CAD Sketcher + py-slvs (GPL-3)
  - QRemeshify / QuadWild (GPL-3)
- **Hard Surface workspace** preset (matcap, cavity, wireframe overlay, vertex/edge/midpoint snapping).

## Build

Follow the standard Blender build instructions:

https://developer.blender.org/docs/handbook/building_blender/

```bash
git clone https://github.com/NeuralIO444/Spinner3D.git
cd Spinner3D
git checkout spinner/hardsurface-v1
make update
make
```

## Branch plan

- `main` — tracks upstream Blender HEAD (currently `191de40e`).
- `spinner/hardsurface-v1` — hard-surface integration work. All changes land here via PRs. Do not push directly to `main`.

## License

Spinner3D as a whole is GPL-3. Individual third-party components keep their own compatible licenses. See `THIRD_PARTY.md`.
