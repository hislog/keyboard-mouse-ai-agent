"""GUI module for the instruction dialog using customtkinter."""

import logging
import threading
from typing import Optional, Callable

import customtkinter as ctk

logger = logging.getLogger(__name__)

# Configure customtkinter appearance
ctk.set_appearance_mode("Dark")  # Dark mode for background service feel
ctk.set_default_color_theme("blue")


class InstructionDialog(ctk.CTkToplevel):
    """Floating instruction dialog that appears on hotkey trigger."""

    def __init__(
        self,
        parent,
        on_submit: Callable[[str], None],
        on_cancel: Optional[Callable[[], None]] = None,
    ):
        """Initialize the instruction dialog.

        Args:
            parent: Parent window.
            on_submit: Callback function when user submits command.
            on_cancel: Optional callback when user cancels.
        """
        super().__init__(parent)
        
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.result_command = None
        
        # Window configuration
        self.title("AI Agent Command")
        self.geometry("500x180")
        self.resizable(False, False)
        
        # Keep window on top
        self.attributes('-topmost', True)
        
        # Center the window on screen
        self._center_window()
        
        self._create_widgets()
        
        # Bind Enter key to submit, Escape to cancel
        self.bind('<Return>', lambda e: self._submit())
        self.bind('<Escape>', lambda e: self._cancel())
        
        # Focus on entry field
        self.command_entry.focus_set()
        
        logger.info("Instruction dialog created.")

    def _center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _create_widgets(self):
        """Create the UI widgets."""
        # Main frame with padding
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title label
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Enter your command:", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Command entry field
        self.command_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="e.g., 'Open Chrome and search for Python tutorials'",
            height=40,
            font=ctk.CTkFont(size=14),
        )
        self.command_entry.pack(fill="x", pady=(0, 15))
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        # Submit button
        self.submit_btn = ctk.CTkButton(
            btn_frame,
            text="Execute",
            command=self._submit,
            width=100,
            height=35,
        )
        self.submit_btn.pack(side="left", padx=(0, 10))
        
        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self._cancel,
            fg_color="gray",
            hover_color="darkgray",
            width=100,
            height=35,
        )
        self.cancel_btn.pack(side="right")

    def _submit(self):
        """Handle submit action."""
        command = self.command_entry.get().strip()
        if command:
            logger.info(f"Command submitted: {command}")
            self.result_command = command
            self.destroy()
            # Call callback in a separate thread to avoid blocking GUI
            threading.Thread(target=self.on_submit, args=(command,), daemon=True).start()
        else:
            # Shake animation or visual feedback for empty input
            self.command_entry.configure(border_color="red")
            self.after(500, lambda: self.command_entry.configure(border_color=""))

    def _cancel(self):
        """Handle cancel action."""
        logger.info("Command cancelled.")
        self.result_command = None
        self.destroy()
        if self.on_cancel:
            self.on_cancel()

    def get_command(self) -> Optional[str]:
        """Get the entered command after dialog closes."""
        return self.result_command


class DialogManager:
    """Manages the lifecycle of instruction dialogs."""

    def __init__(self):
        """Initialize the dialog manager."""
        self.root = None
        self.dialog = None
        self._is_initialized = False

    def initialize(self):
        """Initialize the hidden root window."""
        if self._is_initialized:
            return
            
        # Create hidden root window
        self.root = ctk.CTk()
        self.root.withdraw()  # Hide the root window
        self.root.title("KM Agent Background Service")
        
        # Protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_root_close)
        
        self._is_initialized = True
        logger.info("Dialog manager initialized.")

    def show_dialog(self, on_submit: Callable[[str], None], on_cancel: Optional[Callable[[], None]] = None):
        """Show the instruction dialog.

        Args:
            on_submit: Callback when command is submitted.
            on_cancel: Optional callback when cancelled.
        """
        if not self._is_initialized:
            self.initialize()
        
        # Create dialog
        self.dialog = InstructionDialog(self.root, on_submit=on_submit, on_cancel=on_cancel)
        
        # Wait for dialog to close
        self.root.wait_window(self.dialog)

    def _on_root_close(self):
        """Handle root window close event."""
        logger.info("Root window closing.")
        self.root.quit()
        self.root.destroy()

    def run(self):
        """Start the main event loop."""
        if not self._is_initialized:
            self.initialize()
        logger.info("Starting dialog event loop.")
        self.root.mainloop()

    def stop(self):
        """Stop the event loop."""
        if self.root:
            self.root.after(0, self.root.quit)
