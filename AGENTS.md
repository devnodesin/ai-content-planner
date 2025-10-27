# AGENTS.md

For all workflow, technical requirements, and implementation details, refer to [`REQUIRMENTS.md`](./REQUIRMENTS.md).

## Agent Guidance
- Follow the workflow and architecture described in `REQUIRMENTS.md`.
- Use the latest Python best practices.
- Always leverage AI for question and idea generation.
- Periodically autosave session data if the user works for a long time.
- On quit, save all session data to `out_content_ideas.json`.
- On continue, generate more questions based on context and user input.

## Folder Structure
Recommended project structure:
```
content-planner/
├── agents/        # Agent logic and workflow
├── ai/            # AI integration and question generation
├── ui/            # Console UI/UX logic
├── utils/         # Utility functions
├── main.py        # Main entry point
├── requirements.txt
├── out_content_ideas.json       # Output file for session data
├── AGENTS.md
├── REQUIRMENTS.md
```

## Coding Rules
- Follow PEP 8 for Python code style
- Use type hints and docstrings for all functions and classes
- Prefer modern Python features (f-strings, pathlib, dataclasses, etc.)
- Organize code into logical modules as shown in the folder structure
- Use descriptive variable and function names
- Do not store secrets or API keys in code; always use environment variables.
- Validate and sanitize all user input.
- Handle errors gracefully, especially with external API calls.

### Testing
Refer to [`REQUIRMENTS.md`](./REQUIRMENTS.md) for detailed testing instructions and requirements.

## Anti-Patterns / Do Nots
- Do not duplicate requirements or workflow details already present in `REQUIRMENTS.md`.
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
- For all workflow, technical requirements, and implementation details, refer to [`REQUIRMENTS.md`](./REQUIRMENTS.md).
- For more on AGENTS.md conventions, see [agents.md](https://agents.md/) and [agentdotmd.github.io](https://agentdotmd.github.io/website/)
