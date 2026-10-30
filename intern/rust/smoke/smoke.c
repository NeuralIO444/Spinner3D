/* SPDX-License-Identifier: GPL-3.0-or-later */
/* Minimal C smoke test that links the Rust FFI exports. */

#include <stdio.h>
#include <stdint.h>

/* Declarations matching the generated headers. */
extern uint32_t spinner_stroke_abi_version(void);
extern int32_t spinner_gesture_classify(uint8_t pressed, float moved_px, float time_ms,
                                        float drag_threshold_px, float tap_timeout_ms);
extern float spinner_pressure_eval(float t, float p0, float p1, float p2, float p3);

int main(void) {
    uint32_t ver = spinner_stroke_abi_version();
    printf("abi_version=%u\n", ver);
    if (ver != 2) {
        fprintf(stderr, "unexpected abi version\n");
        return 1;
    }

    int32_t g = spinner_gesture_classify(0, 2.0f, 50.0f, 8.0f, 200.0f);
    printf("gesture=%d\n", g);

    float p = spinner_pressure_eval(0.5f, 0.0f, 0.3f, 0.7f, 1.0f);
    printf("pressure=%f\n", p);

    printf("smoke ok\n");
    return 0;
}
