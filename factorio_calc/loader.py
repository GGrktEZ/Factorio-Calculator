"""
Data loading module for reading JSON configuration files.
Handles loading base.json (game data) and Config.json (user configuration),
with filenames configurable via environment (.env).
"""
from __future__ import annotations
import json
import os
import logging
from typing import Dict, Any
from .models import FactorioData
from . import settings

logger = logging.getLogger('FactorioCalculator')


class DataLoader:
    """Handles loading and parsing JSON configuration files."""

    def __init__(self, directory: str):
        self.directory = directory
        logger.debug(f"DataLoader initialized with directory: {directory}")

    def load_file(self, filename: str) -> Dict[str, Any]:
        file_path = os.path.join(self.directory, filename)
        logger.debug(f"Loading JSON file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Successfully loaded {filename}")
            return data
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filename}: {e.msg}")
            raise json.JSONDecodeError(
                f"Invalid JSON in {filename}: {e.msg}",
                e.doc,
                e.pos
            )

    def load_base_data(self) -> FactorioData:
        """
        Load the base game data from base.json.

        Returns:
            FactorioData object containing all game data
        """
        logger.info("Loading base game data")
        raw_data = self.load_file(settings.BASE_JSON)
        factorio_data = FactorioData.from_dict(raw_data)
        logger.info(f"Loaded {len(factorio_data.recipes)} recipes, "
                    f"{len(factorio_data.machines)} machines, "
                    f"{len(factorio_data.modules)} modules")
        return factorio_data

    def load_config(self) -> Dict[str, Any]:
        logger.info("Loading user configuration")
        config = self.load_file(settings.CONFIG_JSON)
        logger.debug(f"Configuration loaded: belt_color={config.get('belt_color')}, "
                     f"product={config.get('product')}, "
                     f"verbose={config.get('verbose')}, "
                     f"consoleLogging={config.get('consoleLogging')}")
        return config

    @staticmethod
    def get_current_directory() -> str:
        # Always resolve to project root so data files live at repository root
        return str(settings.ROOT_DIR)
