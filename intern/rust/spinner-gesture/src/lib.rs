//! Ctrl/Alt tap-versus-drag classification for Spinner3D.
use std::panic::catch_unwind;

#[repr(C)]
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum GestureKind {
    None = 0,
    Tap = 1,
    Drag = 2,
}

#[no_mangle]
pub extern "C" fn spinner_gesture_classify(
    pressed: u8,
    moved_px: f32,
    time_ms: f32,
    drag_threshold_px: f32,
    tap_timeout_ms: f32,
) -> i32 {
    catch_unwind(|| {
        if !moved_px.is_finite() || !time_ms.is_finite() {
            return -1;
        }
        if moved_px >= drag_threshold_px {
            GestureKind::Drag as i32
        } else if pressed == 0 && time_ms < tap_timeout_ms {
            // Tap only on release
            GestureKind::Tap as i32
        } else {
            GestureKind::None as i32
        }
    })
    .unwrap_or(-1)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn classifies_tap() {
        let k = spinner_gesture_classify(1, 2.0, 80.0, 8.0, 200.0);
        assert_eq!(k, GestureKind::Tap as i32);
    }

    #[test]
    fn classifies_drag() {
        let k = spinner_gesture_classify(1, 20.0, 50.0, 8.0, 200.0);
        assert_eq!(k, GestureKind::Drag as i32);
    }
}
