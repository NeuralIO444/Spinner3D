//! Spinner3D remesh scaffold (R2).
//!
//! Minimal isotropic remesh entry point. Real algorithm later.
//! Thread-safe via Mutex. Every export catches panics.

use std::collections::HashMap;
use std::panic::catch_unwind;
use std::sync::{Mutex, OnceLock};

struct RemeshJob {
    target_edge_len: f32,
    iterations: u32,
}

struct Registry {
    next_id: u64,
    jobs: HashMap<u64, RemeshJob>,
}

fn registry() -> &'static Mutex<Registry> {
    static REG: OnceLock<Mutex<Registry>> = OnceLock::new();
    REG.get_or_init(|| {
        Mutex::new(Registry {
            next_id: 1,
            jobs: HashMap::new(),
        })
    })
}

#[no_mangle]
pub extern "C" fn spinner_remesh_create(target_edge_len: f32, iterations: u32) -> u64 {
    catch_unwind(|| {
        if !target_edge_len.is_finite() || target_edge_len <= 0.0 {
            return 0;
        }
        let mut reg = match registry().lock() {
            Ok(r) => r,
            Err(_) => return 0,
        };
        let id = reg.next_id;
        reg.next_id += 1;
        reg.jobs.insert(
            id,
            RemeshJob {
                target_edge_len,
                iterations,
            },
        );
        id
    })
    .unwrap_or(0)
}

#[no_mangle]
pub extern "C" fn spinner_remesh_free(id: u64) -> i32 {
    catch_unwind(|| {
        let mut reg = match registry().lock() {
            Ok(r) => r,
            Err(_) => return -2,
        };
        if reg.jobs.remove(&id).is_some() {
            0
        } else {
            -1
        }
    })
    .unwrap_or(-2)
}

#[no_mangle]
pub extern "C" fn spinner_remesh_iterations(id: u64) -> i32 {
    catch_unwind(|| {
        let reg = match registry().lock() {
            Ok(r) => r,
            Err(_) => return -2,
        };
        reg.jobs.get(&id).map(|j| j.iterations as i32).unwrap_or(-1)
    })
    .unwrap_or(-2)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn create_query_free() {
        let id = spinner_remesh_create(0.1, 5);
        assert_ne!(id, 0);
        assert_eq!(spinner_remesh_iterations(id), 5);
        assert_eq!(spinner_remesh_free(id), 0);
        assert_eq!(spinner_remesh_iterations(id), -1);
    }
}
