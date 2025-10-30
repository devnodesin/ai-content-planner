# Content Planner


An interactive Python command-line application for AI-powered content idea generation for e-commerce products.
Uses Ollama Cloud to generate smart customer questions and unique content ideas in JSON format.

**The AI acts as a curious customer**, asking genuine questions without assumptions, helping you understand what information your customers need.

Built with Python 3.13 and managed with [uv](https://docs.astral.sh/uv/) for fast, reliable dependency management.

📋 **For technical specifications, architecture, and detailed design information, see [SPEC.md](./spec/SPEC.md)**

## Features

- 🤖 **AI-powered customer perspective** - AI acts like a real customer, asking genuine questions before purchase
- 📄 **Context File Generator** - Convert .md, .json files, or web URLs into standardized context format
- 📂 **Session Resume** - Load previous sessions or start new ones with interactive arrow-key menu
- ❓ **Smart question generation** - Diverse question types (what, who, which, whose, when, why, where, how)
- ⏭️ **Skip questions** - Press Enter to skip any question you don't want to answer
- 💡 **Structured content ideas** - Article titles with 100-150 char summaries, returned in JSON format
- 🚫 **Smart deduplication** - No duplicate or similar content ideas (70%+ similarity filtered)
- 🔄 **Follow-up rounds** - AI asks follow-up questions for unclear areas and explores new product aspects
- 📊 **JSON export** for easy integration
- 💾 **Auto-save** every 5 minutes (silent background)
- 📝 **Manual save** with 's' key (returns to menu, not questions)
- 🔄 **User2AI Mode** - Interactive Q&A with AI asking questions (default workflow)
- 🤖 **AI2AI Mode** - Automated mode where customer AI and salesman AI interact automatically
  - Customer agent generates questions
  - Salesman agent answers using product context from `out/context.md`
  - Separate configurable models for each agent
- 🎨 **Colorful interface** - Easy-to-read colored output (menu, questions, outputs, success messages)
- 🐛 **Logging support** - Optional logging for debugging and monitoring
- 🧪 **Code coverage** - Built-in pytest-cov for test coverage analysis
- 🤖 **AI model display** - See which AI model is being used during generation
- ⚡ **Lightning-fast** dependency management with uv
- 🐍 **Python 3.13** (latest stable, supported until 2029)

---

## Quick Start

### 1. Install uv

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install Dependencies

- Copy the example env file
- Edit .env and add your Ollama API key from https://ollama.com

```bash
cp .env.example .env
```

```bash
uv sync
uv run python run.py
```

### Run Tests

```bash
# Run all tests
uv run pytest src/tests/ -v

# Run specific test file
uv run pytest src/tests/test_session.py -v

# Run tests with coverage report
uv run pytest src/tests/ -v --cov=src --cov-report=term

# Run tests with detailed coverage (shows missing lines)
uv run pytest src/tests/ -v --cov=src --cov-report=term-missing

# Generate HTML coverage report
uv run pytest src/tests/ -v --cov=src --cov-report=html
# Then open htmlcov/index.html in your browser
```

### Add Dependencies

```bash
# Add runtime dependency
uv add package-name

# Add dev dependency
uv add --dev package-name

# Update all dependencies
uv sync --upgrade

# Update specific package
uv add package-name@latest
```

---

## Context File Generator

Generate standardized markdown context files from various input sources (`.md`, `.json`, web URLs) for use with the content planner.

### Quick Usage

```bash
# From a markdown file
uv run python tools/generate_context.py product.md

# From a JSON file with custom output name
uv run python tools/generate_context.py data.json --output custom_context

# From a web URL with preview (HTML auto-converted to markdown)
uv run python tools/generate_context.py https://example.com/api/product --preview

# Show help
uv run python tools/generate_context.py --help
```

### Features
- Accepts `.md` files, `.json` files, or web URLs
- Validates and parses source data
- Converts to standardized markdown format
- **Automatic HTML to markdown conversion** for web URLs
- **Removes unwanted sections**: header, footer, nav, aside, sidebar
- **Extracts main content only** for clean, AI-friendly output
- Smart file handling (overwrite protection, auto-numbering)
- Optional preview before saving
- Comprehensive error handling

**📖 Full documentation:** [docs/GENERATE_CONTEXT.md](docs/GENERATE_CONTEXT.md)  
**⚡ Quick reference:** [spec/GENERATE_CONTEXT_QUICK_REF.md](spec/GENERATE_CONTEXT_QUICK_REF.md)  
**📋 Implementation details:** [spec/GENERATE_CONTEXT_IMPLEMENTATION.md](spec/GENERATE_CONTEXT_IMPLEMENTATION.md)

---

## How It Works


The AI acts as a smart customer evaluating your product, asking genuine questions that real customers would ask before making a purchase. It uses previous Q&A context to ask follow-up questions for unclear areas and explores new product aspects. Content ideas are unique, deduplicated, and returned in JSON format.

**See [SPEC.md](./spec/SPEC.md) for detailed workflow, question logic, and output format.**

---

## Usage

### Session Resume

On startup, if an existing session file (`out/content_ideas.json`) is found, you'll see:

```bash
📂 Existing Session Found
----------------------------------------------------------------------

Product/Topic: Wireless Headphones
Rounds Completed: 3
Q&A Pairs: 15
Content Ideas: 30
Last Updated: 2025-01-27T10:30:00

======================================================================
📋 Options: [r] Resume, [n] New, [q] Quit
======================================================================
Your choice (r/n/q): r
```

**Options:**
- **r (Resume)** - Load existing session and continue from where you left off
- **n (New)** - Start a new session with a different product
- **q (Quit)** - Exit the application

### Main Workflow

1. **Session Resume (if applicable)** - Choose to resume existing session or start new
2. **Main Menu** - Select mode: User2AI, AI2AI, Save, or Quit
3. **Enter Product Name** (if new session) - Type your product name
4. **Mode Execution**:
   - **User2AI Mode**: AI generates questions → You answer them
   - **AI2AI Mode**: AI generates questions → AI answers them (using context file)
5. **Review Content Ideas** - Get article title ideas with summaries
6. **Return to Main Menu** - Choose next action

### Menu Flow

After session resume or starting new:
```
======================================================================
📋 Options: [u] User2AI Mode, [a] AI2AI Mode, [s] Save, [q] Quit
======================================================================
Your choice (u/a/s/q): 
```

**Options:**
- `u` - **User2AI Mode** - AI asks questions, you answer them
- `a` - **AI2AI Mode** - AI asks and answers questions automatically using `out/context.md`
- `s` - Save current progress (returns to menu)
- `q` - Quit and save all data to `out/content_ideas.json`

### Example Session

```bash
$ uv run python run.py

# If existing session found
📂 Existing Session Found
----------------------------------------------------------------------
Product/Topic: Wireless Headphones
Rounds Completed: 2
Q&A Pairs: 10
Content Ideas: 20
Last Updated: 2025-01-27T10:30:00

======================================================================
📋 Options: [r] Resume, [n] New, [q] Quit
======================================================================
Your choice (r/n/q): n

======================================================================
  🎯 Content Planner - Product Input
======================================================================

Enter product name: Smart Fitness Tracker

======================================================================
📋 Options: [u] User2AI Mode, [a] AI2AI Mode, [s] Save, [q] Quit
======================================================================
Your choice (u/a/s/q): u

🤖 AI is generating questions (model: deepseek-v3.1:671b-cloud)...

----------------------------------------------------------------------
  📝 Questions & Answers
----------------------------------------------------------------------

💡 Tip: Press Enter without typing to skip a question

[1/5] What is the primary function of the Smart Fitness Tracker?

💡 Tip: Press Enter without typing to skip a question

[1/5] What is this product used for?
Your answer: Listening to music and taking calls without wires

[2/5] Who is this product designed for?
Your answer: Commuters, fitness enthusiasts, and remote workers

[3/5] How do I use this product properly?
Your answer: Pair via Bluetooth, charge before first use, adjust fit for comfort

[4/5] What makes this product different from others on the market?
Your answer:

  ⏭️  Skipped

[5/5] Where can I buy this product?
Your answer: Available on our website and Amazon, shipping worldwide

🤖 AI is generating content ideas (model: deepseek-v3.1:671b-cloud)...

💡 Content Ideas (Round 1)
----------------------------------------------------------------------

  1. How Wireless Headphones Transform Your Daily Commute
     → Guide on using wireless headphones for commuting with noise cancellation and battery tips for all-day use.

  2. The Ultimate Guide to Choosing Wireless Headphones for Fitness
     → Complete buying guide for fitness enthusiasts covering sweat resistance, secure fit, and workout-friendly features.

  3. 48-Hour Battery Life: Never Run Out of Music Again
     → In-depth analysis of extended battery performance, charging tips, and real-world usage scenarios for travelers.

  4. Active Noise Cancellation Explained: Why It Matters for Remote Work
     → Technical guide on ANC technology benefits for productivity, focus, and reducing distractions in home offices.

  5. How to Properly Pair and Set Up Your Wireless Headphones
     → Step-by-step tutorial covering Bluetooth pairing, optimal settings, and troubleshooting common connection issues.
  ...

======================================================================
📋 Options: [u] User2AI Mode, [a] AI2AI Mode, [s] Save, [q] Quit
======================================================================
Your choice (u/a/s/q): s

✓ Progress saved! (out_content_ideas.json)

Your choice (u/a/s/q): u
```

---

## Configuration

Create a `.env` file with your Ollama API key:

```env
# Required: Customer agent API key
OLLAMA_API_KEY=your_api_key_here

# Optional: Separate configuration for salesman agent in AI2AI mode
# If not set, uses OLLAMA_API_KEY and OLLAMA_MODEL
OLLAMA_API_KEY_SALESMAN=your_api_key_here
OLLAMA_MODEL_SALESMAN=minimax-m2:cloud
```

### AI2AI Mode Setup

To use AI2AI mode:

1. Create/edit `out/context.md` with your product information
2. Configure salesman agent in `.env` (optional, uses customer settings if not set)
3. Select `[a] AI2AI Mode` from the main menu

The `out/context.md` file should contain comprehensive product details that the salesman agent will use to answer questions. A template is provided in the file.

**For all configuration options and available models, see [SPEC.md](./spec/SPEC.md)**

---

## Output Format


All session data is saved to `out/content_ideas.json` in structured JSON format:

```
{
   "product_name": "...",
   "rounds": ...,
   "qa_history": [
      { "round": 1, "question": "...", "answer": "...", "timestamp": "..." },
      ...
   ],
   "content_ideas": [
      { "title": "...", "summary": "..." },
      ...
   ],
   "last_updated": "..."
}
```

**For detailed output format specification, see [SPEC.md](./spec/SPEC.md)**



---

## Troubleshooting

### API Not Working?

If you see API errors:

1. Check your `.env` file has valid `OLLAMA_API_KEY`
2. Get/verify API key at [ollama.com](https://ollama.com/)
3. Check internet connection

The application will show a help menu and allow you to continue even if the API is unavailable.

### uv Command Not Found?

Install uv following the instructions at [docs.astral.sh/uv/](https://docs.astral.sh/uv/)

### Python Version Issues?

This project requires Python 3.13+. Check your version:

```bash
python --version
```

uv can manage Python versions for you:

```bash
uv python install 3.13
```

### Tests Failing?

Ensure all dependencies are installed:

```bash
uv sync --extra dev
uv run pytest src/tests/ -v
```

## Requirements

- Python 3.13+
- Ollama Cloud API key (free at [ollama.com](https://ollama.com/))
- Internet connection for AI features

**For detailed technical specifications, see [SPEC.md](./spec/SPEC.md)**

---

## License

MIT

---

## Contributing

Contributions are welcome! Please see [SPEC.md](./spec/SPEC.md) for coding standards and technical requirements.

---

## Support

For issues, questions, or contributions, please refer to the project repository.

Get your Ollama API key: [ollama.com](https://ollama.com/)  
Learn more about uv: [docs.astral.sh/uv/](https://docs.astral.sh/uv/)
