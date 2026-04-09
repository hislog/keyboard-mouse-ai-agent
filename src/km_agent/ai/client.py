"""AI Client for interacting with LLM providers (e.g., OpenAI)."""

import os
import json
import logging
from typing import List, Optional
import requests

from ..ai.models import IntentRecognitionResult, ChatMessage, PlannedAction, ActionParameter

logger = logging.getLogger(__name__)


class AIClient:
    """Client for communicating with Cloud AI providers."""

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.openai.com/v1"):
        """Initialize the AI client.

        Args:
            api_key: The API key for the LLM provider. If None, reads from OPENAI_API_KEY env var.
            base_url: The base URL for the API endpoint. Defaults to OpenAI.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url.rstrip("/")

        if not self.api_key:
            logger.warning("API Key not found. Please set OPENAI_API_KEY environment variable.")

        # System prompt defining the agent's capabilities and output format
        self.system_prompt = """
You are an intelligent GUI automation agent for Windows. 
Your task is to interpret user commands and break them down into a sequence of atomic actions.

Available Atomic Skills:
1. click(x, y): Click at specific screen coordinates.
2. double_click(x, y): Double click at specific coordinates.
3. right_click(x, y): Right click at specific coordinates.
4. type_text(text): Type the given text into the active window.
5. press_hotkey(keys): Press a combination of keys (e.g., ['ctrl', 'c']).
6. drag(start_x, start_y, end_x, end_y): Drag from start to end coordinates.
7. scroll(clicks, x, y): Scroll the mouse wheel.
8. find_image_on_screen(image_path): Locate an image on screen (returns coordinates).
9. ocr_region(x, y, width, height): Extract text from a screen region.
10. get_active_window_title(): Get the title of the currently active window.

Output Format:
You must respond ONLY with a valid JSON object matching this schema:
{
    "intent": "string",
    "confidence": float (0.0-1.0),
    "reasoning": "string (optional)",
    "actions": [
        {
            "skill_name": "string",
            "parameters": [
                {"name": "string", "value": any, "type": "string"}
            ],
            "description": "string (optional)"
        }
    ]
}

If the command is ambiguous or cannot be executed, set confidence low and explain in reasoning.
"""

    def _call_llm_api(self, messages: List[dict]) -> str:
        """Call the LLM API and return the raw response text.

        Args:
            messages: List of message dictionaries with 'role' and 'content'.

        Returns:
            The raw text response from the API.

        Raises:
            requests.RequestException: If the API call fails.
            ValueError: If the API response is invalid.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "gpt-4o",  # Using latest GPT-4o for best reasoning
            "messages": messages,
            "temperature": 0.1,  # Low temperature for deterministic outputs
            "response_format": {"type": "json_object"},  # Force JSON output
        }

        url = f"{self.base_url}/chat/completions"

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return content
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Failed to call LLM API: {e}")
            raise

    def recognize_intent(self, user_command: str, context: Optional[str] = None) -> IntentRecognitionResult:
        """Analyze user command and return structured intent.

        Args:
            user_command: The natural language command from the user.
            context: Optional context about the current screen state.

        Returns:
            IntentRecognitionResult object containing parsed actions.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
        ]

        user_content = f"User Command: {user_command}"
        if context:
            user_content += f"\nCurrent Context: {context}"

        messages.append({"role": "user", "content": user_content})

        try:
            response_text = self._call_llm_api(messages)
            parsed_data = json.loads(response_text)
            
            # Validate and convert to Pydantic model
            result = IntentRecognitionResult(**parsed_data)
            logger.info(f"Intent recognized: {result.intent} (confidence: {result.confidence})")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            # Fallback for non-JSON responses
            return IntentRecognitionResult(
                intent="unknown",
                confidence=0.0,
                reasoning=f"AI returned invalid JSON: {response_text[:100]}",
                actions=[]
            )
        except Exception as e:
            logger.error(f"Error processing intent: {e}")
            raise
