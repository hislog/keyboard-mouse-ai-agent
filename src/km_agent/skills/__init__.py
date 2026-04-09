"""Skills module initialization."""

from .base import BaseSkill, SkillResult
from .mouse_keyboard import (
    ClickSkill,
    DoubleClickSkill,
    RightClickSkill,
    TypeTextSkill,
    PressHotkeySkill,
    DragSkill,
    ScrollSkill,
)
from .screen_analysis import (
    OCRRegionSkill,
    FindImageOnScreenSkill,
    GetActiveWindowTitleSkill,
    GetScreenSizeSkill,
)


class SkillRegistry:
    """Registry for all available atomic skills."""

    _skills = {}

    @classmethod
    def register(cls, skill_class):
        """Register a skill class."""
        instance = skill_class()
        cls._skills[instance.name] = instance
        return skill_class

    @classmethod
    def get_skill(cls, name: str):
        """Get a skill by name."""
        return cls._skills.get(name)

    @classmethod
    def list_skills(cls):
        """List all registered skills."""
        return list(cls._skills.keys())

    @classmethod
    def execute(cls, name: str, **kwargs):
        """Execute a skill by name with given parameters."""
        skill = cls.get_skill(name)
        if not skill:
            raise ValueError(f"Skill '{name}' not found. Available: {cls.list_skills()}")
        return skill.execute(**kwargs)


# Register all built-in skills
SkillRegistry.register(ClickSkill)
SkillRegistry.register(DoubleClickSkill)
SkillRegistry.register(RightClickSkill)
SkillRegistry.register(TypeTextSkill)
SkillRegistry.register(PressHotkeySkill)
SkillRegistry.register(DragSkill)
SkillRegistry.register(ScrollSkill)
SkillRegistry.register(OCRRegionSkill)
SkillRegistry.register(FindImageOnScreenSkill)
SkillRegistry.register(GetActiveWindowTitleSkill)
SkillRegistry.register(GetScreenSizeSkill)

__all__ = [
    "BaseSkill",
    "SkillResult",
    "SkillRegistry",
    "ClickSkill",
    "DoubleClickSkill",
    "RightClickSkill",
    "TypeTextSkill",
    "PressHotkeySkill",
    "DragSkill",
    "ScrollSkill",
    "OCRRegionSkill",
    "FindImageOnScreenSkill",
    "GetActiveWindowTitleSkill",
    "GetScreenSizeSkill",
]
