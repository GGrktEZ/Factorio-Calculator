"""Utility functions shared across modules."""
from __future__ import annotations

def format_name(name: str) -> str:
    """Format a machine/recipe name for display."""
    return name.replace('_', ' ').title()
