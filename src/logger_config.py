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
        """Initialize the logger with file and optional console output.
        
        Sets up a logger that writes to factorio_calculator.log in the project root
        and optionally to console. Ignored external log_dir to prevent output 
        directory pollution. Should only be called once.
        
        Args:
            log_dir: Deprecated. Log file always written to project root.
            enable_console: Whether to enable console output. If None, uses settings.LOG_CONSOLE.
            
        Returns:
            Configured logging.Logger instance.
            
        Logs:
            Info: Logger initialization completion and console status.
            Debug: Log file path.
        """
        if cls._logger is not None:
            return cls._logger

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
        """Get the configured logger instance.
        
        Returns the logger, initializing it if not yet initialized.
        
        Returns:
            The FactorioCalculator logger.
        """
        if cls._logger is None:
            return cls.initialize()
        return cls._logger

    @classmethod
    def get_log_file(cls) -> Optional[str]:
        """Get the path to the log file.
        
        Returns:
            The absolute path to factorio_calculator.log, or None if not initialized.
        """
        return cls._log_file
