"""Unit tests for AI intent recognition models."""

import pytest
from pydantic import ValidationError
from km_agent.ai.models import (
    IntentRecognitionResult,
    PlannedAction,
    ActionParameter,
    ChatMessage,
)


class TestActionParameter:
    """Tests for ActionParameter model."""

    def test_create_valid_parameter(self):
        """Test creating a valid action parameter."""
        param = ActionParameter(name="x", value=100, type="int")
        assert param.name == "x"
        assert param.value == 100
        assert param.type == "int"

    def test_create_parameter_with_any_type(self):
        """Test creating a parameter with various value types."""
        param_str = ActionParameter(name="text", value="hello", type="str")
        param_int = ActionParameter(name="count", value=42, type="int")
        param_float = ActionParameter(name="duration", value=0.5, type="float")
        param_list = ActionParameter(name="keys", value=["ctrl", "c"], type="list")

        assert param_str.value == "hello"
        assert param_int.value == 42
        assert param_float.value == 0.5
        assert param_list.value == ["ctrl", "c"]


class TestPlannedAction:
    """Tests for PlannedAction model."""

    def test_create_valid_action(self):
        """Test creating a valid planned action."""
        action = PlannedAction(
            skill_name="click",
            parameters=[
                ActionParameter(name="x", value=100, type="int"),
                ActionParameter(name="y", value=200, type="int"),
            ],
            description="Click at position (100, 200)",
        )
        assert action.skill_name == "click"
        assert len(action.parameters) == 2
        assert action.description == "Click at position (100, 200)"

    def test_create_action_without_description(self):
        """Test creating an action without description."""
        action = PlannedAction(skill_name="type_text", parameters=[])
        assert action.skill_name == "type_text"
        assert action.description is None


class TestIntentRecognitionResult:
    """Tests for IntentRecognitionResult model."""

    def test_create_valid_result(self):
        """Test creating a valid intent recognition result."""
        result = IntentRecognitionResult(
            intent="open_application",
            confidence=0.95,
            actions=[
                PlannedAction(
                    skill_name="press_hotkey",
                    parameters=[
                        ActionParameter(name="keys", value=["win", "r"], type="list")
                    ],
                )
            ],
            reasoning="User wants to open the Run dialog",
        )
        assert result.intent == "open_application"
        assert result.confidence == 0.95
        assert len(result.actions) == 1
        assert result.reasoning == "User wants to open the Run dialog"

    def test_confidence_bounds(self):
        """Test that confidence must be between 0 and 1."""
        # Valid confidence
        result = IntentRecognitionResult(intent="test", confidence=0.5, actions=[])
        assert result.confidence == 0.5

        # Invalid confidence should raise ValidationError
        with pytest.raises(ValidationError):
            IntentRecognitionResult(intent="test", confidence=1.5, actions=[])

        with pytest.raises(ValidationError):
            IntentRecognitionResult(intent="test", confidence=-0.1, actions=[])

    def test_empty_actions(self):
        """Test creating a result with no actions."""
        result = IntentRecognitionResult(
            intent="unknown", confidence=0.0, reasoning="Could not understand"
        )
        assert result.actions == []
        assert result.reasoning == "Could not understand"


class TestChatMessage:
    """Tests for ChatMessage model."""

    def test_create_system_message(self):
        """Test creating a system message."""
        msg = ChatMessage(role="system", content="You are a helpful assistant.")
        assert msg.role == "system"
        assert msg.content == "You are a helpful assistant."

    def test_create_user_message(self):
        """Test creating a user message."""
        msg = ChatMessage(role="user", content="Open Chrome please.")
        assert msg.role == "user"

    def test_invalid_role(self):
        """Test that invalid roles raise ValidationError."""
        with pytest.raises(ValidationError):
            ChatMessage(role="invalid_role", content="test")
