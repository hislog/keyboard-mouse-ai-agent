"""用于 AI 意图识别和动作规划的 Pydantic 模型。"""

from typing import Optional, List, Literal, Any
from pydantic import BaseModel, Field


class ActionParameter(BaseModel):
    """表示原子技能动作的单个参数。"""

    name: str = Field(..., description="参数名称（例如：'x', 'y', 'text'）。")
    value: Any = Field(..., description="参数值。")
    type: str = Field(..., description="期望的数据类型（例如：'int', 'str', 'float'）。")


class PlannedAction(BaseModel):
    """表示要执行的单个原子动作。"""

    skill_name: str = Field(
        ...,
        description="要调用的原子技能名称（例如：'click', 'type_text', 'drag'）。",
    )
    parameters: List[ActionParameter] = Field(
        default_factory=list, description="技能所需的参数列表。"
    )
    description: Optional[str] = Field(
        None, description="此动作作用的简短自然语言描述。"
    )


class IntentRecognitionResult(BaseModel):
    """来自 AI 的结构化输出，表示用户的意图。"""

    intent: str = Field(..., description="分类的意图（例如：'open_app', 'click_element', 'search_web'）。")
    confidence: float = Field(..., ge=0.0, le=1.0, description="意图识别的置信度分数。")
    actions: List[PlannedAction] = Field(
        default_factory=list, description="实现意图的原子动作序列。"
    )
    reasoning: Optional[str] = Field(
        None, description="AI 推理过程的可选解释。"
    )


class ChatMessage(BaseModel):
    """表示对话历史中的消息。"""

    role: Literal["system", "user", "assistant"]
    content: str
