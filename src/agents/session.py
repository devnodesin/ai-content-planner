"""Session manager for storing and persisting application state."""

import json
import threading
import time
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
from utils.config import Config


class SessionManager:
    """Manages session state and persistence."""

    def __init__(self):
        """Initialize session manager."""
        self.product_name: str = ""
        self.qa_history: List[Dict[str, str]] = []
        self.content_ideas: List[str] = []
        self.round_count: int = 0
        self.output_file = Path(Config.OUTPUT_FILE)
        self.autosave_thread: threading.Thread = None
        self.autosave_enabled: bool = False
        self.last_save_time: float = time.time()
        
        # Ensure output directory exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

    def set_product(self, product_name: str):
        """Set the product name."""
        self.product_name = product_name

    def add_qa_round(self, questions: List[str], answers: List[str]):
        """
        Add a round of Q&A to history.
        
        Args:
            questions: List of questions
            answers: List of answers
        """
        self.round_count += 1
        for q, a in zip(questions, answers):
            self.qa_history.append({
                'round': self.round_count,
                'question': q,
                'answer': a,
                'timestamp': datetime.now().isoformat()
            })

    def add_content_ideas(self, ideas: List[Dict[str, str]]):
        """
        Add content ideas to the collection with intelligent deduplication.
        
        Args:
            ideas: List of content idea dictionaries with 'title' and 'summary'
        """
        for idea in ideas:
            # Handle both old format (string) and new format (dict)
            if isinstance(idea, str):
                idea_dict = {'title': idea, 'summary': ''}
            else:
                idea_dict = idea
            
            title = idea_dict.get('title', '').strip()
            if not title:
                continue
            
            # Check for exact duplicates
            if any(existing.get('title', '') == title for existing in self.content_ideas):
                continue
            
            # Check for similar duplicates (case-insensitive and normalized)
            title_normalized = title.lower().strip()
            is_duplicate = False
            
            for existing_idea in self.content_ideas:
                existing_title = existing_idea.get('title', '')
                existing_normalized = existing_title.lower().strip()
                
                # Check if titles are too similar (simple similarity check)
                if title_normalized == existing_normalized:
                    is_duplicate = True
                    break
                
                # Check if one is a substring of the other (avoiding very similar titles)
                if len(title_normalized) > 20 and len(existing_normalized) > 20:
                    # Calculate simple similarity
                    words_new = set(title_normalized.split())
                    words_existing = set(existing_normalized.split())
                    
                    if len(words_new) > 3 and len(words_existing) > 3:
                        common_words = words_new.intersection(words_existing)
                        similarity = len(common_words) / min(len(words_new), len(words_existing))
                        
                        # If more than 70% similar, consider it a duplicate
                        if similarity > 0.7:
                            is_duplicate = True
                            break
            
            if not is_duplicate:
                self.content_ideas.append({
                    'title': title,
                    'summary': idea_dict.get('summary', '').strip()
                })
    
    def get_content_ideas(self) -> List[Dict[str, str]]:
        """Get all unique content ideas."""
        return self.content_ideas

    def get_qa_context(self) -> List[Dict[str, str]]:
        """Get Q&A history for context."""
        return self.qa_history

    def save(self) -> bool:
        """
        Save session data to JSON file.
        
        Returns:
            True if save was successful
        """
        try:
            data = {
                'product_name': self.product_name,
                'rounds': self.round_count,
                'qa_history': self.qa_history,
                'content_ideas': self.content_ideas,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.last_save_time = time.time()
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False

    def load(self) -> bool:
        """
        Load session data from JSON file if it exists.
        
        Returns:
            True if load was successful
        """
        if not self.output_file.exists():
            return False

        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.product_name = data.get('product_name', '')
            self.qa_history = data.get('qa_history', [])
            self.content_ideas = data.get('content_ideas', [])
            self.round_count = data.get('rounds', 0)
            
            return True
        except Exception as e:
            print(f"Error loading session: {e}")
            return False

    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get session summary from the output file without loading it.
        
        Returns:
            Dictionary with session summary or None if file doesn't exist
        """
        if not self.output_file.exists():
            return None

        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                'product_name': data.get('product_name', ''),
                'rounds': data.get('rounds', 0),
                'qa_count': len(data.get('qa_history', [])),
                'ideas_count': len(data.get('content_ideas', [])),
                'last_updated': data.get('last_updated', 'Unknown')
            }
        except Exception as e:
            print(f"Error reading session summary: {e}")
            return None

    def _autosave_worker(self):
        """Background worker for autosave."""
        while self.autosave_enabled:
            time.sleep(Config.AUTOSAVE_INTERVAL_SECONDS)
            if self.autosave_enabled:
                self.save()

    def start_autosave(self):
        """Start autosave background thread."""
        if not self.autosave_enabled:
            self.autosave_enabled = True
            self.autosave_thread = threading.Thread(target=self._autosave_worker, daemon=True)
            self.autosave_thread.start()

    def stop_autosave(self):
        """Stop autosave background thread."""
        self.autosave_enabled = False
        if self.autosave_thread:
            self.autosave_thread.join(timeout=1)
