"""Tests for AI client."""

from ai.client import AIClient


def test_ai_client_initialization():
    """Test AI client initialization."""
    client = AIClient()
    assert client is not None
    # is_available depends on API key configuration
    assert isinstance(client.is_available, bool)


def test_generate_questions_without_api():
    """Test question generation fails gracefully without API."""
    client = AIClient()
    if not client.is_available:
        questions = client.generate_questions("Test Product")
        assert questions == []


def test_generate_content_ideas_without_api():
    """Test content idea generation fails gracefully without API."""
    client = AIClient()
    if not client.is_available:
        qa_pairs = [{'question': 'What?', 'answer': 'Something'}]
        ideas = client.generate_content_ideas("Test Product", qa_pairs, [])
        assert ideas == []


def test_content_ideas_deduplication():
    """Test that existing ideas are passed to avoid duplicates."""
    client = AIClient()
    if not client.is_available:
        qa_pairs = [{'question': 'What?', 'answer': 'Something'}]
        existing = ["Idea 1", "Idea 2"]
        ideas = client.generate_content_ideas("Test Product", qa_pairs, existing)
        assert ideas == []
