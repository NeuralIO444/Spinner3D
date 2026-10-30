//! CLI that builds and validates the Spinner3D brush pack / shelf JSON.
//!
//! Usage: spinner-assets <manifest.json>
//! Exits 0 on success, non-zero on validation failure.

use std::env;
use std::fs;
use std::process::ExitCode;

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("usage: spinner-assets <manifest.json>");
        return ExitCode::from(2);
    }
    match validate(&args[1]) {
        Ok(()) => ExitCode::from(0),
        Err(e) => {
            eprintln!("validation failed: {e}");
            ExitCode::from(1)
        }
    }
}

fn validate(path: &str) -> Result<(), String> {
    let text = fs::read_to_string(path).map_err(|e| e.to_string())?;
    if !text.contains("\"brushes\"") {
        return Err("missing brushes key".into());
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    #[test]
    fn rejects_missing_key() {
        let mut f = tempfile::NamedTempFile::new().unwrap();
        write!(f, r#"{{"other":[]}}"#).unwrap();
        assert!(validate(f.path().to_str().unwrap()).is_err());
    }
}
