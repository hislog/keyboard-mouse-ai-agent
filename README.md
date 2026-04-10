# keyboard-mouse-ai-agent

一个用于 Windows 的后台 AI 代理服务，通过键盘快捷键和原子技能控制用户界面。

## 功能特性

- **热键激活**：按 `Ctrl+Alt+A`（可配置）从任何地方调用命令对话框。
- **AI 驱动的意图识别**：使用 LLM（GPT-4o 或兼容模型）理解自然语言命令。
- **原子技能**：执行精确的 GUI 自动化操作：
  - 鼠标：点击、双击、右键点击、拖拽、滚动
  - 键盘：输入文本、按下热键
  - 屏幕分析：OCR、图像识别、窗口信息
- **单文件分发**：打包为独立的 `.exe`，无需外部依赖。
- **支持 pip 安装**：可直接从 PyPI 安装（未来）。

## 系统要求

- **操作系统**：仅限 Windows 10/11
- **Python**：3.10、3.11 或 3.12
- **API 密钥**：OpenAI API 密钥（或兼容端点）

## 安装

### 从源码安装（开发模式）

```bash
git clone https://github.com/yourusername/keyboard-mouse-ai-agent.git
cd keyboard-mouse-ai-agent
pip install -e ".[dev]"
```

### 设置环境变量

```powershell
# PowerShell
setx OPENAI_API_KEY "your-openai-api-key-here"
```

## 使用方法

1. **启动代理服务**：
   ```bash
   km-agent
   ```

2. **调用命令对话框**：
   按 `Ctrl+Alt+A`（或您配置的热键）。

3. **输入自然语言命令**：
   示例：
   - "打开 Chrome 并搜索 Python 教程"
   - "复制选中的文本并粘贴到记事本中"
   - "截取左上角的屏幕截图并保存"
   - "点击标有'提交'的按钮"

4. **AI 执行操作**：代理解释您的命令并执行必要的点击、输入或其他操作。

## 配置

| 环境变量 | 描述 | 默认值 |
|---------------------|-------------|---------|
| `OPENAI_API_KEY` | 您的 OpenAI API 密钥 | 必需 |
| `KM_AGENT_HOTKEY` | 热键组合 | `ctrl+alt+a` |
| `KM_AGENT_API_BASE_URL` | 自定义 API 端点 | `https://api.openai.com/v1` |

## 构建独立可执行文件

要创建用于分发的单文件 `.exe`：

```bash
pip install pyinstaller
pyinstaller --onefile --name km-agent src/km_agent/main.py
```

或使用提供的 spec 文件：

```bash
pyinstaller pyinstaller.spec
```

可执行文件将在 `dist/` 文件夹中。

## 架构

```
km_agent/
├── ai/                 # AI 意图识别
│   ├── client.py       # LLM API 客户端
│   └── models.py       # Pydantic 模型
├── skills/             # 原子自动化技能
│   ├── base.py         # 基础技能类
│   ├── mouse_keyboard.py
│   └── screen_analysis.py
├── gui/                # 用户界面
│   └── dialog.py       # 命令对话框
├── utils/              # 工具函数
│   └── helpers.py      # 日志记录、配置
└── main.py             # 入口点
```

## 开发

### 代码风格
本项目遵循 [Google Python 风格指南](https://google.github.io/styleguide/pyguide.html)。

### 运行测试
```bash
pytest tests/
```

### 代码检查与格式化
```bash
black src/ tests/
isort src/ tests/
mypy src/
```

## 路线图

- [ ] 支持多个 LLM 提供商（Anthropic、本地模型）
- [ ] 操作执行期间的视觉反馈
- [ ] 宏录制和回放
- [ ] 自定义技能的插件系统
- [ ] 多显示器支持增强

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎贡献！请提出问题或提交拉取请求。

---

**注意**：此工具具有强大的功能。请负责任地使用，仅在您拥有或有权自动化的系统上使用。
