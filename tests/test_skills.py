"""Unit tests for skill registry and execution."""

import pytest
from unittest.mock import patch, MagicMock
from km_agent.skills import SkillRegistry, SkillResult


class TestSkillRegistry:
    """Tests for the SkillRegistry class."""

    def test_list_skills(self):
        """Test that skills are registered correctly."""
        skills = SkillRegistry.list_skills()
        assert len(skills) > 0
        assert "click" in skills
        assert "type_text" in skills
        assert "press_hotkey" in skills

    def test_get_skill(self):
        """Test retrieving a skill by name."""
        skill = SkillRegistry.get_skill("click")
        assert skill is not None
        assert skill.name == "click"

    def test_get_nonexistent_skill(self):
        """Test retrieving a nonexistent skill."""
        skill = SkillRegistry.get_skill("nonexistent_skill")
        assert skill is None

    @patch('km_agent.skills.mouse_keyboard.pyautogui.size')
    def test_execute_get_screen_size_skill(self, mock_size):
        """Test executing get_screen_size skill (mocked)."""
        # Mock the screen size return value
        mock_size.return_value = (1920, 1080)
        
        result = SkillRegistry.execute("get_screen_size")
        assert isinstance(result, SkillResult)
        assert result.success is True
        assert "width" in result.data
        assert "height" in result.data
        assert result.data["width"] == 1920
        assert result.data["height"] == 1080


class TestMouseKeyboardSkills:
    """Tests for mouse and keyboard skills with mocked pyautogui."""

    @patch('km_agent.skills.mouse_keyboard.pyautogui.click')
    def test_click_skill(self, mock_click):
        """Test click skill execution."""
        result = SkillRegistry.execute("click", x=100, y=200, button="left")
        assert result.success is True
        mock_click.assert_called_once_with(x=100, y=200, clicks=1, interval=0.1, button="left")

    @patch('km_agent.skills.mouse_keyboard.pyautogui.write')
    def test_type_text_skill(self, mock_write):
        """Test type_text skill execution."""
        result = SkillRegistry.execute("type_text", text="Hello World", interval=0.05)
        assert result.success is True
        mock_write.assert_called_once_with("Hello World", interval=0.05)

    @patch('km_agent.skills.mouse_keyboard.pyautogui.hotkey')
    def test_press_hotkey_skill(self, mock_hotkey):
        """Test press_hotkey skill execution."""
        result = SkillRegistry.execute("press_hotkey", keys=["ctrl", "c"])
        assert result.success is True
        mock_hotkey.assert_called_once_with("ctrl", "c")

    @patch('km_agent.skills.mouse_keyboard.pyautogui.moveTo')
    @patch('km_agent.skills.mouse_keyboard.pyautogui.drag')
    def test_drag_skill(self, mock_drag, mock_moveTo):
        """Test drag skill execution."""
        result = SkillRegistry.execute("drag", start_x=100, start_y=100, end_x=200, end_y=200, duration=0.5)
        assert result.success is True
        mock_moveTo.assert_called_once_with(100, 100)
        mock_drag.assert_called_once_with(100, 100, duration=0.5)


class TestScreenAnalysisSkills:
    """Tests for screen analysis skills with mocked dependencies."""

    @patch('km_agent.skills.screen_analysis.pyautogui.size')
    def test_get_screen_size_skill(self, mock_size):
        """Test get_screen_size skill."""
        mock_size.return_value = (2560, 1440)
        result = SkillRegistry.execute("get_screen_size")
        assert result.success is True
        assert result.data["width"] == 2560
        assert result.data["height"] == 1440

    @patch('builtins.__import__')
    def test_get_active_window_title_skill(self, mock_import):
        """Test get_active_window_title skill (mocked win32gui)."""
        # Mock the win32gui module
        mock_win32gui = MagicMock()
        mock_win32gui.GetForegroundWindow.return_value = 12345
        mock_win32gui.GetWindowText.return_value = "Notepad"
        
        def import_side_effect(name, *args, **kwargs):
            if name == 'win32gui':
                return mock_win32gui
            # For other imports, use the real import
            import builtins
            return builtins.__import__(name, *args, **kwargs)
        
        mock_import.side_effect = import_side_effect
        
        result = SkillRegistry.execute("get_active_window_title")
        assert result.success is True
        assert result.data["title"] == "Notepad"


class TestSkillResults:
    """Tests for SkillResult data structure."""

    def test_success_result(self):
        """Test creating a successful result."""
        result = SkillResult(success=True, message="Operation completed", data={"key": "value"})
        assert result.success is True
        assert result.message == "Operation completed"
        assert result.data == {"key": "value"}

    def test_failure_result(self):
        """Test creating a failure result."""
        result = SkillResult(success=False, message="Operation failed")
        assert result.success is False
        assert result.message == "Operation failed"
        assert result.data is None
