"""Console UI/UX for the content planner application."""

import sys
import time
from typing import List, Optional


class Colors:
    """ANSI color codes for terminal output."""
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class ConsoleUI:
    """Console-based user interface with colors."""

    @staticmethod
    def clear_screen():
        """Clear the console screen."""
        print('\n' * 2)

    @staticmethod
    def print_header(text: str):
        """Print a formatted header."""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 70}")
        print(f"  {text}")
        print(f"{'=' * 70}{Colors.RESET}\n")

    @staticmethod
    def print_section(text: str):
        """Print a section divider."""
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'-' * 70}")
        print(f"  {text}")
        print(f"{'-' * 70}{Colors.RESET}\n")

    @staticmethod
    def print_info(text: str):
        """Print informational text."""
        print(f"{Colors.BRIGHT_BLUE}ℹ  {text}{Colors.RESET}")

    @staticmethod
    def print_success(text: str):
        """Print success message in green."""
        print(f"{Colors.BRIGHT_GREEN}{Colors.BOLD}✓ {text}{Colors.RESET}")

    @staticmethod
    def print_error(text: str):
        """Print error message in red."""
        print(f"{Colors.BRIGHT_RED}{Colors.BOLD}✗ {text}{Colors.RESET}")

    @staticmethod
    def print_warning(text: str):
        """Print warning message in yellow."""
        print(f"{Colors.BRIGHT_YELLOW}⚠  {text}{Colors.RESET}")
    
    @staticmethod
    def print_ai_thinking(text: str = "AI Thinking"):
        """Print AI thinking message with animation."""
        print(f"{Colors.BRIGHT_MAGENTA}🤖 {text}", end='', flush=True)
        for _ in range(3):
            time.sleep(0.3)
            print('.', end='', flush=True)
        print(f"{Colors.RESET}")
    
    @staticmethod
    def print_question(number: int, total: int, question: str):
        """Print a question in a distinct color."""
        print(f"\n{Colors.YELLOW}{Colors.BOLD}[{number}/{total}] {question}{Colors.RESET}")
    
    @staticmethod
    def print_menu_option(key: str, description: str):
        """Print a menu option."""
        print(f"  {Colors.CYAN}{Colors.BOLD}[{key}]{Colors.RESET} {Colors.WHITE}{description}{Colors.RESET}")

    @staticmethod
    def get_input(prompt: str, allow_empty: bool = False) -> str:
        """
        Get user input with validation.
        
        Args:
            prompt: Prompt to display
            allow_empty: Whether to allow empty input
            
        Returns:
            User input string
        """
        while True:
            try:
                user_input = input(f"{Colors.WHITE}{prompt}{Colors.RESET}: ").strip()
                if user_input or allow_empty:
                    return user_input
                print(f"{Colors.DIM}Input cannot be empty. Please try again.{Colors.RESET}")
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n{Colors.BRIGHT_CYAN}👋 Goodbye!{Colors.RESET}")
                sys.exit(0)

    @staticmethod
    def get_product_name() -> str:
        """Get product name from user."""
        ConsoleUI.print_header("🎯 Content Planner - Product Input")
        return ConsoleUI.get_input("Enter product name")

    @staticmethod
    def display_questions(questions: List[str]) -> List[str]:
        """
        Display questions and collect answers.
        Allows skipping questions by pressing Enter without input.
        
        Args:
            questions: List of questions to ask
            
        Returns:
            List of answers (empty string for skipped questions)
        """
        answers = []
        ConsoleUI.print_section("📝 Questions & Answers")
        
        print(f"{Colors.DIM}💡 Tip: Press Enter without typing to skip a question{Colors.RESET}\n")
        
        for i, question in enumerate(questions, 1):
            ConsoleUI.print_question(i, len(questions), question)
            answer = ConsoleUI.get_input("Your answer", allow_empty=True)
            
            if not answer:
                print(f"{Colors.DIM}  ⏭️  Skipped{Colors.RESET}")
            
            answers.append(answer)
        
        return answers

    @staticmethod
    def display_content_ideas(ideas: List, round_num: int):
        """
        Display generated content ideas.
        
        Args:
            ideas: List of content ideas (dict with title and summary)
            round_num: Current round number
        """
        ConsoleUI.print_section(f"💡 Content Ideas (Round {round_num})")
        
        if not ideas:
            ConsoleUI.print_warning("No content ideas generated.")
            return
        
        for i, idea in enumerate(ideas, 1):
            # Handle both old format (string) and new format (dict)
            if isinstance(idea, dict):
                title = idea.get('title', idea)
                summary = idea.get('summary', '')
                print(f"\n  {Colors.BRIGHT_WHITE}{Colors.BOLD}{i}. {title}{Colors.RESET}")
                if summary:
                    print(f"     {Colors.DIM}→ {summary}{Colors.RESET}")
            else:
                print(f"  {Colors.BRIGHT_WHITE}{i}. {idea}{Colors.RESET}")

    @staticmethod
    def get_user_choice() -> str:
        """
        Get user's choice to continue or quit.
        
        Returns:
            User choice: 'c', 'q', or 's'
        """
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 70}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}📋 Options:{Colors.RESET}")
        ConsoleUI.print_menu_option('c', 'Continue - Generate more questions')
        ConsoleUI.print_menu_option('q', 'Quit - Save and exit')
        ConsoleUI.print_menu_option('s', 'Save - Save current progress')
        print(f"{Colors.CYAN}{Colors.BOLD}{'=' * 70}{Colors.RESET}")
        
        while True:
            choice = ConsoleUI.get_input("Your choice (c/q/s)", allow_empty=True).lower()
            if choice in ['c', 'q', 's']:
                return choice
            if not choice:
                continue
            ConsoleUI.print_error("Invalid choice. Please enter 'c', 'q', or 's'.")

    @staticmethod
    def show_help_menu():
        """Display help menu with all available commands."""
        ConsoleUI.print_header("❓ Help Menu")
        print(f"{Colors.BRIGHT_WHITE}Available Commands:{Colors.RESET}")
        ConsoleUI.print_menu_option('c', 'Continue to next round (generate more questions)')
        ConsoleUI.print_menu_option('q', 'Quit and save all data to out_content_ideas.json')
        ConsoleUI.print_menu_option('s', 'Save current progress without quitting')
        print(f"\n{Colors.BRIGHT_WHITE}Features:{Colors.RESET}")
        print(f"  {Colors.DIM}• Auto-save every 5 minutes (silent background){Colors.RESET}")
        print(f"  {Colors.DIM}• Up to 5 questions per round{Colors.RESET}")
        print(f"  {Colors.DIM}• AI-powered question and content idea generation{Colors.RESET}")
        print(f"\n{Colors.BRIGHT_WHITE}Configuration:{Colors.RESET}")
        print(f"  {Colors.DIM}• Set OLLAMA_API_KEY in .env file{Colors.RESET}")
        print(f"  {Colors.DIM}• Set OLLAMA_MODEL in .env (default: deepseek-v3.1:671b-cloud){Colors.RESET}")
        print(f"\n{Colors.CYAN}{'=' * 70}{Colors.RESET}\n")

    @staticmethod
    def show_api_error():
        """Display API configuration error and help."""
        ConsoleUI.print_error("Ollama API is not configured or unavailable!")
        print("\nTo fix this:")
        print("  1. Create a .env file (copy from .env.example)")
        print("  2. Get API key from https://ollama.com")
        print("  3. Set OLLAMA_API_KEY in .env file")
        print("  4. Optionally set OLLAMA_MODEL (default: deepseek-v3.1:671b-cloud)")
        ConsoleUI.show_help_menu()
