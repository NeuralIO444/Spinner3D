//! Ctrl/Alt tap-versus-drag classification for Spinner3D.
//!
//! Called from the window/event path under WITH_SPINNER_RUST_GESTURE.

use std::panic::catch_unwind;

#[repr(C)]
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum GestureKind {
    None = 0,
    Tap = 1,
    Drag = 2,
}

#[no_mangle]
pub unsafe extern "C" fn spinner_gesture_classify(
    pressed: bool,
    moved_px: f32,
    time_ms: f32,
    drag_threshold_px: f32,
    tap_timeout_ms: f32,
) -> i32 {
    let result = catch_unwind(|| {
        if !pressed {
            return GestureKind::None as i32;
        }
        if moved_px >= drag_threshold_px {
            GestureKind::Drag as i32
        } else if time_ms < tap_timeout_ms {
            GestureKind::Tap as i32
        } else {
            GestureKind::None as i32
        }
    });
    result.unwrap_or(-1)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn classifies_tap() {
        let k = unsafe { spinner_gesture_classify(true, 2.0, 80.0, 8.0, 200.0) };
        assert_eq!(k, GestureKind::Tap as i32);
    }

    #[test]
    fn classifies_drag() {
        let k = unsafe { spinner_gesture_classify(true, 20.0, 50.0, 8.0, 200.0) };
        assert_eq!(k, GestureKind::Drag as i32);
    }
}
