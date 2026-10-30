#!/bin/sh
# Build staticlibs and link the C smoke test.
# Run from intern/rust/
set -e
cd "$(dirname "$0")/.."

cargo build --release -p spinner-stroke -p spinner-gesture -p spinner-pressure

cc -o smoke/smoke smoke/smoke.c \
    -L target/release \
    -lspinner_stroke -lspinner_gesture -lspinner_pressure \
    -lpthread -ldl -lm

./smoke/smoke
