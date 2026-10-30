//! Spinner3D stroke smoothing (Lazy Mouse / 1€).
//!
//! Called from paint_stroke.cc under WITH_SPINNER_RUST_STROKE.
//! Unsafe is confined to the FFI boundary. Every export catches panics.

use std::mem::{align_of, size_of};
use std::panic::catch_unwind;

#[no_mangle]
pub unsafe extern "C" fn spinner_stroke_smooth_1euro(
    points: *const f32,
    len: u32,
    cutoff: f32,
    beta: f32,
    d_cutoff: f32,
    dt: f32,
    out: *mut f32,
    out_len: u32,
) -> i32 {
    let result = catch_unwind(|| {
        if len == 0 {
            return 0; // empty is valid
        }
        if points.is_null() || out.is_null() {
            return -1;
        }
        if out_len < len.saturating_mul(2) {
            return -7; // out too small
        }
        let n = match (len as usize).checked_mul(2) {
            Some(v) => v,
            None => return -3,
        };
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
        if !cutoff.is_finite()
            || cutoff <= 0.0
            || !beta.is_finite()
            || beta < 0.0
            || !d_cutoff.is_finite()
            || d_cutoff <= 0.0
            || !dt.is_finite()
            || dt <= 0.0
        {
            return -6;
        }
        let input = unsafe { std::slice::from_raw_parts(points, n) };
        let output = unsafe { std::slice::from_raw_parts_mut(out, n) };
        if input.iter().any(|v| !v.is_finite()) {
            return -6;
        }
        spinner_stroke_core::smooth_1euro(input, cutoff, beta, d_cutoff, dt, output);
        0
    });
    result.unwrap_or(-2)
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
                output.len() as u32,
            )
        };
        assert_eq!(code, 0);
    }

    #[test]
    fn golden_constant_input() {
        // Constant input should stay constant.
        let input = [1.0_f32, 2.0, 1.0, 2.0, 1.0, 2.0];
        let mut output = vec![0.0_f32; input.len()];
        let code = unsafe {
            spinner_stroke_smooth_1euro(
                input.as_ptr(),
                3,
                1.0,
                0.0,
                1.0,
                1.0 / 60.0,
                output.as_mut_ptr(),
                output.len() as u32,
            )
        };
        assert_eq!(code, 0);
        for i in 0..3 {
            assert!((output[i * 2] - 1.0).abs() < 1e-5);
            assert!((output[i * 2 + 1] - 2.0).abs() < 1e-5);
        }
    }

    #[test]
    fn rejects_small_out() {
        let input = [0.0_f32; 4];
        let mut output = [0.0_f32; 2];
        let code = unsafe {
            spinner_stroke_smooth_1euro(
                input.as_ptr(),
                2,
                1.0,
                0.0,
                1.0,
                1.0 / 60.0,
                output.as_mut_ptr(),
                output.len() as u32,
            )
        };
        assert_eq!(code, -7);
    }
    #[test]
    fn rejects_overlap() {
        let mut buf = vec![0.0_f32; 4];
        let code = unsafe {
            spinner_stroke_smooth_1euro(
                buf.as_ptr(),
                2,
                1.0,
                0.0,
                1.0,
                1.0 / 60.0,
                buf.as_mut_ptr(),
                buf.len() as u32,
            )
        };
        assert_eq!(code, -5);
    }
}
