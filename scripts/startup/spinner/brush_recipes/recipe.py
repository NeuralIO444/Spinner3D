# SPDX-License-Identifier: GPL-3.0-or-later
"""Data-driven brush recipe (.sfbrush).

Adapted from SculptForge src/core/BrushRecipe.h (GPL-3).
Recipes are data only; no executable code is loaded.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class RecipeError(ValueError):
    """Raised when a .sfbrush file is invalid."""


DIRECTIONS = ("normal", "inflate", "view", "stroke")
PLANES = ("none", "clay", "flatten", "fill", "scrape")
PATTERNS = ("none", "noise", "scales", "ridges", "pores", "cracks")


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


@dataclass
class BrushRecipe:
    name: str = "Custom Brush"
    description: str = ""
    direction: str = "normal"
    depth: float = 0.5
    plane: str = "none"
    plane_amount: float = 0.5
    pinch: float = 0.0
    drag: float = 0.0
    smooth: float = 0.0
    hardness: float = 0.5
    tip_sharpness: float = 0.0
    pattern: str = "none"
    pattern_scale: float = 0.2
    pattern_amount: float = 0.0
    spacing: float = 0.25
    jitter: float = 0.0
    pressure_curve: float = 1.0
    front_faces_only: bool = False
    cavity_mask: float = 0.0
    source: str = "session"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "direction": self.direction,
            "depth": self.depth,
            "plane": self.plane,
            "planeAmount": self.plane_amount,
            "pinch": self.pinch,
            "drag": self.drag,
            "smooth": self.smooth,
            "hardness": self.hardness,
            "tipSharpness": self.tip_sharpness,
            "pattern": self.pattern,
            "patternScale": self.pattern_scale,
            "patternAmount": self.pattern_amount,
            "spacing": self.spacing,
            "jitter": self.jitter,
            "pressureCurve": self.pressure_curve,
            "frontFacesOnly": self.front_faces_only,
            "cavityMask": self.cavity_mask,
            "format": "sfbrush",
            "version": 1,
        }


def load_sfbrush(path: str | Path) -> BrushRecipe:
    """Load and validate a .sfbrush JSON file. Unknown keys are ignored."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RecipeError(f"invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise RecipeError("root must be an object")
    if data.get("format") not in (None, "sfbrush"):
        raise RecipeError(f"unsupported format: {data.get('format')}")

    recipe = BrushRecipe()
    recipe.name = str(data.get("name", recipe.name))
    recipe.description = str(data.get("description", ""))
    recipe.direction = str(data.get("direction", recipe.direction))
    if recipe.direction not in DIRECTIONS:
        recipe.direction = "normal"
    recipe.depth = _clamp(float(data.get("depth", recipe.depth)), -1.0, 1.0)
    recipe.plane = str(data.get("plane", recipe.plane))
    if recipe.plane not in PLANES:
        recipe.plane = "none"
    recipe.plane_amount = _clamp(float(data.get("planeAmount", recipe.plane_amount)), 0.0, 1.0)
    recipe.pinch = _clamp(float(data.get("pinch", recipe.pinch)), -1.0, 1.0)
    recipe.drag = _clamp(float(data.get("drag", recipe.drag)), 0.0, 1.0)
    recipe.smooth = _clamp(float(data.get("smooth", recipe.smooth)), 0.0, 1.0)
    recipe.hardness = _clamp(float(data.get("hardness", recipe.hardness)), 0.0, 1.0)
    recipe.tip_sharpness = _clamp(float(data.get("tipSharpness", recipe.tip_sharpness)), 0.0, 1.0)
    recipe.pattern = str(data.get("pattern", recipe.pattern))
    if recipe.pattern not in PATTERNS:
        recipe.pattern = "none"
    recipe.pattern_scale = _clamp(float(data.get("patternScale", recipe.pattern_scale)), 0.03, 2.0)
    recipe.pattern_amount = _clamp(float(data.get("patternAmount", recipe.pattern_amount)), 0.0, 1.0)
    recipe.spacing = _clamp(float(data.get("spacing", recipe.spacing)), 0.02, 2.0)
    recipe.jitter = _clamp(float(data.get("jitter", recipe.jitter)), 0.0, 1.0)
    recipe.pressure_curve = _clamp(float(data.get("pressureCurve", recipe.pressure_curve)), 0.3, 3.0)
    recipe.front_faces_only = bool(data.get("frontFacesOnly", False))
    recipe.cavity_mask = _clamp(float(data.get("cavityMask", recipe.cavity_mask)), -1.0, 1.0)
    return recipe
