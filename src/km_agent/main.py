"""键盘鼠标 AI 代理的主要入口点。"""

import logging
import sys
import threading
from typing import Optional

import keyboard

from .ai import AIClient, IntentRecognitionResult
from .skills import SkillRegistry, SkillResult
from .gui import DialogManager
from .utils import setup_logging, Config

logger = logging.getLogger(__name__)


class AgentService:
    """协调 AI 代理功能的主要服务类。"""

    def __init__(self, hotkey: Optional[str] = None):
        """初始化代理服务。

        Args:
            hotkey: 触发对话框的热键组合。默认为配置值。
        """
        self.hotkey = hotkey or Config.get_hotkey()
        self.ai_client = AIClient()
        self.dialog_manager = DialogManager()
        self._is_running = False
        
        logger.info(f"代理服务已初始化，热键：{self.hotkey}")

    def _execute_plan(self, intent_result: IntentRecognitionResult) -> None:
        """执行 AI 计划中的动作序列。

        Args:
            intent_result: 来自 AI 的结构化意图结果。
        """
        if not intent_result.actions:
            logger.warning("没有要执行的动作。")
            return

        logger.info(f"正在执行 {len(intent_result.actions)} 个动作...")

        for i, action in enumerate(intent_result.actions):
            try:
                logger.info(f"步骤 {i+1}: 执行 '{action.skill_name}'")
                
                # 将参数从 ActionParameter 列表转换为字典
                params = {p.name: p.value for p in action.parameters}
                
                # 执行技能
                result: SkillResult = SkillRegistry.execute(action.skill_name, **params)
                
                if result.success:
                    logger.info(f"步骤 {i+1} 完成：{result.message}")
                else:
                    logger.error(f"步骤 {i+1} 失败：{result.message}")
                    # 根据严重程度决定是否继续或中止
                    # 目前我们继续但记录错误
                    
            except Exception as e:
                logger.error(f"步骤 {i+1} 异常：{e}")
                # 即使一个动作失败也继续下一个动作

        logger.info("动作计划执行完成。")

    def _handle_command(self, command: str) -> None:
        """处理用户命令：使用 AI 分析并执行。

        Args:
            command: 来自用户的自然语言命令。
        """
        logger.info(f"正在处理命令：{command}")

        try:
            # 步骤 1：获取上下文（可选增强）
            # context = SkillRegistry.execute("get_active_window_title").data.get("title", "Unknown")
            context = None  # 目前简化处理

            # 步骤 2：使用 AI 识别意图
            intent_result = self.ai_client.recognize_intent(command, context=context)

            if intent_result.confidence < 0.5:
                logger.warning(f"低置信度 ({intent_result.confidence}): {intent_result.reasoning}")
                # 可以在此处显示警告对话框

            # 步骤 3：执行计划的动作
            self._execute_plan(intent_result)

        except Exception as e:
            logger.error(f"处理命令失败：{e}", exc_info=True)
            # 可以在此处显示错误对话框

    def _on_hotkey_triggered(self) -> None:
        """热键被按下时的回调函数。"""
        logger.info("热键已触发，正在显示对话框...")
        
        # 在单独的线程中显示对话框以避免阻塞热键监听器
        def show_and_process():
            self.dialog_manager.show_dialog(
                on_submit=self._handle_command,
                on_cancel=lambda: logger.debug("用户已取消命令")
            )
        
        threading.Thread(target=show_and_process, daemon=True).start()

    def start(self) -> None:
        """启动代理服务（阻塞）。"""
        logger.info("正在启动 KM 代理服务...")
        self._is_running = True

        # 注册热键
        try:
            keyboard.add_hotkey(self.hotkey, self._on_hotkey_triggered)
            logger.info(f"热键 '{self.hotkey}' 注册成功。")
        except Exception as e:
            logger.error(f"注册热键失败：{e}")
            raise

        # 初始化 GUI
        self.dialog_manager.initialize()

        # 启动 GUI 主循环（阻塞）
        # 注意：keyboard 库也需要泵送事件，所以我们一起运行它们
        logger.info("代理服务正在运行。按热键调用命令。")
        
        # 运行 GUI 事件循环
        # keyboard 库在后台使用自己的线程工作
        self.dialog_manager.run()

    def stop(self) -> None:
        """停止代理服务。"""
        logger.info("正在停止 KM 代理服务...")
        self._is_running = False
        
        # 注销所有热键
        keyboard.unhook_all()
        
        # 停止 GUI
        self.dialog_manager.stop()
        
        logger.info("代理服务已停止。")


def main():
    """应用程序的主要入口点。"""
    # 设置日志记录
    setup_logging(level=logging.INFO)
    
    logger.info("=" * 60)
    logger.info("键盘鼠标 AI 代理 - 正在启动")
    logger.info("=" * 60)
    
    # 检查 API 密钥
    if not Config.get_api_key():
        logger.warning("未设置 OPENAI_API_KEY 环境变量。AI 功能将失败。")
        logger.warning("请设置它：setx OPENAI_API_KEY 'your-key-here'")

    try:
        # 创建并启动服务
        service = AgentService()
        service.start()
    except KeyboardInterrupt:
        logger.info("被用户中断。")
    except Exception as e:
        logger.error(f"致命错误：{e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("应用程序关闭完成。")


if __name__ == "__main__":
    main()
