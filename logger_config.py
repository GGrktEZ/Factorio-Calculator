"""
Compatibility shim: expose `LoggerSetup` from the new package location.
Prefer importing from `factorio_calc.logger_config` directly.
"""
from factorio_calc.logger_config import LoggerSetup

__all__ = ["LoggerSetup"]
