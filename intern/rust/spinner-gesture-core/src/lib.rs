//! Safe gesture classification core.
#![forbid(unsafe_code)]

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum GestureKind {
    None = 0,
    Tap = 1,
    Drag = 2,
}

/// Classify a gesture. Tap is returned only when `pressed == false` (release).
#[allow(clippy::result_unit_err)]
pub fn classify(
    pressed: bool,
    moved_px: f32,
    time_ms: f32,
    drag_threshold_px: f32,
    tap_timeout_ms: f32,
) -> Result<GestureKind, ()> {
    if !moved_px.is_finite() || !time_ms.is_finite() {
        return Err(());
    }
    if moved_px >= drag_threshold_px {
        Ok(GestureKind::Drag)
    } else if !pressed && time_ms < tap_timeout_ms {
        Ok(GestureKind::Tap)
    } else {
        Ok(GestureKind::None)
    }
}
