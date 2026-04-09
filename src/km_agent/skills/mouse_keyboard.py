"""Mouse and Keyboard control skills using pyautogui."""

import logging
import time
from typing import Any, Dict, List

import pyautogui

from .base import BaseSkill, SkillResult

logger = logging.getLogger(__name__)

# Configure pyautogui for safety and speed
pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
pyautogui.PAUSE = 0.1  # Small pause between actions


class ClickSkill(BaseSkill):
    """Skill to perform mouse clicks at specific coordinates."""

    name = "click"
    description = "Click at specific screen coordinates."

    def execute(self, x: int, y: int, button: str = "left", clicks: int = 1) -> SkillResult:
        """Execute a click action.

        Args:
            x: X coordinate on the screen.
            y: Y coordinate on the screen.
            button: Mouse button ('left', 'right', 'middle'). Defaults to 'left'.
            clicks: Number of clicks. Defaults to 1.

        Returns:
            SkillResult indicating success or failure.
        """
        try:
            logger.info(f"Clicking at ({x}, {y}) with {button} button, {clicks} times.")
            pyautogui.click(x=x, y=y, clicks=clicks, interval=0.1, button=button)
            return SkillResult(success=True, message=f"Clicked at ({x}, {y})")
        except Exception as e:
            logger.error(f"Click failed: {e}")
            return SkillResult(success=False, message=f"Click failed: {str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "x", "type": "int", "description": "X coordinate"},
            {"name": "y", "type": "int", "description": "Y coordinate"},
            {"name": "button", "type": "str", "description": "Mouse button (left/right/middle)"},
            {"name": "clicks", "type": "int", "description": "Number of clicks"},
        ]


class DoubleClickSkill(BaseSkill):
    """Skill to perform double clicks."""

    name = "double_click"
    description = "Double click at specific coordinates."

    def execute(self, x: int, y: int) -> SkillResult:
        """Execute a double click."""
        try:
            logger.info(f"Double clicking at ({x}, {y}).")
            pyautogui.doubleClick(x=x, y=y)
            return SkillResult(success=True, message=f"Double clicked at ({x}, {y})")
        except Exception as e:
            logger.error(f"Double click failed: {e}")
            return SkillResult(success=False, message=f"Double click failed: {str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "x", "type": "int", "description": "X coordinate"},
            {"name": "y", "type": "int", "description": "Y coordinate"},
        ]


class RightClickSkill(BaseSkill):
    """Skill to perform right clicks."""

    name = "right_click"
    description = "Right click at specific coordinates."

    def execute(self, x: int, y: int) -> SkillResult:
        """Execute a right click."""
        try:
            logger.info(f"Right clicking at ({x}, {y}).")
            pyautogui.rightClick(x=x, y=y)
            return SkillResult(success=True, message=f"Right clicked at ({x}, {y})")
        except Exception as e:
            logger.error(f"Right click failed: {e}")
            return SkillResult(success=False, message=f"Right click failed: {str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "x", "type": "int", "description": "X coordinate"},
            {"name": "y", "type": "int", "description": "Y coordinate"},
        ]


class TypeTextSkill(BaseSkill):
    """Skill to type text into the active window."""

    name = "type_text"
    description = "Type the given text into the active window."

    def execute(self, text: str, interval: float = 0.05) -> SkillResult:
        """Execute text typing.

        Args:
            text: The text to type.
            interval: Time between keystrokes in seconds.

        Returns:
            SkillResult indicating success or failure.
        """
        try:
            logger.info(f"Typing text: {text[:50]}...")
            pyautogui.write(text, interval=interval)
            return SkillResult(success=True, message=f"Typed text successfully")
        except Exception as e:
            logger.error(f"Type text failed: {e}")
            return SkillResult(success=False, message=f"Type text failed: {str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "text", "type": "str", "description": "Text to type"},
            {"name": "interval", "type": "float", "description": "Interval between keystrokes"},
        ]


class PressHotkeySkill(BaseSkill):
    """Skill to press keyboard hotkeys."""

    name = "press_hotkey"
    description = "Press a combination of keys."

    def execute(self, keys: List[str]) -> SkillResult:
        """Execute hotkey press.

        Args:
            keys: List of key names (e.g., ['ctrl', 'c']).

        Returns:
            SkillResult indicating success or failure.
        """
        try:
            logger.info(f"Pressing hotkey: {keys}")
            pyautogui.hotkey(*keys)
            return SkillResult(success=True, message=f"Pressed hotkey: {'+'.join(keys)}")
        except Exception as e:
            logger.error(f"Hotkey press failed: {e}")
            return SkillResult(success=False, message=f"Hotkey press failed: {str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "keys", "type": "list", "description": "List of keys to press"}
        ]


class DragSkill(BaseSkill):
    """Skill to drag mouse from one point to another."""

    name = "drag"
    description = "Drag from start to end coordinates."

    def execute(
        self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5
    ) -> SkillResult:
        """Execute drag action.

        Args:
            start_x: Start X coordinate.
            start_y: Start Y coordinate.
            end_x: End X coordinate.
            end_y: End Y coordinate.
            duration: Duration of the drag in seconds.

        Returns:
            SkillResult indicating success or failure.
        """
        try:
            logger.info(f"Dragging from ({start_x}, {start_y}) to ({end_x}, {end_y})")
            pyautogui.moveTo(start_x, start_y)
            pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration)
            return SkillResult(success=True, message="Drag completed")
        except Exception as e:
            logger.error(f"Drag failed: {e}")
            return SkillResult(success=False, message=f"Drag failed: {str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "start_x", "type": "int", "description": "Start X coordinate"},
            {"name": "start_y", "type": "int", "description": "Start Y coordinate"},
            {"name": "end_x", "type": "int", "description": "End X coordinate"},
            {"name": "end_y", "type": "int", "description": "End Y coordinate"},
            {"name": "duration", "type": "float", "description": "Duration in seconds"},
        ]


class ScrollSkill(BaseSkill):
    """Skill to scroll the mouse wheel."""

    name = "scroll"
    description = "Scroll the mouse wheel."

    def execute(self, clicks: int, x: int = None, y: int = None) -> SkillResult:
        """Execute scroll action.

        Args:
            clicks: Number of clicks to scroll (positive for up, negative for down).
            x: Optional X coordinate to move to before scrolling.
            y: Optional Y coordinate to move to before scrolling.

        Returns:
            SkillResult indicating success or failure.
        """
        try:
            if x is not None and y is not None:
                pyautogui.moveTo(x, y)
            logger.info(f"Scrolling {clicks} clicks at ({x}, {y})")
            pyautogui.scroll(clicks)
            return SkillResult(success=True, message=f"Scrolled {clicks} clicks")
        except Exception as e:
            logger.error(f"Scroll failed: {e}")
            return SkillResult(success=False, message=f"Scroll failed: {str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "clicks", "type": "int", "description": "Number of scroll clicks"},
            {"name": "x", "type": "int", "description": "Optional X coordinate"},
            {"name": "y", "type": "int", "description": "Optional Y coordinate"},
        ]
