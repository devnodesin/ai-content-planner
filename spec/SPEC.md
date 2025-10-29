# Content Planner - Technical Specification

This document contains the detailed technical specifications, architecture, design decisions, and requirements for the Content Planner application.

## Requirements & Workflow

This project is an interactive Python application for idea generation to assist content writing for an e-commerce company.

### Workflow

#### Step 0: Session Resume (Optional)
- On startup, if a previous session exists (`out_content_ideas.json`), the application displays a summary showing:
  - Product name
  - Number of rounds completed
  - Q&A pairs count
  - Content ideas count
  - Last updated timestamp
- An interactive menu with arrow key navigation allows the user to:
  - **Load existing session**: Resume where you left off
  - **Start new session**: Begin with a new product
- If no previous session exists, proceed directly to Step 1.

#### Step 1: Enter Product Name
- The user enters a product name (`$PRODUCT`).
- The application uses Ollama Cloud to generate customer questions about the product.
- The number of questions per round is controlled by `MAX_QUESTIONS_PER_ROUND` in the config (default: 5).
- Questions use diverse prompts: what, who, which, whose, when, why, where, how.

#### Step 2: Interactive Q&A
- The user answers the generated questions interactively (up to `MAX_QUESTIONS_PER_ROUND` per round).
- **Skip Feature**: Press Enter without typing to skip any question.
- Only answered questions are saved; skipped questions are ignored.

#### Step 3: Content Idea Generation
- Based on the user's answers, the application generates content/article ideas (titles and summaries).
- Content ideas are unique, deduplicated (no similar ideas above 70% similarity).
- Returned in JSON format: `{ "title": ..., "summary": ... }`.
- Designed to attract humans, search engines, and AI systems.

#### Follow-Up Rounds & Smart Questioning
- After each round, the user can:
  - Press `c` to **continue**: Generate more questions based on previous Q&A context, focusing on follow-up questions for unclear areas and exploring new, unexplored product aspects.
  - Press `s` to **save**: Save current progress without quitting.
  - Press `q` to **quit**: Save all data to `out_content_ideas.json` and exit.
- The AI never re-asks clearly answered questions, never makes assumptions, and only asks what helps make a buying decision.
- **Autosave**: Background autosave every 5 minutes (default, configurable via `AUTOSAVE_INTERVAL_SECONDS`).

