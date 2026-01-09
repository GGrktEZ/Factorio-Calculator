"""
Logging configuration module.
Centralizes all logging setup with support for file and console output.
"""
from __future__ import annotations
import logging
import os
import sys
from typing import Optional
import settings


class LoggerSetup:
    """Manages logger configuration for the application."""

    _logger: Optional[logging.Logger] = None
    _log_file: Optional[str] = None

    @classmethod
    def initialize(cls, log_dir: Optional[str] = None, enable_console: Optional[bool] = None) -> logging.Logger:
        if cls._logger is not None:
            return cls._logger

        # Always write logs to project root (./factorio_calculator.log)
        # Ignore any external log_dir that may point to the calculation output folder
        log_directory = str(settings.ROOT_DIR)
        os.makedirs(log_directory, exist_ok=True)

        logger = logging.getLogger('FactorioCalculator')
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        cls._log_file = os.path.join(log_directory, 'factorio_calculator.log')
        file_handler = logging.FileHandler(cls._log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_enabled = settings.LOG_CONSOLE if enable_console is None else enable_console
        if console_enabled:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            if hasattr(console_handler.stream, 'reconfigure'):
                try:
                    console_handler.stream.reconfigure(encoding='utf-8')
                except Exception:
                    pass
            logger.addHandler(console_handler)

        cls._logger = logger
        logger.info("Logger initialized successfully")
        if console_enabled:
            logger.info("Console logging enabled")
        logger.debug(f"Log file: {cls._log_file}")

        return logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger is None:
            return cls.initialize()
        return cls._logger

    @classmethod
    def get_log_file(cls) -> Optional[str]:
        return cls._log_file
