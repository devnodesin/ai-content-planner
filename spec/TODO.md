## I want to do below modifications 

1. move `generate_context.py` under `tools` dir
2. `generate_context.py` should remove html tags like:  header, footer, aside, sidebar, nav etc.. only inlcude the pages main content to `context_input.md`


## Reorg and cleanup 

- can we move `examples/*` and `vacuum_context.md` -> `under tests/test_data`
- implmentation spefication thing like requriments should bem oved under `spec` dir, consolidated `docs\GENERATE_CONTEXT_IMPLEMENTATION.md` `docs\GENERATE_CONTEXT_QUICK_REF.md`


## Context Support: Markdown File

- If a markdown file named `context_input.md` is present and valid, use its content as context for answering questions instead of manual user input.
- On startup, the application should check for a valid `context_input.md`.
- If the file exists and is valid, prompt the user:
  - Option 1: Load context from the markdown file and continue with the existing product/topic.
  - Option 2: Start a new session with a new product and context.

## Application Modes: AI2AI and AI2User

- Support two modes of operation:
  - **AI2User**: The current workflow, where the user interacts with the AI as a customer.
  - **AI2AI**: An automated chat system where one AI acts as a salesperson and the other as a customer.

### AI2AI Mode Requirements

1. **Role Assignment**: Each AI agent is assigned a distinct persona:
   - Salesperson: Uses product-specific context from a file.
   - Customer: Uses present-day context, profile, needs, and possible objections.
2. **Context Injection**:
   - Salesperson AI receives product information, FAQs, and selling points.
   - Customer AI receives a profile and possible questions/objections.
3. **Conversation Loop**:
   - Agents interact in a turn-based dialogue.
   - Salesperson AI informs, persuades, and addresses concerns.
   - Customer AI asks questions, expresses doubts, and makes decisions.
4. **AI Models**:
   - Both agents use language models (e.g., GPT, Ollama) with role-specific context prompts.
   - Responses are generated based on roles and evolving conversation.
5. **Session Management**:
   - Track the conversation, save session data, and analyze outcomes (e.g., successful sale, objections, information gaps).
6. **Applications**:
   - Training, testing sales scripts, generating realistic Q&A datasets, simulating customer interactions for product development.
