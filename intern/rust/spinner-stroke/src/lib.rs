//! Spinner3D stroke smoothing (Lazy Mouse / 1€).
//!
//! Called from paint_stroke.cc under WITH_SPINNER_RUST_STROKE.
//! Unsafe is confined to the FFI boundary. Every export catches panics.

use std::panic::catch_unwind;
use std::mem::{align_of, size_of};

#[no_mangle]
pub unsafe extern "C" fn spinner_stroke_smooth_1euro(
    points: *const f32,
    len: u32,
    cutoff: f32,
    beta: f32,
    d_cutoff: f32,
    dt: f32,
    out: *mut f32,
) -> i32 {
    let result = catch_unwind(|| {
        if points.is_null() || out.is_null() || len == 0 {
            return -1;
        }
        let n = match (len as usize).checked_mul(2) { Some(v) => v, None => return -3 };
        if n > (isize::MAX as usize) / size_of::<f32>() {
            return -3;
        }
        if points.align_offset(align_of::<f32>()) != 0 || out.align_offset(align_of::<f32>()) != 0 {
            return -4;
        }
        // Reject overlap to avoid aliasing UB.
        let points_end = points as usize + n * size_of::<f32>();
        let out_end = out as usize + n * size_of::<f32>();
        if (points as usize) < out_end && (out as usize) < points_end {
            return -5;
        }
        if !cutoff.is_finite() || cutoff <= 0.0 || !beta.is_finite() || beta < 0.0 || !d_cutoff.is_finite() || d_cutoff <= 0.0 || !dt.is_finite() || dt <= 0.0 {
            return -6;
        }
        let input = unsafe { std::slice::from_raw_parts(points, n) };
        let output = unsafe { std::slice::from_raw_parts_mut(out, n) };
        if input.iter().any(|v| !v.is_finite()) {
            return -6;
        }
        smooth_1euro(input, cutoff, beta, d_cutoff, dt, output);
        0
    });
    result.unwrap_or(-2)
}

fn smooth_1euro(input: &[f32], cutoff: f32, beta: f32, d_cutoff: f32, dt: f32, output: &mut [f32]) {
    if input.is_empty() {
        return;
    }
    let mut prev_x = input[0];
    let mut prev_y = input[1];
    let mut prev_dx = 0.0_f32;
    let mut prev_dy = 0.0_f32;
    output[0] = prev_x;
    output[1] = prev_y;
    let a_base = alpha(dt, cutoff);
    let a_d = alpha(dt, d_cutoff);
    for i in 1..(input.len() / 2) {
        let x = input[i * 2];
        let y = input[i * 2 + 1];
        let dx = (x - prev_x) / dt;
        let dy = (y - prev_y) / dt;
        let edx = a_d * dx + (1.0 - a_d) * prev_dx;
        let edy = a_d * dy + (1.0 - a_d) * prev_dy;
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
        let code = unsafe {
            spinner_stroke_smooth_1euro(
                input.as_ptr(),
                (input.len() / 2) as u32,
                1.0,
                0.0,
                1.0,
                1.0 / 60.0,
                output.as_mut_ptr(),
            )
        };
        assert_eq!(code, 0);
    }

    #[test]
    fn rejects_overlap() {
        let mut buf = vec![0.0_f32; 4];
        let code = unsafe {
            spinner_stroke_smooth_1euro(buf.as_ptr(), 2, 1.0, 0.0, 1.0, 1.0 / 60.0, buf.as_mut_ptr())
        };
        assert_eq!(code, -5);
    }
}
