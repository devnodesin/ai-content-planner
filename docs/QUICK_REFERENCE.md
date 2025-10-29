# Quick Reference - After Reorganization

## 🚀 Quick Start Commands

### Running the Application
```bash
# From root directory (recommended)
uv run python run.py

# Alternative: from src directory
cd src && uv run python main.py
```

### Testing
```bash
# Run all tests
uv run pytest src/tests/ -v

# Run specific test
uv run pytest src/tests/test_session.py -v

# Run with coverage
uv add --dev pytest-cov
uv run pytest src/tests/ --cov=src --cov-report=html
```

### Development
```bash
# Install/sync dependencies
uv sync

# Add package
uv add package-name

# Add dev package
uv add --dev package-name
```

## 📁 Where Things Are Now

| Old Location | New Location |
|--------------|--------------|
| `main.py` | `src/main.py` |
| `agents/` | `src/agents/` |
| `ai/` | `src/ai/` |
| `ui/` | `src/ui/` |
| `utils/` | `src/utils/` |
| `tests/` | `src/tests/` |

## 🔧 Import Paths

All imports remain the same (relative imports still work):
```python
from agents import ContentPlannerAgent
from ai import AIClient
from ui import ConsoleUI
from utils.config import Config
```

## ⚙️ Configuration Files Updated

- `pyproject.toml` - Updated package paths and test configuration
- `AGENTS.md` - Updated folder structure and commands
- `spec/SPEC.md` - Updated project structure
- `README.md` - Updated all commands

## 📝 Notes

- The `run.py` launcher automatically configures Python paths
- All 14 tests pass with the new structure
- No code changes required - only directory reorganization
- Output file (`out_content_ideas.json`) stays at root level
