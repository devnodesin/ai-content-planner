# AGENTS.md

For all workflow, technical requirements, and implementation details, refer to [`SPEC.md`](./spec/SPEC.md).

## Agent Guidance
- Follow the workflow and architecture described in `SPEC.md`.
- Use the latest Python best practices.
- Always leverage AI for question and idea generation using Ollama Cloud.
- Periodically autosave session data if the user works for a long time.
- On quit, save all session data to `out_content_ideas.json` (JSON format: product name, Q&A, content ideas).
- On continue, generate more questions based on previous Q&A context, focusing on follow-up and unexplored areas.

## Folder Structure
Recommended project structure:
```
ai-content-planner/
├── src/               # All source code
│   ├── agents/        # Agent logic and workflow
│   ├── ai/            # AI integration and question generation
│   ├── ui/            # Console UI/UX logic
│   ├── utils/         # Utility functions
│   ├── tests/         # Test suite
│   └── main.py        # Main entry point
├── docs/              # Documentation
├── spec/              # Specifications
├── tools/             # Utility tools (e.g., generate_context.py)
├── run.py             # Application launcher
├── pyproject.toml     # Project configuration
├── requirements.txt
└── out_content_ideas.json  # Output file for session data
```


## Coding Rules
- Always use [uv](https://docs.astral.sh/uv/) for building, running, testing, and managing dependencies in this project.
- All build, run, and test commands must use uv:
	- Install dependencies: `uv sync`
	- Run the app: `uv run python run.py` (or from src/: `uv run python main.py`)
	- Run all tests: `uv run pytest src/tests/ -v`
	- Run specific test file: `uv run pytest src/tests/test_session.py -v`
	- Add runtime dependency: `uv add package-name`
	- Add dev dependency: `uv add --dev package-name`
	- Update all dependencies: `uv sync --upgrade`
	- Update specific package: `uv add package-name@latest`
- Do not use pip, python -m pip, or other package managers for this project.
- Follow PEP 8 for Python code style
- Use type hints and docstrings for all functions and classes
- Prefer modern Python features (f-strings, pathlib, dataclasses, etc.)
- Organize code into logical modules as shown in the folder structure
- Use descriptive variable and function names
- Do not store secrets or API keys in code; always use environment variables.
- Validate and sanitize all user input.
- Handle errors gracefully, especially with external API calls and AI responses.

### Testing
Refer to [`SPEC.md`](./spec/SPEC.md) for detailed testing instructions, requirements, and output format.

## Anti-Patterns / Do Nots
- Do not duplicate requirements or workflow details already present in `SPEC.md`.
- Do not store secrets or API keys in code; always use environment variables.
- Do not ignore error handling, especially for external API calls.
- Do not bypass code style, linting, or testing requirements.
- Do not commit code without descriptive messages and proper review.

## Pull Request & Commit Guidelines
- Use descriptive commit messages.
- Run all tests before submitting PRs.
- Ensure code style and linting pass.
- Update tests for any code changes.

## Reference
-- For all workflow, technical requirements, and implementation details, refer to [`SPEC.md`](./spec/SPEC.md).
- For more on AGENTS.md conventions, see [agents.md](https://agents.md/) and [agentdotmd.github.io](https://agentdotmd.github.io/website/)
