//! Tablet pressure curve evaluation for Spinner3D.
use std::panic::catch_unwind;

#[no_mangle]
pub extern "C" fn spinner_pressure_eval(
    t: f32,
    p0: f32,
    p1: f32,
    p2: f32,
    p3: f32,
) -> f32 {
    catch_unwind(|| {
        if !t.is_finite() || ![p0, p1, p2, p3].iter().all(|v| v.is_finite()) {
            return f32::NAN;
        }
        let t = t.clamp(0.0, 1.0);
        let u = 1.0 - t;
        let v = u * u * u * p0 + 3.0 * u * u * t * p1 + 3.0 * u * t * t * p2 + t * t * t * p3;
        v.clamp(0.0, 1.0)
    })
    .unwrap_or(f32::NAN)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn endpoints() {
        let a = spinner_pressure_eval(0.0, 0.0, 0.3, 0.7, 1.0);
        let b = spinner_pressure_eval(1.0, 0.0, 0.3, 0.7, 1.0);
        assert!((a - 0.0).abs() < 1e-5);
        assert!((b - 1.0).abs() < 1e-5);
    }

    #[test]
    fn nan_on_bad_input() {
        assert!(spinner_pressure_eval(f32::NAN, 0.0, 0.0, 0.0, 1.0).is_nan());
    }
}
