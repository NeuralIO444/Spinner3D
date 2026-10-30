#ifndef SPINNER_GESTURE_H
#define SPINNER_GESTURE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

int32_t spinner_gesture_classify(bool pressed, float moved_px, float time_ms, float drag_threshold_px, float tap_timeout_ms);

#ifdef __cplusplus
}
#endif

#endif
