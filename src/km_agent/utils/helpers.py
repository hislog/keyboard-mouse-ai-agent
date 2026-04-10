"""用于日志记录、配置和辅助函数的工具函数。"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    format_string: Optional[str] = None,
) -> None:
    """配置应用程序的日志记录。

    Args:
        level: 日志级别（例如：logging.DEBUG, logging.INFO）。
        log_file: 日志文件的可选路径。如果为 None，则仅记录到控制台。
        format_string: 自定义格式字符串。如果为 None，则使用默认值。
    """
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    # 创建格式化器
    formatter = logging.Formatter(format_string)

    # 设置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # 清除现有的处理器
    root_logger.handlers.clear()

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 文件处理器（可选）
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    logging.info(f"日志记录已配置：级别={logging.getLevelName(level)}, 文件={log_file}")


def get_resource_path(relative_path: str) -> Path:
    """获取资源的绝对路径，适用于开发和 PyInstaller 打包。

    这对于 PyInstaller 单文件可执行文件至关重要，因为资源
    会被提取到临时文件夹中。

    Args:
        relative_path: 从项目根目录到资源的相对路径。

    Returns:
        指向资源的绝对 Path 对象。
    """
    # 检查是否在 PyInstaller 打包中运行
    if getattr(sys, 'frozen', False):
        # 作为编译后的可执行文件运行
        base_path = Path(sys.executable).parent
    else:
        # 在正常 Python 环境中运行
        base_path = Path(__file__).parent.parent.parent

    return base_path / relative_path


class Config:
    """应用程序配置管理。"""

    # 触发对话框的默认热键 (Ctrl+Alt+A)
    DEFAULT_HOTKEY = "ctrl+alt+a"
    
    # AI 配置
    DEFAULT_AI_MODEL = "gpt-4o"
    DEFAULT_AI_TEMPERATURE = 0.1
    
    # 技能执行设置
    SKILL_EXECUTION_DELAY = 0.5  # 技能之间的秒数
    
    # GUI 设置
    DIALOG_WIDTH = 500
    DIALOG_HEIGHT = 180
    
    @classmethod
    def get_hotkey(cls) -> str:
        """获取配置的热键。"""
        import os
        return os.getenv("KM_AGENT_HOTKEY", cls.DEFAULT_HOTKEY)
    
    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """从环境获取 AI API 密钥。"""
        import os
        return os.getenv("OPENAI_API_KEY")
    
    @classmethod
    def get_api_base_url(cls) -> str:
        """从环境获取 AI API 基础 URL。"""
        import os
        return os.getenv("KM_AGENT_API_BASE_URL", "https://api.openai.com/v1")
