//! Safe 1€ stroke smoothing core.
#![forbid(unsafe_code)]

/// Smooth interleaved [x, y, x, y, ...] points.
/// `dt` is the time step in seconds. `d_cutoff` is the derivative cutoff.
pub fn smooth_1euro(
    input: &[f32],
    cutoff: f32,
    beta: f32,
    d_cutoff: f32,
    dt: f32,
    output: &mut [f32],
) {
    if input.is_empty() || output.len() < input.len() {
        return;
    }
    let mut prev_x = input[0];
    let mut prev_y = input[1];
    let mut prev_dx = 0.0_f32;
    let mut prev_dy = 0.0_f32;
    output[0] = prev_x;
    output[1] = prev_y;
    let _a_base = alpha(dt, cutoff);
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
    fn golden_constant() {
        let input = vec![1.0_f32, 2.0, 1.0, 2.0, 1.0, 2.0];
        let mut output = vec![0.0_f32; input.len()];
        smooth_1euro(&input, 1.0, 0.0, 1.0, 1.0 / 60.0, &mut output);
        for i in 0..3 {
            assert!(
                (output[i * 2] - 1.0).abs() < 1e-5,
                "x[{}]={}",
                i,
                output[i * 2]
            );
            assert!(
                (output[i * 2 + 1] - 2.0).abs() < 1e-5,
                "y[{}]={}",
                i,
                output[i * 2 + 1]
            );
        }
    }

    #[test]
    fn golden_step_response() {
        // Step from 0 to 1 should approach 1 monotonically.
        let input = vec![0.0_f32, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0];
        let mut output = vec![0.0_f32; input.len()];
        smooth_1euro(&input, 1.0, 0.0, 1.0, 1.0 / 60.0, &mut output);
        assert!(output[2] > 0.0 && output[2] < 1.0);
        assert!(output[4] >= output[2]);
        assert!(output[6] >= output[4]);
    }
}
