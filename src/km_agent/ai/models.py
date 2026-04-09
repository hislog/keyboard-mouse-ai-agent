"""Pydantic models for AI intent recognition and action planning."""

from typing import Optional, List, Literal, Any
from pydantic import BaseModel, Field


class ActionParameter(BaseModel):
    """Represents a single parameter for an atomic skill action."""

    name: str = Field(..., description="The name of the parameter (e.g., 'x', 'y', 'text').")
    value: Any = Field(..., description="The value of the parameter.")
    type: str = Field(..., description="The expected data type (e.g., 'int', 'str', 'float').")


class PlannedAction(BaseModel):
    """Represents a single atomic action to be executed."""

    skill_name: str = Field(
        ...,
        description="The name of the atomic skill to invoke (e.g., 'click', 'type_text', 'drag').",
    )
    parameters: List[ActionParameter] = Field(
        default_factory=list, description="List of parameters required for the skill."
    )
    description: Optional[str] = Field(
        None, description="A brief natural language description of what this action does."
    )


class IntentRecognitionResult(BaseModel):
    """The structured output from the AI representing the user's intent."""

    intent: str = Field(..., description="The classified intent (e.g., 'open_app', 'click_element', 'search_web').")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the intent recognition.")
    actions: List[PlannedAction] = Field(
        default_factory=list, description="Sequence of atomic actions to fulfill the intent."
    )
    reasoning: Optional[str] = Field(
        None, description="Optional explanation of the AI's reasoning process."
    )


class ChatMessage(BaseModel):
    """Represents a message in the conversation history."""

    role: Literal["system", "user", "assistant"]
    content: str
