use criterion::{black_box, criterion_group, criterion_main, Criterion};
use spinner_stroke::spinner_stroke_smooth_1euro;

fn bench_1euro(c: &mut Criterion) {
    let n = 1024u32;
    let mut input = vec![0.0f32; (n * 2) as usize];
    for i in 0..n as usize {
        input[i * 2] = i as f32;
        input[i * 2 + 1] = ((i % 7) as f32) * 0.01;
    }
    let mut output = vec![0.0f32; input.len()];
    c.bench_function("1euro_1024", |b| {
        b.iter(|| unsafe {
            spinner_stroke_smooth_1euro(
                black_box(input.as_ptr()),
                black_box(n),
                black_box(1.0),
                black_box(0.0),
                black_box(1.0),
                black_box(1.0),
                black_box(output.as_mut_ptr()),
                black_box(n * 2),
            )
        })
    });
}

criterion_group!(benches, bench_1euro);
criterion_main!(benches);
