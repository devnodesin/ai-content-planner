"""AI client for interacting with Ollama API."""

import os
from typing import List, Dict, Any, Optional
from ollama import Client
from utils.config import Config


class AIClient:
    """Client for interacting with Ollama Cloud API."""

    def __init__(self):
        """Initialize the AI client."""
        self.client: Optional[Client] = None
        self.is_available = False
        
        if Config.is_api_configured():
            try:
                self.client = Client(
                    host=Config.OLLAMA_HOST,
                    headers={'Authorization': f'Bearer {Config.OLLAMA_API_KEY}'}
                )
                self.is_available = True
            except Exception as e:
                print(f"Warning: Could not initialize AI client: {e}")
                self.is_available = False

    def generate_questions(self, product_name: str, context: List[Dict[str, str]] = None) -> List[str]:
        """
        Generate questions about a product using AI.
        
        Args:
            product_name: Name of the product
            context: Previous Q&A context for follow-up questions
            
        Returns:
            List of questions (up to MAX_QUESTIONS_PER_ROUND)
        """
        if not self.is_available or not self.client:
            return []

        try:
            if context:
                # Follow-up round: Smart customer exploring toward purchase decision
                context_text = "\n\nWhat I've learned so far:\n"
                for qa in context:
                    context_text += f"Q: {qa.get('question', '')}\nA: {qa.get('answer', '')}\n"
                
                prompt = f"""You are a smart customer evaluating a product called "{product_name}" before making a purchase decision.

{context_text}

Based on what you've learned above, generate exactly {Config.MAX_QUESTIONS_PER_ROUND} questions that help you make an informed purchase decision.

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

Return ONLY the questions, one per line, numbered 1-{Config.MAX_QUESTIONS_PER_ROUND}. No commentary."""
            else:
                # First round: Basic customer questions
                prompt = f"""You are a customer who has just discovered a new product called "{product_name}".

You know NOTHING about this product except its name. Generate exactly {Config.MAX_QUESTIONS_PER_ROUND} questions that a smart customer would ask before considering a purchase.

As a customer, you want to understand:
- What this product is and what it does
- Who it's for and how to use it
- What makes it special or different
- Practical details (price, availability, options)
- Why you should buy it

Use diverse question types (what, who, which, whose, when, why, where, how) such as:
- "What is this product used for?"
- "Who is this product designed for?"
- "How do I use this product?"
- "What makes this product different from others?"
- "Where can I buy this product?"
- "When will it be available?"
- "Why should I choose this product?"
- "What sizes/colors/versions are available?"
- "How much does it cost?"

Do NOT make assumptions about the product. Only ask genuine customer questions.

Return ONLY the questions, one per line, numbered 1-{Config.MAX_QUESTIONS_PER_ROUND}. No commentary."""

            messages = [{'role': 'user', 'content': prompt}]
            
            response = ""
            for part in self.client.chat(Config.OLLAMA_MODEL, messages=messages, stream=True):
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

            return questions[:Config.MAX_QUESTIONS_PER_ROUND]

        except Exception as e:
            print(f"Error generating questions: {e}")
            return []

    def generate_content_ideas(self, product_name: str, qa_pairs: List[Dict[str, str]], existing_ideas: List[str] = None) -> List[str]:
        """
        Generate content/article ideas based on product and Q&A.
        
        Args:
            product_name: Name of the product
            qa_pairs: List of question-answer pairs
            existing_ideas: Previously generated content ideas to avoid duplicates
            
        Returns:
            List of content ideas (titles only)
        """
        if not self.is_available or not self.client:
            return []

        try:
            qa_text = "\n".join([
                f"Q: {qa['question']}\nA: {qa['answer']}"
                for qa in qa_pairs
            ])
            
            existing_text = ""
            if existing_ideas and len(existing_ideas) > 0:
                existing_text = f"\n\nPreviously generated content ideas (DO NOT create similar or duplicate ideas):\n"
                for idea in existing_ideas:
                    existing_text += f"- {idea}\n"

            prompt = f"""You are a content strategist for an e-commerce company selling "{product_name}".

Your goal: Generate exactly {Config.CONTENT_IDEAS_PER_ROUND} HIGH-QUALITY, HIGH-PERFORMING article/blog title ideas that will convert potential customers into buyers.

Customer Q&A Insights:
{qa_text}
{existing_text}

Create content titles that:
1. **Target Different Buyer Journey Stages**:
   - Awareness: Educational content (What, Why, How)
   - Consideration: Comparison and benefits (vs, reasons, features)
   - Decision: Buying guides, reviews, guarantees

2. **Optimize for Multiple Audiences**:
   - New buyers discovering the product
   - Search engines (SEO-friendly keywords)
   - AI assistants (clear, specific information)
   - Human readers (engaging, clickable)

3. **Follow Best Practices**:
   - Answer specific questions from the Q&A
   - Address pain points and objections
   - Highlight unique value propositions
   - Include numbers when relevant (listicles perform well)
   - Use power words (Ultimate, Complete, Essential, Proven)
   - Be specific and actionable

4. **Use Diverse Content Angles**:
   - How-to guides and tutorials
   - Benefits and features
   - Comparisons and alternatives
   - Use cases and applications
   - Buying guides and reviews
   - Problem-solution content
   - Social proof and testimonials

Examples of high-performing title formats:
- "How to [achieve specific benefit] with {product_name}"
- "The Ultimate Guide to Choosing {product_name} for [use case]"
- "{product_name} vs [Alternative]: Complete Comparison for [audience]"
- "[Number] Reasons Why {product_name} is Perfect for [target audience]"
- "What [Expert/Customer Type] Need to Know About {product_name}"
- "Is {product_name} Worth It? Honest Review and Analysis"

CRITICAL REQUIREMENTS:
- Each title must be UNIQUE and cover a DIFFERENT angle
- DO NOT create duplicate or similar content ideas
- DO NOT repeat ideas already listed above
- Ensure each title provides distinct value
- Make titles specific, not generic

Return ONLY the titles, one per line, numbered 1-{Config.CONTENT_IDEAS_PER_ROUND}. No commentary or explanation."""

            messages = [{'role': 'user', 'content': prompt}]
            
            response = ""
            for part in self.client.chat(Config.OLLAMA_MODEL, messages=messages, stream=True):
                response += part['message']['content']

            # Parse ideas from response
            ideas = []
            for line in response.strip().split('\n'):
                line = line.strip()
                if line:
                    # Remove numbering
                    line = line.lstrip('0123456789.)- ')
                    if line and len(line) > 10:
                        ideas.append(line)

            return ideas[:Config.CONTENT_IDEAS_PER_ROUND]

        except Exception as e:
            print(f"Error generating content ideas: {e}")
            return []
