"""Main workflow agent for content planning."""

from typing import List
from ai import AIClient
from ui import ConsoleUI
from .session import SessionManager
from utils.config import Config


class ContentPlannerAgent:
    """Main agent orchestrating the content planning workflow."""

    def __init__(self):
        """Initialize the content planner agent."""
        self.ai_client = AIClient()
        self.ui = ConsoleUI()
        self.session = SessionManager()

    def run(self):
        """Run the main application loop."""
        # Check API availability
        if not self.ai_client.is_available:
            self.ui.show_api_error()
            # Continue anyway as per requirements
        
        # Get product name
        product_name = self.ui.get_product_name()
        self.session.set_product(product_name)
        
        # Start autosave
        self.session.start_autosave()
        
        try:
            # Main interaction loop
            while True:
                # Generate questions
                questions = self._generate_questions()
                
                if not questions:
                    self.ui.print_error("Could not generate questions. Please check API configuration.")
                    self.ui.show_help_menu()
                    choice = self.ui.get_user_choice()
                    if choice == 'q':
                        break
                    elif choice == 's':
                        self.session.save()
                        self.ui.print_success("Progress saved!")
                    continue
                
                # Get answers from user
                answers = self.ui.display_questions(questions)
                
                # Store Q&A
                self.session.add_qa_round(questions, answers)
                
                # Generate content ideas
                ideas = self._generate_content_ideas()
                
                if ideas:
                    self.session.add_content_ideas(ideas)
                    self.ui.display_content_ideas(ideas, self.session.round_count)
                else:
                    self.ui.print_warning("Could not generate content ideas.")
                
                # Get user choice
                choice = self.ui.get_user_choice()
                
                if choice == 'q':
                    break
                elif choice == 's':
                    self.session.save()
                    self.ui.print_success("Progress saved!")
                # 'c' continues the loop
        
        finally:
            # Stop autosave and save final state
            self.session.stop_autosave()
            if self.session.save():
                self.ui.print_success(f"Session saved to {Config.OUTPUT_FILE}")
            else:
                self.ui.print_error("Failed to save session")

    def _generate_questions(self) -> List[str]:
        """Generate questions using AI."""
        context = self.session.get_qa_context()
        return self.ai_client.generate_questions(
            self.session.product_name,
            context if context else None
        )

    def _generate_content_ideas(self) -> List[str]:
        """Generate content ideas using AI."""
        return self.ai_client.generate_content_ideas(
            self.session.product_name,
            self.session.get_qa_context(),
            self.session.get_content_ideas()
        )
