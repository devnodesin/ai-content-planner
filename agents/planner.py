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
                # Generate questions with AI thinking indicator
                self.ui.print_ai_thinking("AI is generating questions")
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
                        continue  # Return to menu after save
                    continue
                
                # Get answers from user
                answers = self.ui.display_questions(questions)
                
                # Filter out skipped questions (empty answers)
                qa_pairs = [(q, a) for q, a in zip(questions, answers) if a.strip()]
                
                if not qa_pairs:
                    self.ui.print_warning("All questions were skipped. Please answer at least one question.")
                    continue
                
                # Store Q&A (only answered questions)
                answered_questions = [q for q, a in qa_pairs]
                answered_answers = [a for q, a in qa_pairs]
                self.session.add_qa_round(answered_questions, answered_answers)
                
                # Generate content ideas with AI thinking indicator
                self.ui.print_ai_thinking("AI is generating content ideas")
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
                    # Return to menu after save, not to questions
                    continue
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
