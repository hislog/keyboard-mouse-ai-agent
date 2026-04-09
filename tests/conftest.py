"""Configuration and environment setup for pytest."""

import sys
import os
from pathlib import Path
from unittest.mock import MagicMock

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Mock X11 display for headless environments (Linux CI/CD)
# This must be done BEFORE importing pyautogui
if os.name != 'nt' and 'DISPLAY' not in os.environ:
    # Create a mock DISPLAY variable for pyautogui
    os.environ['DISPLAY'] = ':0.0'
    
    # Try to set up a virtual framebuffer if available
    try:
        # Attempt to use xvfb-run if available (for actual GUI tests)
        pass
    except Exception:
        pass

# Pytest configuration
pytest_plugins = []

def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "gui: marks tests that require GUI (skip in headless environments)"
    )
