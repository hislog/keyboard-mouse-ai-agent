"""使用 pyautogui 的鼠标和键盘控制技能。"""

import logging
import time
from typing import Any, Dict, List

import pyautogui

from .base import BaseSkill, SkillResult

logger = logging.getLogger(__name__)

# 配置 pyautogui 以确保安全性和速度
pyautogui.FAILSAFE = True  # 将鼠标移到左上角以中止
pyautogui.PAUSE = 0.1  # 动作之间的小停顿


class ClickSkill(BaseSkill):
    """在特定坐标执行鼠标点击的技能。"""

    name = "click"
    description = "在特定屏幕坐标处点击。"

    def execute(self, x: int, y: int, button: str = "left", clicks: int = 1) -> SkillResult:
        """执行点击动作。

        Args:
            x: 屏幕上的 X 坐标。
            y: 屏幕上的 Y 坐标。
            button: 鼠标按钮（'left', 'right', 'middle'）。默认为 'left'。
            clicks: 点击次数。默认为 1。

        Returns:
            表示成功或失败的 SkillResult。
        """
        try:
            logger.info(f"正在 ({x}, {y}) 处使用 {button} 按钮点击 {clicks} 次。")
            pyautogui.click(x=x, y=y, clicks=clicks, interval=0.1, button=button)
            return SkillResult(success=True, message=f"已在 ({x}, {y}) 处点击")
        except Exception as e:
            logger.error(f"点击失败：{e}")
            return SkillResult(success=False, message=f"点击失败：{str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "x", "type": "int", "description": "X 坐标"},
            {"name": "y", "type": "int", "description": "Y 坐标"},
            {"name": "button", "type": "str", "description": "鼠标按钮 (left/right/middle)"},
            {"name": "clicks", "type": "int", "description": "点击次数"},
        ]


class DoubleClickSkill(BaseSkill):
    """执行双击的技能。"""

    name = "double_click"
    description = "在特定坐标处双击。"

    def execute(self, x: int, y: int) -> SkillResult:
        """执行双击。"""
        try:
            logger.info(f"正在 ({x}, {y}) 处双击。")
            pyautogui.doubleClick(x=x, y=y)
            return SkillResult(success=True, message=f"已在 ({x}, {y}) 处双击")
        except Exception as e:
            logger.error(f"双击失败：{e}")
            return SkillResult(success=False, message=f"双击失败：{str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "x", "type": "int", "description": "X 坐标"},
            {"name": "y", "type": "int", "description": "Y 坐标"},
        ]


class RightClickSkill(BaseSkill):
    """执行右键点击的技能。"""

    name = "right_click"
    description = "在特定坐标处右键点击。"

    def execute(self, x: int, y: int) -> SkillResult:
        """执行右键点击。"""
        try:
            logger.info(f"正在 ({x}, {y}) 处右键点击。")
            pyautogui.rightClick(x=x, y=y)
            return SkillResult(success=True, message=f"已在 ({x}, {y}) 处右键点击")
        except Exception as e:
            logger.error(f"右键点击失败：{e}")
            return SkillResult(success=False, message=f"右键点击失败：{str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "x", "type": "int", "description": "X 坐标"},
            {"name": "y", "type": "int", "description": "Y 坐标"},
        ]


class TypeTextSkill(BaseSkill):
    """将文本输入到活动窗口的技能。"""

    name = "type_text"
    description = "将给定文本输入到活动窗口中。"

    def execute(self, text: str, interval: float = 0.05) -> SkillResult:
        """执行文本输入。

        Args:
            text: 要输入的文本。
            interval: 按键之间的时间间隔（秒）。

        Returns:
            表示成功或失败的 SkillResult。
        """
        try:
            logger.info(f"正在输入文本：{text[:50]}...")
            pyautogui.write(text, interval=interval)
            return SkillResult(success=True, message=f"文本输入成功")
        except Exception as e:
            logger.error(f"文本输入失败：{e}")
            return SkillResult(success=False, message=f"文本输入失败：{str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "text", "type": "str", "description": "要输入的文本"},
            {"name": "interval", "type": "float", "description": "按键之间的间隔"},
        ]


class PressHotkeySkill(BaseSkill):
    """按下键盘热键的技能。"""

    name = "press_hotkey"
    description = "按下组合键。"

    def execute(self, keys: List[str]) -> SkillResult:
        """执行热键按下。

        Args:
            keys: 键名列表（例如：['ctrl', 'c']）。

        Returns:
            表示成功或失败的 SkillResult。
        """
        try:
            logger.info(f"正在按下热键：{keys}")
            pyautogui.hotkey(*keys)
            return SkillResult(success=True, message=f"已按下热键：{'+'.join(keys)}")
        except Exception as e:
            logger.error(f"热键按下失败：{e}")
            return SkillResult(success=False, message=f"热键按下失败：{str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "keys", "type": "list", "description": "要按下的键列表"}
        ]


class DragSkill(BaseSkill):
    """将鼠标从一个点拖拽到另一个点的技能。"""

    name = "drag"
    description = "从起始坐标拖拽到结束坐标。"

    def execute(
        self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5
    ) -> SkillResult:
        """执行拖拽动作。

        Args:
            start_x: 起始 X 坐标。
            start_y: 起始 Y 坐标。
            end_x: 结束 X 坐标。
            end_y: 结束 Y 坐标。
            duration: 拖拽持续时间（秒）。

        Returns:
            表示成功或失败的 SkillResult。
        """
        try:
            logger.info(f"正在从 ({start_x}, {start_y}) 拖拽到 ({end_x}, {end_y})")
            pyautogui.moveTo(start_x, start_y)
            pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration)
            return SkillResult(success=True, message="拖拽完成")
        except Exception as e:
            logger.error(f"拖拽失败：{e}")
            return SkillResult(success=False, message=f"拖拽失败：{str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "start_x", "type": "int", "description": "起始 X 坐标"},
            {"name": "start_y", "type": "int", "description": "起始 Y 坐标"},
            {"name": "end_x", "type": "int", "description": "结束 X 坐标"},
            {"name": "end_y", "type": "int", "description": "结束 Y 坐标"},
            {"name": "duration", "type": "float", "description": "持续时间（秒）"},
        ]


class ScrollSkill(BaseSkill):
    """滚动鼠标滚轮的技能。"""

    name = "scroll"
    description = "滚动鼠标滚轮。"

    def execute(self, clicks: int, x: int = None, y: int = None) -> SkillResult:
        """执行滚动动作。

        Args:
            clicks: 滚动次数（正数向上，负数向下）。
            x: 可选的 X 坐标，在滚动前移动到此位置。
            y: 可选的 Y 坐标，在滚动前移动到此位置。

        Returns:
            表示成功或失败的 SkillResult。
        """
        try:
            if x is not None and y is not None:
                pyautogui.moveTo(x, y)
            logger.info(f"正在 ({x}, {y}) 处滚动 {clicks} 次")
            pyautogui.scroll(clicks)
            return SkillResult(success=True, message=f"已滚动 {clicks} 次")
        except Exception as e:
            logger.error(f"滚动失败：{e}")
            return SkillResult(success=False, message=f"滚动失败：{str(e)}")

    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        return [
            {"name": "clicks", "type": "int", "description": "滚动次数"},
            {"name": "x", "type": "int", "description": "可选的 X 坐标"},
            {"name": "y", "type": "int", "description": "可选的 Y 坐标"},
        ]
