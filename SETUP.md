# AgentSaasy Setup Guide

> ⚠️ **Do not paste this entire document into the terminal.**  
> Follow these instructions in the Cursor UI. For terminal commands only, see `TERMINAL-COMMANDS.md`.

---

## API Keys Setup

### Important: API Keys Cost Money (Separate from Cursor/Claude.ai)

**Understand the difference:**
- **claude.ai subscription** ($20/month Pro) = Chat interface access only
- **API access** = Pay-per-use (separate billing, requires payment method)

**For this project, you only need:**
```bash
OPENAI_API_KEY=sk-...  # Required - agent uses GPT-4o-mini
```

**Optional (not used by default):**
```bash
ANTHROPIC_API_KEY=sk-ant-...  # Only if you want to test Claude API
```

### API Pricing Reference

**OpenAI GPT-4o-mini** (default):
- Input: ~$0.15 per 1M tokens
- Output: ~$0.60 per 1M tokens
- Free tier: $5 credit on signup
- **Typical query cost: ~$0.0006** (very affordable)

**Anthropic Claude Sonnet 4**:
- Input: ~$3 per 1M tokens
- Output: ~$15 per 1M tokens
- Free tier: $5 credit on signup
- **Typical query cost: ~$0.014** (20x more expensive)

**Cost estimate for 100 test queries:**
- GPT-4o-mini: ~$0.06
- Claude Sonnet 4: ~$1.40

### Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up / log in
3. Create new secret key
4. Copy to `.env`: `OPENAI_API_KEY=sk-...`
5. Add payment method after $5 free credit runs out

### Using Claude API Instead (Optional)

To switch from OpenAI to Claude, modify `agent.py`:

```python
# Replace:
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")

# With:
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)
```

And install: `pip install langchain-anthropic`

---

## Cursor Settings (Configure in the UI)

**Go to:** `Cursor` → `Settings` → `Cursor Settings` → `Features`

| Setting | Value |
|---------|-------|
| Codebase Indexing | ON |
| Auto-import detection | ON |
| Symbol search | ON |

**Privacy:** `Cursor Settings` → `Privacy`
- Enable Cursor to read your codebase (needed for context)
- Include files in .gitignore (.env won't be uploaded)

---

## Verify Your Setup

### 1. Test Chat
- Press `Cmd + L` (Mac) or `Ctrl + L` (Windows) to open chat
- Type: `@Sonnet Explain the ReAct pattern in my agent.py file`
- Cursor should analyze your code and explain

### 2. Test Composer
- Press `Cmd + I` (Mac) or `Ctrl + I` (Windows)
- Type: `Add type hints to all functions in agent.py`
- Review changes, accept if good

### 3. Test Agent Mode
- In chat, type: `Run the agent with a test query and show me the output`
- Cursor should execute `python agent.py` and show results

### 4. Test Terminal Integration
- In chat, type: `Run pytest on my test files`
- Cursor should execute tests and suggest fixes if they fail

---

## Cursor Usage Patterns

### A) Composer (Multi-file editing) - `Cmd + I`

**When to use:**
- Building initial project structure
- Refactoring across multiple files
- Adding a new tool that touches agent.py, tests/, and docs

**Example prompt:**
```
Add a new tool called "forecast_sales" that uses linear regression.
Update agent.py to include it, add tests in tests/test_agent.py,
and update the README with usage examples.
```

Cursor will:
1. Show you all files it'll modify
2. Make changes across all of them
3. Let you review before accepting

### B) Chat - `Cmd + L`

**When to use:**
- Asking questions about code
- Debugging specific functions
- Getting explanations

**Example prompts:**
```
@Sonnet Why is my ReAct agent not calling tools in sequence?

@GPT4 Explain how the query_data tool filters by quarter

Debug the analyze_trends function - growth calculation seems off
```

### C) Inline Edit - Highlight code + `Cmd + K`

**When to use:**
- Quick edits to a function
- Refactoring a small section
- Adding comments

**Example:**
```
# Highlight the analyze_trends function, then Cmd + K:
Add correlation analysis between products and regions
```

---

## Cursor Keyboard Shortcuts (Mac)

**Essential for AI development:**
```
Cmd + L          → Open Chat
Cmd + I          → Open Composer (multi-file)
Cmd + K          → Inline edit (on highlighted code)
Cmd + `          → Toggle terminal
Cmd + Shift + P  → Command palette
Cmd + /          → Add/remove comment

# During chat:
Cmd + Enter      → Send message
Esc              → Close chat
@ + model name   → Force specific model (@Sonnet, @GPT4, etc.)
```

---

## Terminal Commands

**Only run these in a terminal.** Copy from `TERMINAL-COMMANDS.md` to avoid pasting instructions by mistake.
