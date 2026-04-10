"""所有原子技能的基础类。"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class SkillResult:
    """表示技能执行的结果。"""

    def __init__(self, success: bool, message: str, data: Any = None):
        self.success = success
        self.message = message
        self.data = data

    def __repr__(self) -> str:
        return f"SkillResult(success={self.success}, message='{self.message}')"


class BaseSkill(ABC):
    """所有原子自动化技能的抽象基础类。"""

    name: str = "base_skill"
    description: str = "基础技能描述"

    @abstractmethod
    def execute(self, **kwargs) -> SkillResult:
        """使用给定参数执行技能。

        Args:
            **kwargs: 特定技能所需的参数。

        Returns:
            表示成功或失败的 SkillResult。
        """
        pass

    @abstractmethod
    def get_parameters_schema(self) -> List[Dict[str, Any]]:
        """返回此技能所需参数的模式。

        Returns:
            描述每个参数的字典列表（名称、类型、描述）。
        """
        pass
