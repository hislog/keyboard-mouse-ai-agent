"""Utility functions for logging, configuration, and helpers."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    format_string: Optional[str] = None,
) -> None:
    """Configure logging for the application.

    Args:
        level: Logging level (e.g., logging.DEBUG, logging.INFO).
        log_file: Optional path to log file. If None, logs to console only.
        format_string: Custom format string. Uses default if None.
    """
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    # Create formatter
    formatter = logging.Formatter(format_string)

    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    logging.info(f"Logging configured: level={logging.getLevelName(level)}, file={log_file}")


def get_resource_path(relative_path: str) -> Path:
    """Get absolute path to resource, works for dev and PyInstaller bundle.

    This is critical for PyInstaller single-file executables where resources
    are extracted to a temporary folder.

    Args:
        relative_path: Relative path to the resource from project root.

    Returns:
        Absolute Path object to the resource.
    """
    # Check if running in PyInstaller bundle
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = Path(sys.executable).parent
    else:
        # Running in normal Python environment
        base_path = Path(__file__).parent.parent.parent

    return base_path / relative_path


class Config:
    """Application configuration management."""

    # Default hotkey to trigger dialog (Ctrl+Alt+A)
    DEFAULT_HOTKEY = "ctrl+alt+a"
    
    # AI Configuration
    DEFAULT_AI_MODEL = "gpt-4o"
    DEFAULT_AI_TEMPERATURE = 0.1
    
    # Skill execution settings
    SKILL_EXECUTION_DELAY = 0.5  # seconds between skills
    
    # GUI settings
    DIALOG_WIDTH = 500
    DIALOG_HEIGHT = 180
    
    @classmethod
    def get_hotkey(cls) -> str:
        """Get the configured hotkey."""
        import os
        return os.getenv("KM_AGENT_HOTKEY", cls.DEFAULT_HOTKEY)
    
    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """Get the AI API key from environment."""
        import os
        return os.getenv("OPENAI_API_KEY")
    
    @classmethod
    def get_api_base_url(cls) -> str:
        """Get the AI API base URL from environment."""
        import os
        return os.getenv("KM_AGENT_API_BASE_URL", "https://api.openai.com/v1")
