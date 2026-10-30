//! Tablet pressure curve evaluation for Spinner3D.
//!
//! Simple cubic Bezier curve. Called under WITH_SPINNER_RUST_PRESSURE.

use std::panic::catch_unwind;

#[no_mangle]
pub unsafe extern "C" fn spinner_pressure_eval(
    t: f32,
    p0: f32,
    p1: f32,
    p2: f32,
    p3: f32,
) -> f32 {
    let result = catch_unwind(|| {
        let t = t.clamp(0.0, 1.0);
        let u = 1.0 - t;
        u * u * u * p0 + 3.0 * u * u * t * p1 + 3.0 * u * t * t * p2 + t * t * t * p3
    });
    match result {
        Ok(v) => v,
        Err(_) => t,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn endpoints() {
        let a = unsafe { spinner_pressure_eval(0.0, 0.0, 0.3, 0.7, 1.0) };
        let b = unsafe { spinner_pressure_eval(1.0, 0.0, 0.3, 0.7, 1.0) };
        assert!((a - 0.0).abs() < 1e-5);
        assert!((b - 1.0).abs() < 1e-5);
    }
}
