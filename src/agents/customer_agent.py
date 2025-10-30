"""Customer agent for generating questions about a product."""

from typing import List, Dict, Optional
from ollama import Client
from utils.config import Config


class CustomerAgent:
    """AI agent that acts as a customer evaluating a product."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the customer agent.
        
        Args:
            api_key: Ollama API key (defaults to Config.OLLAMA_API_KEY)
            model: Model name (defaults to Config.OLLAMA_MODEL)
        """
        # Use explicit api_key if provided, otherwise fall back to config
        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = Config.OLLAMA_API_KEY
        
        self.model = model or Config.OLLAMA_MODEL
        self.client: Optional[Client] = None
        self.is_available = False
        
        if self.api_key and self.api_key != 'your_api_key_here':
            try:
                self.client = Client(
                    host=Config.OLLAMA_HOST,
                    headers={'Authorization': f'Bearer {self.api_key}'}
                )
                self.is_available = True
            except Exception as e:
                print(f"Warning: Could not initialize customer agent: {e}")
                self.is_available = False

    def generate_questions(
        self,
        product_name: str,
        context: Optional[List[Dict[str, str]]] = None,
        max_questions: Optional[int] = None
    ) -> List[str]:
        """
        Generate questions about a product as a customer.
        
        Args:
            product_name: Name of the product
            context: Previous Q&A context for follow-up questions
            max_questions: Maximum number of questions to generate
            
        Returns:
            List of questions
        """
        if not self.is_available or not self.client:
            return []

        max_questions = max_questions or Config.MAX_QUESTIONS_PER_ROUND

        try:
            if context:
                # Follow-up round: Smart customer exploring toward purchase decision
                context_text = "\n\nWhat I've learned so far:\n"
                for qa in context:
                    context_text += f"Q: {qa.get('question', '')}\nA: {qa.get('answer', '')}\n"
                
                prompt = f"""You are a smart customer evaluating a product called "{product_name}" before making a purchase decision.

{context_text}

Based on what you've learned above, generate exactly {max_questions} questions that help you make an informed purchase decision.

Your goal as a customer is to:
1. **Ask follow-up questions ONLY if there's a valid doubt or unclear information** from previous answers
2. **Explore NEW unexplored areas** of the product that haven't been covered yet
3. **Move toward making a purchase decision** by understanding:
   - Value proposition and benefits
   - Practical usage and compatibility
   - Pricing, warranty, and guarantees
   - Social proof and reviews
   - Comparison with alternatives
   - Post-purchase support
   - Risk mitigation (returns, trials, etc.)

Strategy:
- If something in previous answers needs clarification → ask a follow-up question
- If an important area hasn't been explored → ask about that new area
- Focus on questions that help you decide whether to buy
- Think like a buyer evaluating: features, benefits, value, trust, risk
- Use diverse question types: what, who, which, whose, when, why, where, how

DO NOT:
- Re-ask questions that have been clearly answered
- Make assumptions about the product
- Ask vague or redundant questions

Return ONLY the questions, one per line, numbered 1-{max_questions}. No commentary."""
            else:
                # First round: Basic customer questions
                prompt = f"""You are a customer who has just discovered a new product called "{product_name}".

You know NOTHING about this product except its name. Generate exactly {max_questions} questions that a smart customer would ask before considering a purchase.

As a customer, you want to understand:
- What this product is and what it does
- Who it's for and how to use it
- What makes it special or different
- Practical details (availability, options)
- Why you should buy it

Use diverse question types (what, who, which, whose, when, why, where, how) such as:
- "What is this product used for?"
- "Who is this product designed for?"
- "How to use this product?"
- "Where can I buy this product?"
- "What sizes/colors/versions are available?"

Do NOT make assumptions about the product. Only ask genuine customer questions.

Return ONLY the questions, one per line, numbered 1-{max_questions}. No commentary."""

            messages = [{'role': 'user', 'content': prompt}]
            
            response = ""
            for part in self.client.chat(self.model, messages=messages, stream=True):
                response += part['message']['content']

            # Parse questions from response
            questions = []
            for line in response.strip().split('\n'):
                line = line.strip()
                if line:
                    # Remove numbering like "1.", "1)", etc.
                    line = line.lstrip('0123456789.)- ')
                    if line and len(line) > 10:  # Avoid empty or too short lines
                        questions.append(line)

            return questions[:max_questions]

        except Exception as e:
            print(f"Error generating questions: {e}")
            return []
