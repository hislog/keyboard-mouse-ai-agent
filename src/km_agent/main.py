"""Main entry point for the Keyboard Mouse AI Agent."""

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
    """Main service orchestrating the AI agent functionality."""

    def __init__(self, hotkey: Optional[str] = None):
        """Initialize the agent service.

        Args:
            hotkey: Hotkey combination to trigger the dialog. Defaults to config value.
        """
        self.hotkey = hotkey or Config.get_hotkey()
        self.ai_client = AIClient()
        self.dialog_manager = DialogManager()
        self._is_running = False
        
        logger.info(f"AgentService initialized with hotkey: {self.hotkey}")

    def _execute_plan(self, intent_result: IntentRecognitionResult) -> None:
        """Execute the sequence of actions from the AI plan.

        Args:
            intent_result: The structured intent result from AI.
        """
        if not intent_result.actions:
            logger.warning("No actions to execute.")
            return

        logger.info(f"Executing {len(intent_result.actions)} actions...")

        for i, action in enumerate(intent_result.actions):
            try:
                logger.info(f"Step {i+1}: Executing '{action.skill_name}'")
                
                # Convert parameters from ActionParameter list to dict
                params = {p.name: p.value for p in action.parameters}
                
                # Execute the skill
                result: SkillResult = SkillRegistry.execute(action.skill_name, **params)
                
                if result.success:
                    logger.info(f"Step {i+1} completed: {result.message}")
                else:
                    logger.error(f"Step {i+1} failed: {result.message}")
                    # Decide whether to continue or abort based on severity
                    # For now, we continue but log the error
                    
            except Exception as e:
                logger.error(f"Step {i+1} exception: {e}")
                # Continue to next action even if one fails

        logger.info("Action plan execution completed.")

    def _handle_command(self, command: str) -> None:
        """Process a user command: analyze with AI and execute.

        Args:
            command: The natural language command from user.
        """
        logger.info(f"Processing command: {command}")

        try:
            # Step 1: Get context (optional enhancement)
            # context = SkillRegistry.execute("get_active_window_title").data.get("title", "Unknown")
            context = None  # Simplified for now

            # Step 2: Recognize intent with AI
            intent_result = self.ai_client.recognize_intent(command, context=context)

            if intent_result.confidence < 0.5:
                logger.warning(f"Low confidence ({intent_result.confidence}): {intent_result.reasoning}")
                # Could show a warning dialog here

            # Step 3: Execute the planned actions
            self._execute_plan(intent_result)

        except Exception as e:
            logger.error(f"Failed to process command: {e}", exc_info=True)
            # Could show an error dialog here

    def _on_hotkey_triggered(self) -> None:
        """Callback when the hotkey is pressed."""
        logger.info("Hotkey triggered, showing dialog...")
        
        # Show dialog in a separate thread to avoid blocking hotkey listener
        def show_and_process():
            self.dialog_manager.show_dialog(
                on_submit=self._handle_command,
                on_cancel=lambda: logger.debug("Command cancelled by user")
            )
        
        threading.Thread(target=show_and_process, daemon=True).start()

    def start(self) -> None:
        """Start the agent service (blocking)."""
        logger.info("Starting KM Agent Service...")
        self._is_running = True

        # Register hotkey
        try:
            keyboard.add_hotkey(self.hotkey, self._on_hotkey_triggered)
            logger.info(f"Hotkey '{self.hotkey}' registered successfully.")
        except Exception as e:
            logger.error(f"Failed to register hotkey: {e}")
            raise

        # Initialize GUI
        self.dialog_manager.initialize()

        # Start GUI main loop (this blocks)
        # Note: keyboard library also needs to pump events, so we run them together
        logger.info("Agent service running. Press the hotkey to invoke commands.")
        
        # Run the GUI event loop
        # The keyboard library works in the background with its own threads
        self.dialog_manager.run()

    def stop(self) -> None:
        """Stop the agent service."""
        logger.info("Stopping KM Agent Service...")
        self._is_running = False
        
        # Unregister all hotkeys
        keyboard.unhook_all()
        
        # Stop GUI
        self.dialog_manager.stop()
        
        logger.info("Agent service stopped.")


def main():
    """Main entry point for the application."""
    # Setup logging
    setup_logging(level=logging.INFO)
    
    logger.info("=" * 60)
    logger.info("Keyboard Mouse AI Agent - Starting")
    logger.info("=" * 60)
    
    # Check for API key
    if not Config.get_api_key():
        logger.warning("OPENAI_API_KEY environment variable not set. AI features will fail.")
        logger.warning("Please set it: setx OPENAI_API_KEY 'your-key-here'")

    try:
        # Create and start service
        service = AgentService()
        service.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Application shutdown complete.")


if __name__ == "__main__":
    main()
