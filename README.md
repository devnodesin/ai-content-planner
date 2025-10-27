# Content Planner

An interactive Python command-line application for AI-powered content idea generation for e-commerce products.

**The AI acts as a curious customer**, asking genuine questions without assumptions, helping you understand what information your customers need.

Built with Python 3.13 and managed with [uv](https://docs.astral.sh/uv/) for fast, reliable dependency management.

## Features

- 🤖 **AI-powered customer perspective** - AI acts like a real customer encountering your product
- ❓ **Natural question generation** - Questions use what, who, which, whose, when, why, where, how
- ⏭️  **Skip questions** - Press Enter to skip any question you don't want to answer
- 💡 **Structured content ideas** - Generate article titles with detailed summaries (100-150 chars)
- 🚫 **Smart deduplication** - No duplicate or similar content ideas (70%+ similarity filtered)
- 🎨 **Colorful interface** - Easy-to-read colored output (menu, questions, outputs, success messages)
- 🤖 **AI thinking indicator** - See "AI Thinking..." with progress dots during generation
- 💾 **Auto-save** every 5 minutes (silent background)
- 📝 **Manual save** with 's' key (returns to menu, not questions)
- 🔄 **Iterative rounds** - Each round builds on previous answers
- 📊 **JSON export** for easy integration
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

```bash
uv sync
```

### 3. Configure API Key

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Ollama API key from https://ollama.com
```

### 4. Run the App

```bash
uv run python main.py
```

---

## How It Works

The AI acts as a **smart customer evaluating a product before purchase**. This helps you:

- Understand what questions real customers ask before buying
- Identify information gaps in your product descriptions
- Generate content that moves customers toward purchase decisions
- Build comprehensive product knowledge iteratively
- Create high-quality content optimized for buyers, search engines, and AI assistants

### First Round Questions

The AI asks basic customer questions using various question types:
- **What** is this product used for?
- **Who** is this product designed for?
- **How** do I use this product properly?
- **What** makes this product different from others?
- **What** sizes, colors, or versions are available?
- **Where** can I buy this product?
- **When** will it be available?
- **Why** should I choose this product?
- **How much** does it cost?

### Follow-Up Rounds - Smart Question Strategy

Each subsequent round uses intelligent question selection:

1. **Follow-up questions IF there's a valid doubt or unclear information** from previous answers
2. **Explore NEW unexplored areas** that move toward a purchase decision:
   - Value proposition and benefits
   - Practical usage and compatibility
   - Pricing, warranty, and guarantees
   - Social proof and reviews
   - Comparison with alternatives
   - Post-purchase support
   - Risk mitigation (returns, trials, etc.)

The AI **never re-asks clearly answered questions** and **never makes assumptions** - it only explores what helps make a buying decision.

### Content Ideas - High-Quality & Unique

Generated content titles are:
- ✅ **Unique** - No duplicates or similar ideas (70%+ similarity filtered)
- ✅ **High-performing** - Optimized for conversions
- ✅ **Multi-audience** - Appeals to new buyers, search engines, and AI assistants
- ✅ **Buyer journey focused** - Addresses awareness, consideration, and decision stages
- ✅ **Action-oriented** - Specific, clickable, SEO-friendly titles

---

## Usage

1. **Enter Product Name** - Type your product name (e.g., "Wireless Headphones")
2. **Answer Customer Questions** - Respond to 5 AI-generated questions from a customer perspective
3. **Review Content Ideas** - Get 10 article title ideas that address customer concerns
4. **Choose Action**:
   - `c` - Continue with more questions (AI asks follow-up questions based on your answers)
   - `q` - Quit and save all data to `out.json`
   - `s` - Save current progress (returns to menu, not questions)

### Example Session

```bash
🎯 Content Planner - Product Input
==============================================================================

Enter product name: Wireless Headphones

🤖 AI Thinking...

📝 Questions & Answers
----------------------------------------------------------------------

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

🤖 AI Thinking...

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

📋 Options:
==============================================================================
  [c] Continue - Generate more questions
  [q] Quit - Save and exit
  [s] Save - Save current progress
==============================================================================
Your choice (c/q/s): s

✓ Progress saved!

Your choice (c/q/s): c
```

---

## Configuration

All settings can be customized via environment variables in `.env`:

```env
# Required
OLLAMA_API_KEY=your_api_key_here

# Optional (with defaults)
OLLAMA_MODEL=deepseek-v3.1:671b-cloud
MAX_QUESTIONS_PER_ROUND=5
CONTENT_IDEAS_PER_ROUND=10
AUTOSAVE_INTERVAL_SECONDS=300
```

### Available Ollama Cloud Models

- `deepseek-v3.1:671b-cloud` (default, recommended)
- `gpt-oss:20b-cloud`
- `gpt-oss:120b-cloud`
- `kimi-k2:1t-cloud`
- `qwen3-coder:480b-cloud`
- `glm-4.6:cloud`

---

## Output Format

All session data is saved to `out.json`:

```json
{
  "product_name": "Wireless Headphones",
  "rounds": 2,
  "qa_history": [
    {
      "round": 1,
      "question": "What problem does this product solve?",
      "answer": "Eliminates tangled wires and enables mobility",
      "timestamp": "2025-01-27T12:00:00"
    }
  ],
  "content_ideas": [
    {
      "title": "How Wireless Headphones Transform Your Daily Commute",
      "summary": "Comprehensive guide on using wireless headphones for commuting, covering noise cancellation, battery life tips, and best practices."
    },
    {
      "title": "Top 5 Benefits of Going Wireless for Fitness Enthusiasts",
      "summary": "Explore key advantages of wireless headphones during workouts, including freedom of movement and sweat resistance features."
    }
  ],
  "last_updated": "2025-01-27T12:30:00"
}
```

---

## Development

### Run Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_session.py -v
```

### Add Dependencies

```bash
# Add runtime dependency
uv add package-name

# Add dev dependency
uv add --dev package-name
```

### Update Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update specific package
uv add package-name@latest
```

---

## Project Structure

```
content-planner/
├── agents/              # Workflow orchestration
│   ├── planner.py       # Main content planner agent
│   └── session.py       # Session management & autosave
├── ai/                  # AI integration
│   └── client.py        # Ollama Cloud API client
├── ui/                  # User interface
│   └── console.py       # Console-based UI
├── utils/               # Utilities
│   └── config.py        # Configuration management
├── tests/               # Test suite (11 tests)
│   ├── test_ai.py
│   ├── test_config.py
│   └── test_session.py
├── main.py              # Application entry point
├── pyproject.toml       # Project configuration
├── .env.example         # Environment template
└── README.md            # This file
```

---

## Technology Stack

- **Python**: 3.13.3 (latest stable version for 2025)
- **Package Manager**: [uv](https://docs.astral.sh/uv/) (10-100x faster than pip)
- **Dependencies**: 
  - `ollama` - AI integration with Ollama Cloud
  - `python-dotenv` - Environment variable management
  - `pytest` - Testing framework

### Why uv?

[uv](https://docs.astral.sh/uv/) is a blazingly fast Python package installer and resolver:

- 🚀 **10-100x faster** than pip
- 🔒 **Reliable** dependency resolution with lock files
- 📦 **All-in-one** tool (replaces pip, virtualenv, pip-tools)
- 🎯 **Drop-in replacement** for existing workflows
- 💾 **Disk space efficient** with global cache

### Why Python 3.13?

- Latest stable release (supported until October 2029)
- Best performance and security for production in 2025
- Modern language features and improvements

---

## Architecture

### Core Components

**AI Client** (`ai/client.py`)
- Handles all Ollama Cloud API interactions
- Generates questions based on product and context
- Creates content ideas from Q&A sessions
- Graceful degradation when API is unavailable

**Session Manager** (`agents/session.py`)
- Manages application state
- Handles JSON persistence
- Background autosave thread (every 5 minutes)
- Tracks Q&A history and content ideas

**Content Planner Agent** (`agents/planner.py`)
- Orchestrates the main workflow
- Coordinates between AI, UI, and session components
- Implements iterative Q&A rounds

**Console UI** (`ui/console.py`)
- User input/output handling
- Help menu and error displays
- Formatted output for questions and ideas

**Configuration** (`utils/config.py`)
- Environment variable management
- Default values and validation
- API availability checks

### Design Principles

- **Modular Design**: Separate concerns (AI, UI, session, config)
- **Type Hints**: Full type annotations for maintainability
- **Threading**: Background autosave without blocking UI
- **Graceful Degradation**: Works even if API fails
- **PEP 8 Compliant**: Follows Python coding standards

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
uv run pytest tests/ -v
```

---

## Security

- ✅ No secrets in code
- ✅ Environment variables for sensitive data
- ✅ `.env` in `.gitignore`
- ✅ Input validation and sanitization
- ✅ Secure API key handling

---

## Requirements

- Python 3.13+
- Ollama Cloud API key (free at [ollama.com](https://ollama.com/))
- Internet connection for AI features

---

## License

MIT

---

## Contributing

Contributions are welcome! Please ensure:

- Code follows PEP 8 standards
- All tests pass (`uv run pytest tests/ -v`)
- Type hints are included
- Docstrings are added for new functions
- Security best practices are followed

---

## Support

For issues, questions, or contributions, please refer to the project repository.

Get your Ollama API key: [ollama.com](https://ollama.com/)  
Learn more about uv: [docs.astral.sh/uv/](https://docs.astral.sh/uv/)
