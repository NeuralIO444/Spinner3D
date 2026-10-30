//! Spinner3D half-edge mesh core (R2 scaffold).
//!
//! Minimal half-edge structure with create / free / vertex count.
//! Unsafe only at the FFI boundary. Every export catches panics.

use std::panic::catch_unwind;
use std::collections::HashMap;

#[derive(Clone, Copy, Debug)]
struct HalfEdge {
    vert: u32,
    next: u32,
    twin: u32,
}

struct Mesh {
    verts: Vec<[f32; 3]>,
    edges: Vec<HalfEdge>,
    faces: Vec<u32>, // first half-edge of each face
}

static mut MESHES: Option<HashMap<u64, Mesh>> = None;
static mut NEXT_ID: u64 = 1;

fn meshes() -> &'static mut HashMap<u64, Mesh> {
    unsafe {
        if MESHES.is_none() {
            MESHES = Some(HashMap::new());
        }
        MESHES.as_mut().unwrap()
    }
}

#[no_mangle]
pub extern "C" fn spinner_mesh_create() -> u64 {
    catch_unwind(|| {
        let id = unsafe { NEXT_ID };
        unsafe { NEXT_ID += 1; }
        meshes().insert(id, Mesh { verts: Vec::new(), edges: Vec::new(), faces: Vec::new() });
        id
    })
    .unwrap_or(0)
}

#[no_mangle]
pub extern "C" fn spinner_mesh_free(id: u64) -> i32 {
    catch_unwind(|| {
        if meshes().remove(&id).is_some() { 0 } else { -1 }
    })
    .unwrap_or(-2)
}

#[no_mangle]
pub extern "C" fn spinner_mesh_vert_count(id: u64) -> i32 {
    catch_unwind(|| {
        meshes().get(&id).map(|m| m.verts.len() as i32).unwrap_or(-1)
    })
    .unwrap_or(-2)
}

#[no_mangle]
pub unsafe extern "C" fn spinner_mesh_add_vert(id: u64, x: f32, y: f32, z: f32) -> i32 {
    catch_unwind(|| {
        if !x.is_finite() || !y.is_finite() || !z.is_finite() {
            return -3;
        }
        let m = match meshes().get_mut(&id) {
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
        let v = unsafe { spinner_mesh_add_vert(id, 1.0, 2.0, 3.0) };
        assert_eq!(v, 0);
        assert_eq!(spinner_mesh_vert_count(id), 1);
        assert_eq!(spinner_mesh_free(id), 0);
        assert_eq!(spinner_mesh_vert_count(id), -1);
    }
}
