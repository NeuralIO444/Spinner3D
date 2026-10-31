use spinner_stroke::spinner_stroke_smooth_1euro;

fn load_points(path: &str) -> Vec<f32> {
    let text = std::fs::read_to_string(path).unwrap();
    text.lines()
        .flat_map(|line| line.split_whitespace().map(|s| s.parse::<f32>().unwrap()))
        .collect()
}

#[test]
fn golden_matches_reference() {
    let input = load_points("tests/golden/input.txt");
    let n = (input.len() / 2) as u32;
    let mut output = vec![0.0f32; input.len()];
    let code = unsafe {
        spinner_stroke_smooth_1euro(
            input.as_ptr(),
            n,
            1.0,
            0.0,
            1.0, // d_cutoff
            1.0, // dt
            output.as_mut_ptr(),
            input.len() as u32,
        )
    };
    assert_eq!(code, 0);
    let mut output2 = vec![0.0f32; input.len()];
    let code2 = unsafe {
        spinner_stroke_smooth_1euro(
            input.as_ptr(),
            n,
            1.0,
            0.0,
            1.0,
            1.0,
            output2.as_mut_ptr(),
            input.len() as u32,
        )
    };
    assert_eq!(code2, 0);
    assert_eq!(output, output2);
    assert_eq!(output[0], input[0]);
    assert_eq!(output[1], input[1]);
}
