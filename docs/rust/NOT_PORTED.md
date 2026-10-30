# Modules that stay C/C++

These components remain in C or C++ because they are tightly coupled to Blender’s ABI, have no practical Rust replacement that preserves upstream mergeability, or are not performance-critical for Spinner3D’s goals.

| Module | Reason |
|--------|--------|
| Window manager / UI / editors | Platform and RNA coupling; no stable Rust UI path |
| Python API | Blender’s embedded Python is the public extension surface |
| Depsgraph | Core evaluation graph; changes require upstream coordination |
| Draw / GPU (EEVEE, Workbench) | GPU backend and shader pipeline are C++ |
| Undo | DNA-based undo stack is deeply integrated |
| DNA / RNA | Schema and reflection system used by the entire codebase |
| .blend file I/O | Forward/backward compatibility lives in blenloader |

New Spinner-owned code should be written in Rust behind a `WITH_SPINNER_RUST_*` flag.
