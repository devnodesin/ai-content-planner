"""Console UI/UX for the content planner application."""

import sys
import time
from typing import List, Optional

# Fix Windows Unicode encoding (only if not in pytest)
if sys.platform == 'win32' and 'pytest' not in sys.modules:
    try:
        import io
        if hasattr(sys.stdout, 'buffer'):
            # line_buffering=True ensures output is flushed after each line
            # write_through=True ensures immediate write without buffering
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, 
                encoding='utf-8',
                line_buffering=True,
                write_through=True
            )
        if hasattr(sys.stderr, 'buffer'):
            sys.stderr = io.TextIOWrapper(
                sys.stderr.buffer, 
                encoding='utf-8',
                line_buffering=True,
                write_through=True
            )
    except (AttributeError, ValueError):
        pass  # Already wrapped or not needed

# Platform-specific keyboard input handling
if sys.platform == 'win32':
    import msvcrt
else:
    import tty
    import termios


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
        sys.stdout.flush()  # Ensure immediate display

    @staticmethod
    def print_section(text: str):
        """Print a section divider."""
        print(f"\n{Colors.BLUE}{Colors.BOLD}{'-' * 70}")
        print(f"  {text}")
        print(f"{'-' * 70}{Colors.RESET}\n")
        sys.stdout.flush()  # Ensure immediate display

    @staticmethod
    def print_info(text: str):
        """Print informational text."""
        print(f"{Colors.BRIGHT_BLUE}ℹ  {text}{Colors.RESET}")

    @staticmethod
    def print_success(text: str, file_name: Optional[str] = None):
        """Print success message in green."""
        if file_name:
            print(f"{Colors.BRIGHT_GREEN}{Colors.BOLD}✓ {text} ({file_name}){Colors.RESET}")
        else:
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
    def print_ai_thinking(text: str = "AI Thinking", model_name: Optional[str] = None):
        """Print AI thinking message with animation."""
        if model_name:
            print(f"{Colors.BRIGHT_MAGENTA}🤖 {text} (model: {model_name})", end='', flush=True)
        else:
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
            User choice: 'u', 'a', 'q', or 's'
        """
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 70}")
        print(f"📋 Options: [u] User2AI Mode, [a] AI2AI Mode, [s] Save, [q] Quit")
        print(f"{'=' * 70}{Colors.RESET}")
        
        while True:
            choice = ConsoleUI.get_input("Your choice (u/a/s/q)", allow_empty=True).lower()
            if choice in ['u', 'a', 'q', 's']:
                return choice
            if not choice:
                continue
            ConsoleUI.print_error("Invalid choice. Please enter 'u', 'a', 's', or 'q'.")

    @staticmethod
    def show_help_menu():
        """Display help menu with all available commands."""
        ConsoleUI.print_header("❓ Help Menu")
        print(f"{Colors.BRIGHT_WHITE}Available Commands:{Colors.RESET}")
        ConsoleUI.print_menu_option('u', 'User2AI Mode - Continue to next round (generate more questions)')
        ConsoleUI.print_menu_option('a', 'AI2AI Mode - Let AI generate questions and answers automatically')
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

    @staticmethod
    def _get_key():
        """
        Get a single keypress from the user (cross-platform).
        This function BLOCKS until a valid key is pressed.
        
        Returns:
            String representing the key pressed
        """
        if sys.platform == 'win32':
            # Windows - use msvcrt for raw key input (blocking)
            while True:
                # This blocks until a key is pressed
                key = msvcrt.getch()
                
                # Handle special keys (arrow keys, etc.)
                if key in (b'\x00', b'\xe0'):
                    # Extended key, read the second byte
                    key2 = msvcrt.getch()
                    if key2 == b'H':  # Up arrow
                        return 'up'
                    elif key2 == b'P':  # Down arrow
                        return 'down'
                    elif key2 == b'K':  # Left arrow
                        return 'left'
                    elif key2 == b'M':  # Right arrow
                        return 'right'
                    # Ignore other extended keys and continue waiting
                    continue
                elif key == b'\r':  # Enter (carriage return)
                    return 'enter'
                elif key == b'\n':  # Enter (line feed)
                    return 'enter'
                elif key == b'\x1b':  # Esc
                    return 'esc'
                elif key == b'\x03':  # Ctrl+C
                    raise KeyboardInterrupt
                else:
                    # Try to decode as UTF-8
                    try:
                        char = key.decode('utf-8', errors='ignore')
                        if char and char.isprintable():
                            return char
                        # Ignore non-printable characters and continue waiting
                        continue
                    except:
                        # If decode fails, ignore this key and continue waiting
                        continue
        else:
            # Unix/Linux/Mac
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                
                # Check for escape sequences (arrow keys)
                if ch == '\x1b':
                    # Try to read more characters for escape sequences
                    import select
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        ch2 = sys.stdin.read(1)
                        if ch2 == '[':
                            ch3 = sys.stdin.read(1)
                            if ch3 == 'A':  # Up arrow
                                return 'up'
                            elif ch3 == 'B':  # Down arrow
                                return 'down'
                            elif ch3 == 'C':  # Right arrow
                                return 'right'
                            elif ch3 == 'D':  # Left arrow
                                return 'left'
                    return 'esc'
                elif ch == '\r' or ch == '\n':  # Enter
                    return 'enter'
                elif ch == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt
                else:
                    return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    @staticmethod
    def display_interactive_menu(title: str, options: List[str], selected_index: int = 0) -> int:
        """
        Display an interactive menu with arrow key navigation.
        
        Args:
            title: Menu title
            options: List of menu options
            selected_index: Initially selected option index
            
        Returns:
            Index of selected option, or -1 if ESC was pressed
        """
        current_selection = selected_index
        first_display = True
        
        while True:
            # Clear previous output (simple approach)
            if not first_display:
                # Move cursor up to redraw menu
                if sys.platform == 'win32':
                    # On Windows, just print newlines
                    print('\n' * 2)
                else:
                    # On Unix, we can use ANSI codes to move cursor
                    print('\n' * 2)
            
            first_display = False
            
            # Display title
            ConsoleUI.print_header(title)
            
            # Display options with highlighting
            for i, option in enumerate(options):
                if i == current_selection:
                    # Highlight selected option
                    print(f"  {Colors.BRIGHT_CYAN}{Colors.BOLD}▶ {option}{Colors.RESET}")
                else:
                    print(f"    {Colors.DIM}{option}{Colors.RESET}")
            
            print(f"\n{Colors.DIM}Use ↑/↓ arrow keys to navigate, Enter to select, Esc to exit{Colors.RESET}")
            sys.stdout.flush()  # Ensure immediate display before waiting for input
            
            # Get user input
            try:
                key = ConsoleUI._get_key()
            except KeyboardInterrupt:
                print(f"\n{Colors.BRIGHT_CYAN}👋 Goodbye!{Colors.RESET}")
                return -1
            
            if key == 'up':
                current_selection = (current_selection - 1) % len(options)
            elif key == 'down':
                current_selection = (current_selection + 1) % len(options)
            elif key == 'enter':
                print()  # Add newline
                return current_selection
            elif key == 'esc':
                # Confirm exit
                print(f"\n{Colors.YELLOW}Are you sure you want to exit? (y/n): {Colors.RESET}", end='', flush=True)
                try:
                    confirm = ConsoleUI._get_key()
                    if confirm and confirm.lower() == 'y':
                        print()  # Add newline
                        return -1
                    # If not 'y', continue the menu loop
                except KeyboardInterrupt:
                    print(f"\n{Colors.BRIGHT_CYAN}👋 Goodbye!{Colors.RESET}")
                    return -1
            # Ignore other keys and continue loop

    @staticmethod
    def display_session_summary(product_name: str, rounds: int, qa_count: int, ideas_count: int, last_updated: str):
        """
        Display a summary of an existing session.
        
        Args:
            product_name: Name of the product
            rounds: Number of rounds completed
            qa_count: Number of Q&A pairs
            ideas_count: Number of content ideas
            last_updated: Last update timestamp
        """
        ConsoleUI.print_section("📂 Existing Session Found")
        print(f"{Colors.BRIGHT_WHITE}{Colors.BOLD}Product/Topic:{Colors.RESET} {Colors.CYAN}{product_name}{Colors.RESET}")
        print(f"{Colors.BRIGHT_WHITE}{Colors.BOLD}Rounds Completed:{Colors.RESET} {rounds}")
        print(f"{Colors.BRIGHT_WHITE}{Colors.BOLD}Q&A Pairs:{Colors.RESET} {qa_count}")
        print(f"{Colors.BRIGHT_WHITE}{Colors.BOLD}Content Ideas:{Colors.RESET} {ideas_count}")
        print(f"{Colors.BRIGHT_WHITE}{Colors.BOLD}Last Updated:{Colors.RESET} {Colors.DIM}{last_updated}{Colors.RESET}")
        print()
        sys.stdout.flush()  # Ensure immediate display

