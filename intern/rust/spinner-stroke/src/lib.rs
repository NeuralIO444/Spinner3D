//! Spinner3D stroke smoothing (Lazy Mouse / 1€ / Catmull-Rom).
//!
//! Called from paint_stroke.cc under WITH_SPINNER_RUST_STROKE.
//! All unsafe is confined to the FFI boundary. Every exported function
//! catches panics and returns an error code.

use std::panic::catch_unwind;

/// Apply 1€-style exponential smoothing to a 2D point stream.
///
/// # Safety
/// `points` must be a valid array of `len` pairs of f32 (x, y).
/// `out` must have room for `len` pairs.
#[no_mangle]
pub unsafe extern "C" fn spinner_stroke_smooth_1euro(
    points: *const f32,
    len: u32,
    cutoff: f32,
    beta: f32,
    out: *mut f32,
) -> i32 {
    let result = catch_unwind(|| {
        if points.is_null() || out.is_null() || len == 0 {
            return -1;
        }
        // SAFETY: caller guarantees valid non-null pointers and sufficient length.
        let input = unsafe { std::slice::from_raw_parts(points, (len * 2) as usize) };
        let output = unsafe { std::slice::from_raw_parts_mut(out, (len * 2) as usize) };
        smooth_1euro(input, cutoff, beta, output);
        0
    });
    match result {
        Ok(code) => code,
        Err(_) => -2,
    }
}

fn smooth_1euro(input: &[f32], cutoff: f32, beta: f32, output: &mut [f32]) {
    if input.is_empty() {
        return;
    }
    let mut prev_x = input[0];
    let mut prev_y = input[1];
    let mut prev_dx = 0.0_f32;
    let mut prev_dy = 0.0_f32;
    output[0] = prev_x;
    output[1] = prev_y;

    let dt = 1.0_f32;
    for i in 1..(input.len() / 2) {
        let x = input[i * 2];
        let y = input[i * 2 + 1];
        let dx = (x - prev_x) / dt;
        let dy = (y - prev_y) / dt;
        let edx = alpha(dt, cutoff) * dx + (1.0 - alpha(dt, cutoff)) * prev_dx;
        let edy = alpha(dt, cutoff) * dy + (1.0 - alpha(dt, cutoff)) * prev_dy;
        let speed = (edx * edx + edy * edy).sqrt();
        let cutoff_d = cutoff + beta * speed;
        let a = alpha(dt, cutoff_d);
        let sx = a * x + (1.0 - a) * prev_x;
        let sy = a * y + (1.0 - a) * prev_y;
        output[i * 2] = sx;
        output[i * 2 + 1] = sy;
        prev_x = sx;
        prev_y = sy;
        prev_dx = edx;
        prev_dy = edy;
    }
}

fn alpha(dt: f32, cutoff: f32) -> f32 {
    let tau = 1.0 / (2.0 * std::f32::consts::PI * cutoff.max(1e-6));
    1.0 / (1.0 + tau / dt)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn smooth_reduces_jitter() {
        let input = vec![0.0_f32, 0.0, 1.0, 0.1, 2.0, -0.1, 3.0, 0.05, 4.0, 0.0];
        let mut output = vec![0.0_f32; input.len()];
        // SAFETY: pointers are valid for the test duration.
        let code = unsafe {
            spinner_stroke_smooth_1euro(
                input.as_ptr(),
                (input.len() / 2) as u32,
                1.0,
                0.0,
                output.as_mut_ptr(),
            )
        };
        assert_eq!(code, 0);
        let raw_var = variance_y(&input);
        let smooth_var = variance_y(&output);
        assert!(smooth_var <= raw_var);
    }

    fn variance_y(pts: &[f32]) -> f32 {
        let n = pts.len() / 2;
        if n == 0 {
            return 0.0;
        }
        let mean: f32 = pts.iter().skip(1).step_by(2).sum::<f32>() / n as f32;
        pts.iter().skip(1).step_by(2).map(|y| (y - mean).powi(2)).sum::<f32>() / n as f32
    }
}
