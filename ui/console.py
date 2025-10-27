"""Console UI/UX for the content planner application."""

import sys
from typing import List, Optional


class ConsoleUI:
    """Console-based user interface."""

    @staticmethod
    def clear_screen():
        """Clear the console screen."""
        # Simple approach without external dependencies
        print('\n' * 2)

    @staticmethod
    def print_header(text: str):
        """Print a formatted header."""
        print(f"\n{'=' * 70}")
        print(f"  {text}")
        print(f"{'=' * 70}\n")

    @staticmethod
    def print_section(text: str):
        """Print a section divider."""
        print(f"\n{'-' * 70}")
        print(f"  {text}")
        print(f"{'-' * 70}\n")

    @staticmethod
    def print_info(text: str):
        """Print informational text."""
        print(f"ℹ  {text}")

    @staticmethod
    def print_success(text: str):
        """Print success message."""
        print(f"✓ {text}")

    @staticmethod
    def print_error(text: str):
        """Print error message."""
        print(f"✗ {text}")

    @staticmethod
    def print_warning(text: str):
        """Print warning message."""
        print(f"⚠ {text}")

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
                user_input = input(f"{prompt}: ").strip()
                if user_input or allow_empty:
                    return user_input
                print("Input cannot be empty. Please try again.")
            except (KeyboardInterrupt, EOFError):
                print("\n\nExiting...")
                sys.exit(0)

    @staticmethod
    def get_product_name() -> str:
        """Get product name from user."""
        ConsoleUI.print_header("Content Planner - Product Input")
        return ConsoleUI.get_input("Enter product name")

    @staticmethod
    def display_questions(questions: List[str]) -> List[str]:
        """
        Display questions and collect answers.
        
        Args:
            questions: List of questions to ask
            
        Returns:
            List of answers
        """
        answers = []
        ConsoleUI.print_section("Questions & Answers")
        
        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}] {question}")
            answer = ConsoleUI.get_input("Your answer")
            answers.append(answer)
        
        return answers

    @staticmethod
    def display_content_ideas(ideas: List[str], round_num: int):
        """
        Display generated content ideas.
        
        Args:
            ideas: List of content ideas
            round_num: Current round number
        """
        ConsoleUI.print_section(f"Content Ideas (Round {round_num})")
        
        if not ideas:
            ConsoleUI.print_warning("No content ideas generated.")
            return
        
        for i, idea in enumerate(ideas, 1):
            print(f"  {i}. {idea}")

    @staticmethod
    def get_user_choice() -> str:
        """
        Get user's choice to continue or quit.
        
        Returns:
            User choice: 'c', 'q', or 's'
        """
        print(f"\n{'=' * 70}")
        print("Options:")
        print("  [c] Continue - Generate more questions")
        print("  [q] Quit - Save and exit")
        print("  [s] Save - Save current progress")
        print(f"{'=' * 70}")
        
        while True:
            choice = ConsoleUI.get_input("Your choice (c/q/s)", allow_empty=True).lower()
            if choice in ['c', 'q', 's']:
                return choice
            if not choice:
                continue
            print("Invalid choice. Please enter 'c', 'q', or 's'.")

    @staticmethod
    def show_help_menu():
        """Display help menu with all available commands."""
        ConsoleUI.print_header("Help Menu")
        print("Available Commands:")
        print("  c  - Continue to next round (generate more questions)")
        print("  q  - Quit and save all data to out.json")
        print("  s  - Save current progress without quitting")
        print("\nFeatures:")
        print("  • Auto-save every 5 minutes (silent background)")
        print("  • Up to 5 questions per round")
        print("  • AI-powered question and content idea generation")
        print("\nConfiguration:")
        print("  • Set OLLAMA_API_KEY in .env file")
        print("  • Set OLLAMA_MODEL in .env (default: deepseek-v3.1:671b-cloud)")
        print(f"\n{'=' * 70}\n")

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
