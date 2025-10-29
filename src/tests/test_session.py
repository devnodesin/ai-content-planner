"""Tests for session manager."""

import json
import tempfile
from pathlib import Path
from agents.session import SessionManager


def test_session_initialization():
    """Test session manager initialization."""
    session = SessionManager()
    assert session.product_name == ""
    assert session.qa_history == []
    assert session.content_ideas == []
    assert session.round_count == 0


def test_set_product():
    """Test setting product name."""
    session = SessionManager()
    session.set_product("Test Product")
    assert session.product_name == "Test Product"


def test_add_qa_round():
    """Test adding Q&A round."""
    session = SessionManager()
    questions = ["What is it?", "Who uses it?"]
    answers = ["A product", "Everyone"]
    
    session.add_qa_round(questions, answers)
    
    assert session.round_count == 1
    assert len(session.qa_history) == 2
    assert session.qa_history[0]['question'] == "What is it?"
    assert session.qa_history[0]['answer'] == "A product"


def test_add_content_ideas():
    """Test adding content ideas with deduplication."""
    session = SessionManager()
    ideas = [
        {"title": "Idea 1", "summary": "Summary 1"},
        {"title": "Idea 2", "summary": "Summary 2"},
        {"title": "Idea 1", "summary": "Summary 1"}  # Exact duplicate
    ]
    
    session.add_content_ideas(ideas)
    
    # Should not add exact duplicates
    assert len(session.content_ideas) == 2
    assert session.content_ideas[0]['title'] == "Idea 1"


def test_add_similar_content_ideas():
    """Test that similar content ideas are deduplicated."""
    session = SessionManager()
    
    # Add first batch
    session.add_content_ideas([{"title": "How to Use Wireless Headphones for Running", "summary": "Guide for runners"}])
    
    # Try to add similar idea (should be filtered out)
    session.add_content_ideas([{"title": "How to use wireless headphones for running", "summary": "Another guide"}])  # Case difference
    
    # Should only have 1 (case-insensitive duplicate)
    assert len(session.content_ideas) == 1
    
    # Add a different idea
    session.add_content_ideas([{"title": "Best Wireless Headphones for Gaming", "summary": "Gaming headphones"}])
    
    # Should have 2 now
    assert len(session.content_ideas) == 2


def test_get_content_ideas():
    """Test getting content ideas."""
    session = SessionManager()
    ideas = [
        {"title": "Idea 1", "summary": "Summary 1"},
        {"title": "Idea 2", "summary": "Summary 2"}
    ]
    session.add_content_ideas(ideas)
    
    retrieved = session.get_content_ideas()
    assert len(retrieved) == 2
    assert retrieved[0]['title'] == "Idea 1"
    assert retrieved[0]['summary'] == "Summary 1"


def test_save_and_load():
    """Test saving and loading session."""
    with tempfile.TemporaryDirectory() as tmpdir:
        session = SessionManager()
        session.output_file = Path(tmpdir) / 'test_out_content_ideas.json'
        
        session.set_product("Test Product")
        session.add_qa_round(["Q1"], ["A1"])
        session.add_content_ideas([{"title": "Idea 1", "summary": "Summary 1"}])
        
        # Save
        assert session.save() is True
        assert session.output_file.exists()
        
        # Load in new session
        new_session = SessionManager()
        new_session.output_file = session.output_file
        assert new_session.load() is True
        
        assert new_session.product_name == "Test Product"
        assert len(new_session.qa_history) == 1
        assert len(new_session.content_ideas) == 1
        assert new_session.content_ideas[0]['title'] == "Idea 1"
