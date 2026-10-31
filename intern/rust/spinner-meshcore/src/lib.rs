//! Spinner3D half-edge mesh core (R2).
//!
//! Minimal half-edge structure with create / free / vertex count.
//! Thread-safe via Mutex. Unsafe only at the FFI boundary.
//! Every export catches panics.

use std::collections::HashMap;
use std::panic::catch_unwind;
use std::sync::{Mutex, OnceLock};

#[derive(Clone, Copy, Debug)]
#[allow(dead_code)]
struct HalfEdge {
    vert: u32,
    next: u32,
    twin: u32,
}

#[allow(dead_code)]
struct Mesh {
    verts: Vec<[f32; 3]>,
    edges: Vec<HalfEdge>,
    faces: Vec<u32>,
}

struct Registry {
    next_id: u64,
    meshes: HashMap<u64, Mesh>,
}

fn registry() -> &'static Mutex<Registry> {
    static REG: OnceLock<Mutex<Registry>> = OnceLock::new();
    REG.get_or_init(|| {
        Mutex::new(Registry {
            next_id: 1,
            meshes: HashMap::new(),
        })
    })
}

#[no_mangle]
pub extern "C" fn spinner_mesh_create() -> u64 {
    catch_unwind(|| {
        let mut reg = match registry().lock() {
            Ok(r) => r,
            Err(_) => return 0,
        };
        let id = reg.next_id;
        reg.next_id += 1;
        reg.meshes.insert(
            id,
            Mesh {
                verts: Vec::new(),
                edges: Vec::new(),
                faces: Vec::new(),
            },
        );
        id
    })
    .unwrap_or(0)
}

#[no_mangle]
pub extern "C" fn spinner_mesh_free(id: u64) -> i32 {
    catch_unwind(|| {
        let mut reg = match registry().lock() {
            Ok(r) => r,
            Err(_) => return -2,
        };
        if reg.meshes.remove(&id).is_some() {
            0
        } else {
            -1
        }
    })
    .unwrap_or(-2)
}

#[no_mangle]
pub extern "C" fn spinner_mesh_vert_count(id: u64) -> i32 {
    catch_unwind(|| {
        let reg = match registry().lock() {
            Ok(r) => r,
            Err(_) => return -2,
        };
        reg.meshes
            .get(&id)
            .map(|m| m.verts.len() as i32)
            .unwrap_or(-1)
    })
    .unwrap_or(-2)
}

#[no_mangle]
pub extern "C" fn spinner_mesh_add_vert(id: u64, x: f32, y: f32, z: f32) -> i32 {
    catch_unwind(|| {
        if !x.is_finite() || !y.is_finite() || !z.is_finite() {
            return -3;
        }
        let mut reg = match registry().lock() {
            Ok(r) => r,
            Err(_) => return -2,
        };
        let m = match reg.meshes.get_mut(&id) {
            Some(m) => m,
            None => return -1,
        };
        m.verts.push([x, y, z]);
        (m.verts.len() - 1) as i32
    })
    .unwrap_or(-2)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn create_add_free() {
        let id = spinner_mesh_create();
        assert_ne!(id, 0);
        assert_eq!(spinner_mesh_vert_count(id), 0);
        let v = spinner_mesh_add_vert(id, 1.0, 2.0, 3.0);
        assert_eq!(v, 0);
        assert_eq!(spinner_mesh_vert_count(id), 1);
        assert_eq!(spinner_mesh_free(id), 0);
        assert_eq!(spinner_mesh_vert_count(id), -1);
    }
}
