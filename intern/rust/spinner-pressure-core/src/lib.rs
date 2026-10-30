//! Safe pressure curve evaluation core.
#![forbid(unsafe_code)]

/// Evaluate a cubic Bezier pressure curve. Returns NaN on non-finite input.
pub fn eval(t: f32, p0: f32, p1: f32, p2: f32, p3: f32) -> f32 {
    if !t.is_finite() || ![p0, p1, p2, p3].iter().all(|v| v.is_finite()) {
        return f32::NAN;
    }
    let t = t.clamp(0.0, 1.0);
    let u = 1.0 - t;
    let v = u * u * u * p0 + 3.0 * u * u * t * p1 + 3.0 * u * t * t * p2 + t * t * t * p3;
    v.clamp(0.0, 1.0)
}