### Technical Requirements
- Use Python best practices and latest trends.
- Use `uv` for dependency management and virtual environment setup.
- Implement a high-quality, console-based UI/UX.
- Leverage AI for question and idea generation using Ollama Cloud API.
- Integrate Ollama Cloud for AI models:
  - Create an account at [ollama.com](https://ollama.com/).
  - Generate an API key and set the environment variable `OLLAMA_API_KEY`.
  - Supported cloud models include: `deepseek-v3.1:671b-cloud`, `gpt-oss:20b-cloud`, `gpt-oss:120b-cloud`, `kimi-k2:1t-cloud`, `qwen3-coder:480b-cloud`, `glm-4.6:cloud`.
  - Install the Python library: `pip install ollama`
  - Example usage:
  ```python
  import os
  from ollama import Client
  client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
  )
  messages = [
    {
      'role': 'user',
      'content': 'Why is the sky blue?',
    },
  ]
  for part in client.chat('gpt-oss:120b', messages=messages, stream=True):
    print(part['message']['content'], end='', flush=True)
  ```

## Architecture

### Core Components

**AI Client** (`ai/client.py`)

- Handles all Ollama Cloud API interactions
- Generates questions based on product and context
- Creates content ideas from Q&A sessions
- Graceful degradation when API is unavailable

**Session Manager** (`agents/session.py`)

- Manages application state
- Handles JSON persistence (load/save)
- Background autosave thread (configurable interval, default 5 minutes)
- Tracks Q&A history and content ideas
- Session resume with summary display
- Intelligent deduplication (70% similarity threshold)

**Content Planner Agent** (`agents/planner.py`)

- Orchestrates the main workflow
- Coordinates between AI, UI, and session components
- Implements iterative Q&A rounds
- Handles session resume logic
- Manages user choices (continue, save, quit)

**Console UI** (`ui/console.py`)

- User input/output handling with color-coded output
- Interactive menus with arrow key navigation (cross-platform)
- Help menu and error displays
- Formatted output for questions and ideas
- AI thinking indicators with model name
- Session summary display

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
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **User-Friendly**: Color-coded output, arrow key navigation, skip options

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

## How It Works - Detailed Specification

The AI acts as a **smart customer evaluating a product before purchase**. This helps you:

- Understand what questions real customers ask before buying
- Identify information gaps in your product descriptions
- Generate content that moves customers toward purchase decisions
- Build comprehensive product knowledge iteratively
- Create high-quality content optimized for buyers, search engines, and AI assistants

### Session Resume

- On startup, the application checks for an existing session file (`out_content_ideas.json`).
- If found, displays a summary with product name, progress statistics, and last update time.
- Interactive menu (arrow key navigation) offers two options:
  1. **Resume existing session** - Continue from where you left off
  2. **Start new session** - Begin with a new product (previous session preserved)
- Session data includes all Q&A history, content ideas, and round count.

### First Round Questions

- The AI asks basic customer questions using various question types (what, who, which, whose, when, why, where, how).
- Example questions:
    - "What is this product used for?"
    - "Who is this product designed for?"
    - "How to use this product?"
    - "Where can I buy this product?"
    - "What sizes/colors/versions are available?"
- Users can **skip questions** by pressing Enter without typing an answer.

### Follow-Up Rounds - Smart Question Strategy

- Each subsequent round uses intelligent question selection:
  1. **Follow-up questions ONLY if there's a valid doubt or unclear information** from previous answers
  2. **Explore NEW unexplored areas** that move toward a purchase decision:
     - Value proposition and benefits
     - Practical usage and compatibility
     - Pricing, warranty, and guarantees
     - Social proof and reviews
     - Comparison with alternatives
     - Post-purchase support
     - Risk mitigation (returns, trials, etc.)
- The AI never re-asks clearly answered questions, never makes assumptions, and only explores what helps make a buying decision.
- Questions are always numbered and returned as a list, with no commentary.

### User Controls

After each round, three options are available:
- **[c] Continue** - Generate more questions and content ideas
- **[s] Save** - Save current progress without quitting
- **[q] Quit** - Save all data and exit the application

Background autosave runs every 5 minutes (configurable) to prevent data loss.

### Content Ideas - High-Quality & Unique

- Generated content ideas are:
  - ✅ **Unique** - No duplicates or similar ideas (70%+ similarity filtered)
  - ✅ **High-performing** - Optimized for conversions
  - ✅ **Multi-audience** - Appeals to new buyers, search engines, and AI assistants
  - ✅ **Buyer journey focused** - Addresses awareness, consideration, and decision stages
  - ✅ **Action-oriented** - Specific, clickable, SEO-friendly titles
  - ✅ **JSON format** - Each idea is returned as `{ "title": ..., "summary": ... }` with summary 100-150 characters
  - ✅ **No commentary** - Only the ideas, no extra text

## Configuration Specification

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

## Output Format Specification

All session data is saved to `out_content_ideas.json`:

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

## Security Specifications

- ✅ No secrets in code
- ✅ Environment variables for sensitive data
- ✅ `.env` in `.gitignore`
- ✅ Input validation and sanitization
- ✅ Secure API key handling

## Testing Requirements

- Code follows PEP 8 standards
- All tests pass (`uv run pytest tests/ -v`)
- Type hints are included
- Docstrings are added for new functions
- Security best practices are followed

## Requirements

- Python 3.13+
- Ollama Cloud API key (free at [ollama.com](https://ollama.com/))
- Internet connection for AI features