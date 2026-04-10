"""与 LLM 提供商（如 OpenAI）交互的 AI 客户端。"""

import os
import json
import logging
from typing import List, Optional
import requests

from ..ai.models import IntentRecognitionResult, ChatMessage, PlannedAction, ActionParameter

logger = logging.getLogger(__name__)


class AIClient:
    """用于与云 AI 提供商通信的客户端。"""

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.openai.com/v1"):
        """初始化 AI 客户端。

        Args:
            api_key: LLM 提供商的 API 密钥。如果为 None，则从 OPENAI_API_KEY 环境变量读取。
            base_url: API 端点的基础 URL。默认为 OpenAI。
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url.rstrip("/")

        if not self.api_key:
            logger.warning("未找到 API 密钥。请设置 OPENAI_API_KEY 环境变量。")

        # 系统提示词，定义代理的能力和输出格式
        self.system_prompt = """
你是一个用于 Windows 的智能 GUI 自动化代理。
你的任务是解释用户命令并将它们分解为一系列原子动作。

可用的原子技能：
1. click(x, y): 在特定屏幕坐标处点击。
2. double_click(x, y): 在特定坐标处双击。
3. right_click(x, y): 在特定坐标处右键点击。
4. type_text(text): 将给定文本输入到活动窗口中。
5. press_hotkey(keys): 按下组合键（例如：['ctrl', 'c']）。
6. drag(start_x, start_y, end_x, end_y): 从起始坐标拖拽到结束坐标。
7. scroll(clicks, x, y): 滚动鼠标滚轮。
8. find_image_on_screen(image_path): 在屏幕上定位图像（返回坐标）。
9. ocr_region(x, y, width, height): 从屏幕区域提取文本。
10. get_active_window_title(): 获取当前活动窗口的标题。

输出格式：
你必须仅响应与此模式匹配的有效 JSON 对象：
{
    "intent": "字符串",
    "confidence": 浮点数 (0.0-1.0),
    "reasoning": "字符串（可选）",
    "actions": [
        {
            "skill_name": "字符串",
            "parameters": [
                {"name": "字符串", "value": 任意类型，"type": "字符串"}
            ],
            "description": "字符串（可选）"
        }
    ]
}

如果命令模糊或无法执行，请设置低置信度并在 reasoning 中解释。
"""

    def _call_llm_api(self, messages: List[dict]) -> str:
        """调用 LLM API 并返回原始响应文本。

        Args:
            messages: 包含 'role' 和 'content' 的消息字典列表。

        Returns:
            来自 API 的原始文本响应。

        Raises:
            requests.RequestException: 如果 API 调用失败。
            ValueError: 如果 API 响应无效。
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "gpt-4o",  # 使用最新的 GPT-4o 以获得最佳推理能力
            "messages": messages,
            "temperature": 0.1,  # 低温度以获得确定性输出
            "response_format": {"type": "json_object"},  # 强制 JSON 输出
        }

        url = f"{self.base_url}/chat/completions"

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return content
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP 错误：{e.response.text}")
            raise
        except Exception as e:
            logger.error(f"调用 LLM API 失败：{e}")
            raise

    def recognize_intent(self, user_command: str, context: Optional[str] = None) -> IntentRecognitionResult:
        """分析用户命令并返回结构化意图。

        Args:
            user_command: 来自用户的自然语言命令。
            context: 关于当前屏幕状态的可选上下文。

        Returns:
            包含解析动作的 IntentRecognitionResult 对象。
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]

        user_content = f"用户命令：{user_command}"
        if context:
            user_content += f"\n当前上下文：{context}"

        messages.append({"role": "user", "content": user_content})

        try:
            response_text = self._call_llm_api(messages)
            parsed_data = json.loads(response_text)
            
            # 验证并转换为 Pydantic 模型
            result = IntentRecognitionResult(**parsed_data)
            logger.info(f"意图已识别：{result.intent}（置信度：{result.confidence}）")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"无法将 AI 响应解析为 JSON：{e}")
            # 对非 JSON 响应的回退处理
            return IntentRecognitionResult(
                intent="unknown",
                confidence=0.0,
                reasoning=f"AI 返回了无效的 JSON：{response_text[:100]}",
                actions=[]
            )
        except Exception as e:
            logger.error(f"处理意图时出错：{e}")
            raise
