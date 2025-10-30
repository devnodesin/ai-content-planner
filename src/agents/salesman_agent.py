"""Salesman agent for answering customer questions about a product."""

from typing import Optional
from pathlib import Path
from ollama import Client
from utils.config import Config


class SalesmanAgent:
    """AI agent that acts as a salesman with product knowledge."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, context_file: Optional[str] = None):
        """
        Initialize the salesman agent.
        
        Args:
            api_key: Ollama API key (defaults to Config.OLLAMA_API_KEY_SALESMAN)
            model: Model name (defaults to Config.OLLAMA_MODEL_SALESMAN)
            context_file: Path to context file with product knowledge (defaults to Config.CONTEXT_FILE)
        """
        # Use explicit api_key if provided, otherwise fall back to config
        if api_key is not None:
            self.api_key = api_key
        else:
            self.api_key = Config.OLLAMA_API_KEY_SALESMAN
        
        self.model = model or Config.OLLAMA_MODEL_SALESMAN
        self.context_file = Path(context_file or Config.CONTEXT_FILE)
        self.client: Optional[Client] = None
        self.is_available = False
        self.product_context = ""
        
        # Load product context
        self._load_context()
        
        # Initialize Ollama client
        if self.api_key and self.api_key != 'your_api_key_here':
            try:
                self.client = Client(
                    host=Config.OLLAMA_HOST,
                    headers={'Authorization': f'Bearer {self.api_key}'}
                )
                self.is_available = True
            except Exception as e:
                print(f"Warning: Could not initialize salesman agent: {e}")
                self.is_available = False

    def _load_context(self):
        """Load product context from the context file."""
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    self.product_context = f.read()
            except Exception as e:
                print(f"Warning: Could not load context file: {e}")
                self.product_context = ""
        else:
            print(f"Warning: Context file not found at {self.context_file}")
            self.product_context = ""

    def answer_question(self, question: str, product_name: str) -> str:
        """
        Answer a customer's question about the product.
        
        Args:
            question: The customer's question
            product_name: Name of the product
            
        Returns:
            Answer to the question
        """
        if not self.is_available or not self.client:
            return "I apologize, but I'm currently unable to answer questions. Please try again later."

        try:
            prompt = f"""You are an expert salesman for a product called "{product_name}".

Product Knowledge:
{self.product_context if self.product_context else "No specific product information available."}

Customer Question: {question}

Your task:
1. Respond to customer questions in a friendly, polite, and helpful manner.
2. Use only the provided product information.
3. If information is unavailable, acknowledge this and refer the customer to support.
4. Keep responses clear and concise (maximum 100 characters or 2 sentences).
5. Highlight key benefits and features to help customers make informed purchase decisions.

DO NOT:
- Make up information not in the product knowledge
- Give overly long answers
- Be pushy or aggressive
- Ignore the customer's specific question

Provide a helpful, professional answer:"""

            messages = [{'role': 'user', 'content': prompt}]
            
            response = ""
            for part in self.client.chat(self.model, messages=messages, stream=True):
                response += part['message']['content']

            return response.strip()

        except Exception as e:
            print(f"Error answering question: {e}")
            return "I apologize, but I encountered an error while processing your question. Please try again."
