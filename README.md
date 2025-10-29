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
- 🎨 **Colorful interface** - Easy-to-read colored output (menu, questions, outputs, success messages)
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
# Install pytest
uv add --dev pytest

# Run all tests
uv run pytest src/tests/ -v

# Run specific test file
uv run pytest src/tests/test_session.py -v
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

On startup, if an existing session file (`out_content_ideas.json`) is found, you'll see:

```bash
📂 Existing Session Found
----------------------------------------------------------------------

Product/Topic: Wireless Headphones
Rounds Completed: 3
Q&A Pairs: 15
Content Ideas: 30
Last Updated: 2025-01-27T10:30:00

📂 Session Resume
==============================================================================
  ▶ Load existing session: Wireless Headphones
    Start a new session with a new product
==============================================================================

Use ↑/↓ arrow keys to navigate, Enter to select, Esc to exit
```

- **Navigate** with arrow keys (↑/↓)
- **Select** with Enter
- **Exit** with Esc (confirms before exiting)

### Main Workflow

1. **Enter Product Name** - Type your product name (e.g., "Wireless Headphones")
2. **Answer Customer Questions** - Respond to 5 AI-generated questions from a customer perspective
3. **Review Content Ideas** - Get 10 article title ideas that address customer concerns
4. **Choose Action**:
   - `c` - Continue with more questions (AI asks follow-up questions based on your answers)
   - `q` - Quit and save all data to `out_content_ideas.json`
   - `s` - Save current progress (returns to menu, not questions)

### Example Session

```bash
🎯 Content Planner - Product Input
==============================================================================

Enter product name: Wireless Headphones

🤖 AI is generating questions (model: deepseek-v3.1:671b-cloud)...

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
📋 Options: [c] Continue, [s] Save, [q] Quit
======================================================================
Your choice (c/q/s): s

✓ Progress saved! (out_content_ideas.json)

Your choice (c/q/s): c
```

---

## Configuration

Create a `.env` file with your Ollama API key:

```env
OLLAMA_API_KEY=your_api_key_here
```

**For all configuration options and available models, see [SPEC.md](./spec/SPEC.md)**

---

## Output Format


All session data is saved to `out_content_ideas.json` in structured JSON format:

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
