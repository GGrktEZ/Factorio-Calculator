"""Compatibility shim for DataLoader.

Expose `DataLoader` from the new package location.
Prefer importing from `factorio_calc.loader` directly.
"""
from factorio_calc.loader import DataLoader

__all__ = ["DataLoader"]
