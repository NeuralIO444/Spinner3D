//! Spinner3D hello crate — proves the Rust build system.
//!
//! All unsafe is confined to the FFI boundary. Every exported function
//! catches panics and returns an error code.

use std::panic::catch_unwind;

/// Return a constant magic number so C++ can verify linkage.
///
/// # Safety
/// This function is safe to call from C. It never panics under normal
/// conditions; any panic is caught and converted to an error code.
#[no_mangle]
pub extern "C" fn spinner_hello() -> i32 {
    catch_unwind(|| 0x5350_494E).unwrap_or(-1)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hello_returns_magic() {
        assert_eq!(spinner_hello(), 0x5350_494E);
    }
}
