# keyboard-mouse-ai-agent

A background AI agent service for Windows that controls the user interface via keyboard shortcuts and atomic skills.

## Features

- **Hotkey Activation**: Press `Ctrl+Alt+A` (configurable) to invoke the command dialog from anywhere.
- **AI-Powered Intent Recognition**: Uses LLM (GPT-4o or compatible) to understand natural language commands.
- **Atomic Skills**: Execute precise GUI automation actions:
  - Mouse: Click, Double-click, Right-click, Drag, Scroll
  - Keyboard: Type text, Press hotkeys
  - Screen Analysis: OCR, Image recognition, Window info
- **Single File Distribution**: Package as a standalone `.exe` with no external dependencies.
- **pip Installable**: Install directly from PyPI (future).

## Requirements

- **OS**: Windows 10/11 only
- **Python**: 3.10, 3.11, or 3.12
- **API Key**: OpenAI API key (or compatible endpoint)

## Installation

### From Source (Development)

```bash
git clone https://github.com/yourusername/keyboard-mouse-ai-agent.git
cd keyboard-mouse-ai-agent
pip install -e ".[dev]"
```

### Set Environment Variables

```powershell
# PowerShell
setx OPENAI_API_KEY "your-openai-api-key-here"
```

## Usage

1. **Start the Agent**:
   ```bash
   km-agent
   ```

2. **Invoke Command Dialog**:
   Press `Ctrl+Alt+A` (or your configured hotkey).

3. **Enter Natural Language Command**:
   Examples:
   - "Open Chrome and search for Python tutorials"
   - "Copy the selected text and paste it into Notepad"
   - "Take a screenshot of the top-left corner and save it"
   - "Click on the button labeled 'Submit'"

4. **AI Executes Actions**: The agent interprets your command and performs the necessary clicks, typing, or other operations.

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `KM_AGENT_HOTKEY` | Hotkey combination | `ctrl+alt+a` |
| `KM_AGENT_API_BASE_URL` | Custom API endpoint | `https://api.openai.com/v1` |

## Building Standalone Executable

To create a single-file `.exe` for distribution:

```bash
pip install pyinstaller
pyinstaller --onefile --name km-agent src/km_agent/main.py
```

Or use the provided spec file:

```bash
pyinstaller pyinstaller.spec
```

The executable will be in the `dist/` folder.

## Architecture

```
km_agent/
├── ai/                 # AI intent recognition
│   ├── client.py       # LLM API client
│   └── models.py       # Pydantic models
├── skills/             # Atomic automation skills
│   ├── base.py         # Base skill class
│   ├── mouse_keyboard.py
│   └── screen_analysis.py
├── gui/                # User interface
│   └── dialog.py       # Command dialog
├── utils/              # Utilities
│   └── helpers.py      # Logging, config
└── main.py             # Entry point
```

## Development

### Code Style
This project follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

### Running Tests
```bash
pytest tests/
```

### Linting & Formatting
```bash
black src/ tests/
isort src/ tests/
mypy src/
```

## Roadmap

- [ ] Support for multiple LLM providers (Anthropic, Local models)
- [ ] Visual feedback during action execution
- [ ] Macro recording and playback
- [ ] Plugin system for custom skills
- [ ] Multi-monitor support enhancements

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

**Note**: This tool has powerful capabilities. Use responsibly and only on systems you own or have permission to automate.
