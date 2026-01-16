"""Utility functions shared across modules."""
from __future__ import annotations

def format_name(name: str) -> str:
    """Format a machine/recipe/item name for display.
    
    Converts underscore-separated names to title case words.
    Example: 'transport_belt' -> 'Transport Belt'
    
    Args:
        name: The name to format (usually underscore_separated).
        
    Returns:
        Title-cased display name.
    """
    return name.replace('_', ' ').title()
