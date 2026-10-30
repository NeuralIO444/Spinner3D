//! Spinner3D mesh repair scaffold (R2).
//!
//! Minimal hole-fill / non-manifold fix entry point. Real algorithm later.
//! Thread-safe via Mutex. Every export catches panics.

use std::collections::HashMap;
use std::panic::catch_unwind;
use std::sync::{Mutex, OnceLock};

struct RepairJob {
    fill_holes: bool,
    fix_non_manifold: bool,
}

struct Registry {
    next_id: u64,
    jobs: HashMap<u64, RepairJob>,
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
pub extern "C" fn spinner_repair_create(fill_holes: u8, fix_non_manifold: u8) -> u64 {
    catch_unwind(|| {
        let mut reg = match registry().lock() {
            Ok(r) => r,
            Err(_) => return 0,
        };
        let id = reg.next_id;
        reg.next_id += 1;
        reg.jobs.insert(
            id,
            RepairJob {
                fill_holes: fill_holes != 0,
                fix_non_manifold: fix_non_manifold != 0,
            },
        );
        id
    })
    .unwrap_or(0)
}

#[no_mangle]
pub extern "C" fn spinner_repair_free(id: u64) -> i32 {
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
pub extern "C" fn spinner_repair_will_fill_holes(id: u64) -> i32 {
    catch_unwind(|| {
        let reg = match registry().lock() {
            Ok(r) => r,
            Err(_) => return -2,
        };
        reg.jobs
            .get(&id)
            .map(|j| if j.fill_holes { 1 } else { 0 })
            .unwrap_or(-1)
    })
    .unwrap_or(-2)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn create_query_free() {
        let id = spinner_repair_create(1, 0);
        assert_ne!(id, 0);
        assert_eq!(spinner_repair_will_fill_holes(id), 1);
        assert_eq!(spinner_repair_free(id), 0);
        assert_eq!(spinner_repair_will_fill_holes(id), -1);
    }
}
