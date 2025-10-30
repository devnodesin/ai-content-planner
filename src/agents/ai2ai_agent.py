"""AI2AI workflow agent where customer and salesman agents interact."""

from typing import List
from agents.customer_agent import CustomerAgent
from agents.salesman_agent import SalesmanAgent
from .session import SessionManager
from ui import ConsoleUI
from utils.config import Config
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


class AI2AIAgent:
    """Agent orchestrating AI2AI mode where customer and salesman agents interact."""

    def __init__(self, session: SessionManager):
        """
        Initialize the AI2AI agent.
        
        Args:
            session: Session manager for storing Q&A
        """
        self.customer_agent = CustomerAgent()
        self.salesman_agent = SalesmanAgent()
        self.session = session
        self.ui = ConsoleUI()

    def run_round(self) -> bool:
        """
        Run one round of AI2AI interaction.
        
        Returns:
            True if round was successful, False otherwise
        """
        logger.info("Starting AI2AI round")
        
        # Check if agents are available
        if not self.customer_agent.is_available:
            logger.error("Customer agent is not available")
            self.ui.print_error("Customer agent is not configured. Please check OLLAMA_API_KEY.")
            return False
        
        if not self.salesman_agent.is_available:
            logger.error("Salesman agent is not available")
            self.ui.print_error("Salesman agent is not configured. Please check OLLAMA_API_KEY_SALESMAN.")
            return False
        
        if not self.salesman_agent.product_context:
            logger.error("No product context available for salesman")
            self.ui.print_error(f"No product context found at {Config.CONTEXT_FILE}. Please create the file first.")
            return False
        
        # Generate questions with customer agent
        logger.debug("Customer agent generating questions")
        self.ui.print_ai_thinking(
            "Customer AI is generating questions",
            model_name=self.customer_agent.model
        )
        
        questions = self.customer_agent.generate_questions(
            self.session.product_name,
            self.session.get_qa_context()
        )
        
        if not questions:
            logger.error("Customer agent failed to generate questions")
            self.ui.print_error("Customer agent could not generate questions.")
            return False
        
        logger.info(f"Customer agent generated {len(questions)} questions")
        
        # Have salesman agent answer each question
        self.ui.print_section(f"AI2AI Round {self.session.round_count + 1}")
        
        answered_questions = []
        answered_answers = []
        
        for i, question in enumerate(questions, 1):
            self.ui.print_question(i, len(questions), question)
            
            # Get answer from salesman agent
            logger.debug(f"Salesman agent answering question {i}")
            self.ui.print_ai_thinking(
                "Salesman AI is thinking",
                model_name=self.salesman_agent.model
            )
            
            answer = self.salesman_agent.answer_question(question, self.session.product_name)
            
            # Display answer
            self.ui.print_info(f"Salesman: {answer}\n")
            
            answered_questions.append(question)
            answered_answers.append(answer)
        
        # Store Q&A
        self.session.add_qa_round(answered_questions, answered_answers)
        logger.info(f"Stored {len(answered_questions)} Q&A pairs")
        
        return True
