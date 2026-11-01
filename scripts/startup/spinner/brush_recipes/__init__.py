# SPDX-License-Identifier: GPL-3.0-or-later
"""Spinner3D brush recipe loader.

Adapted from SculptForge's BrushRecipe (GPL-3).
See docs/brushes.md in islandmed/SculptForge for the .sfbrush schema.
"""

from .recipe import BrushRecipe, load_sfbrush, RecipeError

__all__ = ["BrushRecipe", "load_sfbrush", "RecipeError"]
