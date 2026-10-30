#!/bin/sh
# Generate C headers from the FFI crates.
# Requires: cargo install cbindgen
set -e
cd "$(dirname "$0")"
for crate in spinner-stroke spinner-gesture spinner-pressure; do
    cbindgen --config cbindgen.toml --crate "$crate" --output "include/${crate}.h"
done
echo "headers written to include/"
