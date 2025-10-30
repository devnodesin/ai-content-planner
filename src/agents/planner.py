"""Main workflow agent for content planning."""

from typing import List
from ai import AIClient
from ui import ConsoleUI
from .session import SessionManager
from .ai2ai_agent import AI2AIAgent
from utils.config import Config
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


class ContentPlannerAgent:
    """Main agent orchestrating the content planning workflow."""

    def __init__(self):
        """Initialize the content planner agent."""
        self.ai_client = AIClient()
        self.ui = ConsoleUI()
        self.session = SessionManager()
        self.ai2ai_agent = None  # Initialized when needed

    def run(self):
        """Run the main application loop."""
        logger.info("Starting Content Planner application")
        
        # Check API availability
        if not self.ai_client.is_available:
            logger.warning("AI client is not available")
            self.ui.show_api_error()
            # Continue anyway as per requirements
        
        # Check for existing session
        session_summary = self.session.get_session_summary()
        
        if session_summary and session_summary.get('product_name'):
            # Display session summary
            self.ui.display_session_summary(
                product_name=session_summary['product_name'],
                rounds=session_summary['rounds'],
                qa_count=session_summary['qa_count'],
                ideas_count=session_summary['ideas_count'],
                last_updated=session_summary['last_updated']
            )
            
            # Show simplified session resume menu
            choice = self.ui.get_session_resume_choice(session_summary['product_name'])
            
            if choice == 'q':  # Quit
                logger.info("User chose to quit")
                self.ui.print_info("Goodbye!")
                return
            elif choice == 'r':  # Resume existing session
                logger.info("User chose to resume existing session")
                if self.session.load():
                    logger.info(f"Session loaded successfully: {self.session.product_name}")
                    self.ui.print_success(f"Session loaded: {self.session.product_name}")
                    self.ui.print_info(f"Continuing from Round {self.session.round_count}")
                else:
                    logger.error("Failed to load existing session")
                    self.ui.print_error("Failed to load session. Starting new session.")
                    product_name = self.ui.get_product_name()
                    self.session.set_product(product_name)
                    logger.info(f"Started new session for product: {product_name}")
            else:  # choice == 'n' - Start new session
                logger.info("User chose to start new session")
                product_name = self.ui.get_product_name()
                self.session.set_product(product_name)
                logger.info(f"Started new session for product: {product_name}")
        else:
            # No existing session, get product name
            logger.info("No existing session found, starting new session")
            product_name = self.ui.get_product_name()
            self.session.set_product(product_name)
            logger.info(f"Started new session for product: {product_name}")
        
        # Start autosave
        self.session.start_autosave()
        
        try:
            # Main interaction loop - always show menu first
            while True:
                # Show menu and get user choice
                choice = self.ui.get_user_choice()
                logger.info(f"User selected menu option: {choice}")
                
                if choice == 'q':
                    logger.info("User chose to quit")
                    break
                elif choice == 's':
                    logger.info("User chose to save progress")
                    self.session.save()
                    self.ui.print_success("Progress saved!", file_name=Config.OUTPUT_FILE)
                    continue  # Go back to menu
                elif choice == 'a':
                    logger.info("User selected AI2AI Mode")
                    # Initialize AI2AI agent if not already done
                    if not self.ai2ai_agent:
                        self.ai2ai_agent = AI2AIAgent(self.session)
                    
                    # Run AI2AI round
                    success = self.ai2ai_agent.run_round()
                    
                    if not success:
                        self.ui.print_error("AI2AI round failed. Please check configuration.")
                        continue
                    
                    # Generate content ideas after AI2AI round
                    logger.debug("Generating content ideas from AI")
                    self.ui.print_ai_thinking("AI is generating content ideas", model_name=Config.OLLAMA_MODEL)
                    ideas = self._generate_content_ideas()
                    
                    if ideas:
                        logger.info(f"Generated {len(ideas)} content ideas")
                        self.session.add_content_ideas(ideas)
                        self.ui.display_content_ideas(ideas, self.session.round_count)
                    else:
                        logger.warning("Failed to generate content ideas")
                        self.ui.print_warning("Could not generate content ideas.")
                    
                    continue  # Go back to menu
                # 'u' continues to User2AI Mode
                logger.info("User selected User2AI Mode")
                
                # Generate questions with AI thinking indicator
                logger.debug("Generating questions from AI")
                self.ui.print_ai_thinking("AI is generating questions", model_name=Config.OLLAMA_MODEL)
                questions = self._generate_questions()
                
                if not questions:
                    logger.error("Failed to generate questions")
                    self.ui.print_error("Could not generate questions. Please check API configuration.")
                    self.ui.show_help_menu()
                    continue
                
                logger.info(f"Generated {len(questions)} questions")
                
                # Get answers from user
                answers = self.ui.display_questions(questions)
                
                # Filter out skipped questions (empty answers)
                qa_pairs = [(q, a) for q, a in zip(questions, answers) if a.strip()]
                
                if not qa_pairs:
                    logger.warning("All questions were skipped by user")
                    self.ui.print_warning("All questions were skipped. Please answer at least one question.")
                    continue
                
                logger.info(f"User answered {len(qa_pairs)} out of {len(questions)} questions")
                
                # Store Q&A (only answered questions)
                answered_questions = [q for q, a in qa_pairs]
                answered_answers = [a for q, a in qa_pairs]
                self.session.add_qa_round(answered_questions, answered_answers)
                logger.debug(f"Stored Q&A round {self.session.round_count}")
                
                # Generate content ideas with AI thinking indicator
                logger.debug("Generating content ideas from AI")
                self.ui.print_ai_thinking("AI is generating content ideas", model_name=Config.OLLAMA_MODEL)
                ideas = self._generate_content_ideas()
                
                if ideas:
                    logger.info(f"Generated {len(ideas)} content ideas")
                    self.session.add_content_ideas(ideas)
                    self.ui.display_content_ideas(ideas, self.session.round_count)
                else:
                    logger.warning("Failed to generate content ideas")
                    self.ui.print_warning("Could not generate content ideas.")
        
        finally:
            # Stop autosave and save final state
            logger.info("Stopping autosave and saving final state")
            self.session.stop_autosave()
            if self.session.save():
                logger.info(f"Session saved successfully to {Config.OUTPUT_FILE}")
                self.ui.print_success(f"Session saved to {Config.OUTPUT_FILE}")
            else:
                logger.error("Failed to save session")
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
