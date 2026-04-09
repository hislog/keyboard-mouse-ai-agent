"""Base class for all atomic skills."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class SkillResult:
    """Represents the result of a skill execution."""

    def __init__(self, success: bool, message: str, data: Any = None):
        self.success = success
        self.message = message
        self.data = data

    def __repr__(self) -> str:
        return f"SkillResult(success={self.success}, message='{self.message}')"


class BaseSkill(ABC):
    """Abstract base class for all atomic automation skills."""

    name: str = "base_skill"
    description: str = "Base skill description"

    @abstractmethod
    def execute(self, **kwargs) -> SkillResult:
        """Execute the skill with given parameters.

        Args:
            **kwargs: Parameters required by the specific skill.

        Returns:
            SkillResult indicating success or failure.
        """
        pass

    @abstractmethod
    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        """Return the schema of parameters required by this skill.

        Returns:
            List of dictionaries describing each parameter (name, type, description).
        """
        pass
