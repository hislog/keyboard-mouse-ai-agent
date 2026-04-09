"""Screen analysis skills: OCR, Image Recognition, Window Info."""

import logging
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image
import pyautogui

# Lazy import for heavy dependencies (only when needed)
_easyocr_reader = None
_cv2 = None
_np = None

from .base import BaseSkill, SkillResult

logger = logging.getLogger(__name__)


def _get_ocr_reader():
    """Lazy load EasyOCR reader to avoid startup delay."""
    global _easyocr_reader
    if _easyocr_reader is None:
        try:
            import easyocr
            # Initialize for English only by default, can be extended
            _easyocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            logger.info("EasyOCR reader initialized.")
        except ImportError:
            logger.error("EasyOCR not installed. Please install with: pip install easyocr")
            raise
    return _easyocr_reader


def _get_cv2():
    """Lazy load cv2."""
    global _cv2
    if _cv2 is None:
        import cv2
        _cv2 = cv2
    return _cv2


def _get_numpy():
    """Lazy load numpy."""
    global _np
    if _np is None:
        import numpy as np
        _np = np
    return _np


class OCRRegionSkill(BaseSkill):
    """Skill to extract text from a specific screen region using OCR."""

    name = "ocr_region"
    description = "Extract text from a screen region."

    def execute(self, x: int, y: int, width: int, height: int, lang: str = "en") -> SkillResult:
        """Execute OCR on a screen region.

        Args:
            x: Top-left X coordinate.
            y: Top-left Y coordinate.
            width: Width of the region.
            height: Height of the region.
            lang: Language code for OCR (default: 'en').

        Returns:
            SkillResult with extracted text in data field.
        """
        try:
            logger.info(f"Performing OCR on region ({x}, {y}, {width}, {height})")
            
            # Capture screen region
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            
            # Lazy load dependencies
            cv2 = _get_cv2()
            np = _get_numpy()
            
            # Convert to OpenCV format for better OCR performance
            image_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Get OCR reader
            reader = _get_ocr_reader()
            
            # Perform OCR
            results = reader.readtext(image_cv)
            
            # Extract text
            texts = [result[1] for result in results]
            full_text = " ".join(texts)
            
            logger.info(f"OCR Result: {full_text[:100]}...")
            return SkillResult(
                success=True, 
                message=f"OCR completed on region", 
                data={"text": full_text, "details": results}
            )
            
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return SkillResult(success=False, message=f"OCR failed: {str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "x", "type": "int", "description": "Top-left X coordinate"},
            {"name": "y", "type": "int", "description": "Top-left Y coordinate"},
            {"name": "width", "type": "int", "description": "Width of region"},
            {"name": "height", "type": "int", "description": "Height of region"},
            {"name": "lang", "type": "str", "description": "Language code"},
        ]


class FindImageOnScreenSkill(BaseSkill):
    """Skill to locate an image on the screen."""

    name = "find_image_on_screen"
    description = "Locate an image on screen and return its coordinates."

    def execute(self, image_path: str, confidence: float = 0.8) -> SkillResult:
        """Find an image on the screen.

        Args:
            image_path: Path to the image file to search for.
            confidence: Confidence threshold for matching (0.0-1.0).

        Returns:
            SkillResult with coordinates (x, y, width, height) in data field.
        """
        try:
            logger.info(f"Searching for image: {image_path} (confidence: {confidence})")
            
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            
            if location:
                x, y, width, height = location
                logger.info(f"Image found at ({x}, {y}) with size {width}x{height}")
                return SkillResult(
                    success=True,
                    message="Image found",
                    data={"x": x, "y": y, "width": width, "height": height, "center_x": x + width//2, "center_y": y + height//2}
                )
            else:
                logger.warning("Image not found on screen")
                return SkillResult(success=False, message="Image not found on screen", data=None)
                
        except Exception as e:
            logger.error(f"Image search failed: {e}")
            return SkillResult(success=False, message=f"Image search failed: {str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "image_path", "type": "str", "description": "Path to the image file"},
            {"name": "confidence", "type": "float", "description": "Confidence threshold"},
        ]


class GetActiveWindowTitleSkill(BaseSkill):
    """Skill to get the title of the currently active window."""

    name = "get_active_window_title"
    description = "Get the title of the currently active window."

    def execute(self) -> SkillResult:
        """Get the active window title.

        Note: This uses pyautogui's underlying OS-specific implementation.
        For Windows, pywin32 provides more robust options, but this is cross-platform.

        Returns:
            SkillResult with window title in data field.
        """
        try:
            # pyautogui doesn't have a direct 'get_active_window_title' method
            # We need to use platform-specific code or pywin32
            # Since this project is Windows-only, we'll use a simple placeholder
            # In a real Windows environment, we'd use win32gui.GetForegroundWindow()
            
            # Placeholder: In actual Windows deployment, replace with win32gui call
            title = "Unknown (win32gui not available in this environment)"
            try:
                import win32gui
                hwnd = win32gui.GetForegroundWindow()
                title = win32gui.GetWindowText(hwnd)
            except (ImportError, AttributeError):
                # win32gui not available (e.g., running on Linux for testing)
                pass
            
            logger.info(f"Active window title: {title}")
            return SkillResult(success=True, message="Retrieved active window title", data={"title": title})
            
        except Exception as e:
            logger.error(f"Failed to get window title: {e}")
            return SkillResult(success=False, message=f"Failed to get window title: {str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return []  # No parameters needed


class GetScreenSizeSkill(BaseSkill):
    """Skill to get the current screen resolution."""

    name = "get_screen_size"
    description = "Get the current screen resolution."

    def execute(self) -> SkillResult:
        """Get screen size."""
        try:
            width, height = pyautogui.size()
            logger.info(f"Screen size: {width}x{height}")
            return SkillResult(
                success=True,
                message="Retrieved screen size",
                data={"width": width, "height": height}
            )
        except Exception as e:
            logger.error(f"Failed to get screen size: {e}")
            return SkillResult(success=False, message=f"Failed to get screen size: {str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return []
