//! CLI that builds and validates the `Spinner3D` brush pack / shelf JSON.
//!
//! Usage: spinner-assets <manifest.json>
//! Exits 0 on success, non-zero on validation failure.

use std::env;
use std::fs;
use std::path::Path;
use std::process::ExitCode;

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("usage: spinner-assets <manifest.json>");
        return ExitCode::from(2);
    }
    match validate(Path::new(&args[1])) {
        Ok(()) => ExitCode::from(0),
        Err(e) => {
            eprintln!("validation failed: {e}");
            ExitCode::from(1)
        }
    }
}

fn validate(path: &Path) -> Result<(), String> {
    let meta = fs::metadata(path).map_err(|e| e.to_string())?;
    if meta.len() > 16 * 1024 * 1024 {
        return Err("file too large".into());
    }
    let text = fs::read_to_string(path).map_err(|e| e.to_string())?;
    let v: serde_json::Value = serde_json::from_str(&text).map_err(|e| e.to_string())?;
    match v.get("brushes") {
        Some(serde_json::Value::Array(_)) => Ok(()),
        Some(_) => Err("brushes must be an array".into()),
        None => Err("missing brushes key".into()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    #[test]
    fn rejects_missing_key() {
        let mut f = tempfile::NamedTempFile::new().unwrap();
        write!(f, r#"{{"other":[]}}"#).unwrap();
        assert!(validate(f.path()).is_err());
    }

    #[test]
    fn accepts_valid() {
        let mut f = tempfile::NamedTempFile::new().unwrap();
        write!(f, r#"{{"brushes":[{{"name":"Move"}}]}}"#).unwrap();
        assert!(validate(f.path()).is_ok());
    }
}
