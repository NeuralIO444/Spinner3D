# SPDX-FileCopyrightText: 2026 Spinner3D Authors
# SPDX-License-Identifier: GPL-3.0-or-later

# Spinner3D Rust integration via Corrosion.
# Enabled by WITH_SPINNER_RUST. Defaults OFF so upstream merges stay clean.

if(NOT WITH_SPINNER_RUST)
  return()
endif()

include(FetchContent)

FetchContent_Declare(
  Corrosion
  GIT_REPOSITORY https://github.com/corrosion-rs/corrosion.git
  GIT_TAG v0.6.1
  GIT_SHALLOW TRUE
)

# Prevent Corrosion from overriding the C/C++ compiler selection.
set(Rust_TOOLCHAIN stable CACHE STRING "" FORCE)

FetchContent_MakeAvailable(Corrosion)

corrosion_import_crate(
  MANIFEST_PATH "${CMAKE_SOURCE_DIR}/intern/rust/Cargo.toml"
  CRATES spinner-hello spinner-stroke
  PROFILE release
)

if(WITH_SPINNER_RUST_STROKE)
  target_compile_definitions(bf_editor_sculpt_paint PRIVATE WITH_SPINNER_RUST_STROKE)
  target_link_libraries(bf_editor_sculpt_paint PRIVATE spinner-stroke)
  target_include_directories(bf_editor_sculpt_paint PRIVATE
    "${CMAKE_SOURCE_DIR}/intern/rust/spinner-stroke/include")
endif()

# Optional: generate the C header in CI. For local builds the header is
# checked in under intern/rust/spinner-hello/include/spinner_hello.h.
