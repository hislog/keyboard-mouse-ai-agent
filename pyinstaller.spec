# PyInstaller configuration for keyboard-mouse-ai-agent
# This file ensures all dependencies are properly bundled

--onefile
--name km-agent
--icon=NONE
--hidden-import=pyautogui
--hidden-import=pywin32
--hidden-import=keyboard
--hidden-import=easyocr
--hidden-import=cv2
--hidden-import=numpy
--hidden-import=PIL
--hidden-import=customtkinter
--hidden-import=darkdetect
--collect-all=customtkinter
--collect-all=easyocr

# Exclude unnecessary modules to reduce size
--exclude-module=matplotlib
--exclude-module=scipy
--exclude-module=tkinter.test

# Add runtime options for better Windows compatibility
--runtime-tmpdir=.
--noconfirm
