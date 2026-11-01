# SPDX-License-Identifier: GPL-3.0-or-later
"""Standalone test for the brush recipe loader."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from spinner.brush_recipes import load_sfbrush, RecipeError


def main() -> int:
    sample = Path(__file__).parent / "samples" / "snake_scales.sfbrush"
    recipe = load_sfbrush(sample)
    assert recipe.name == "Snake Scales"
    assert recipe.pattern == "scales"
    assert recipe.depth == 0.35
    assert recipe.hardness == 0.55
    print(f"ok: {recipe.name} pattern={recipe.pattern} depth={recipe.depth}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
