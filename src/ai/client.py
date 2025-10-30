"""AI client for interacting with Ollama API."""

import os
from typing import List, Dict, Any, Optional
from ollama import Client
from utils.config import Config

# Import customer agent directly to avoid circular imports
# from agents.customer_agent import CustomerAgent


class AIClient:
    """Client for interacting with Ollama Cloud API."""

    def __init__(self):
        """Initialize the AI client."""
        # Lazy import to avoid circular dependency
        from agents.customer_agent import CustomerAgent
        
        self.customer_agent = CustomerAgent()
        self.client: Optional[Client] = None
        self.is_available = self.customer_agent.is_available
        
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
        return self.customer_agent.generate_questions(product_name, context)

    def generate_content_ideas(self, product_name: str, qa_pairs: List[Dict[str, str]], existing_ideas: List[Dict[str, str]] = None) -> List[Dict[str, str]]:
        """
        Generate content/article ideas based on product and Q&A.
        
        Args:
            product_name: Name of the product
            qa_pairs: List of question-answer pairs
            existing_ideas: Previously generated content ideas to avoid duplicates
            
        Returns:
            List of content ideas with title and summary
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
                    existing_text += f"- {idea.get('title', idea)}\n"

            prompt = f"""You are a content strategist for an e-commerce company selling "{product_name}".

Your goal: Generate exactly {Config.CONTENT_IDEAS_PER_ROUND} HIGH-QUALITY, HIGH-PERFORMING article/blog ideas that will convert potential customers into buyers.

Customer Q&A Insights:
{qa_text}
{existing_text}

Create content ideas that:
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

OUTPUT FORMAT (IMPORTANT):
Return content ideas in this exact JSON format, one per line:
{{"title": "Article Title Here", "summary": "Brief 100-150 char description of what this article should contain"}}

Generate exactly {Config.CONTENT_IDEAS_PER_ROUND} ideas, numbered 1-{Config.CONTENT_IDEAS_PER_ROUND}.
Each summary should be 100-150 characters and describe the article's key points."""

            messages = [{'role': 'user', 'content': prompt}]
            
            response = ""
            for part in self.client.chat(Config.OLLAMA_MODEL, messages=messages, stream=True):
                response += part['message']['content']

            # Parse ideas from response (expecting JSON format)
            import json
            import re
            
            ideas = []
            # Try to extract JSON objects from the response
            json_pattern = r'\{[^}]+\}'
            matches = re.findall(json_pattern, response, re.DOTALL)
            
            for match in matches:
                try:
                    idea_obj = json.loads(match)
                    if 'title' in idea_obj:
                        # Ensure summary exists and is within character limit
                        summary = idea_obj.get('summary', '')
                        if len(summary) > 150:
                            summary = summary[:147] + '...'
                        elif len(summary) < 100 and summary:
                            # If too short, it's acceptable but flag it
                            pass
                        
                        ideas.append({
                            'title': idea_obj['title'].strip(),
                            'summary': summary.strip()
                        })
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract title from plain text
                    line = match.strip()
                    if len(line) > 10:
                        # Fallback: create simple structure
                        ideas.append({
                            'title': line.lstrip('0123456789.)- '),
                            'summary': 'Content article about this topic.'
                        })

            return ideas[:Config.CONTENT_IDEAS_PER_ROUND]

        except Exception as e:
            print(f"Error generating content ideas: {e}")
            return []
