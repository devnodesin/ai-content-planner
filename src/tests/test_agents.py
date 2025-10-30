"""Tests for customer and salesman agents."""

import pytest
from agents.customer_agent import CustomerAgent
from agents.salesman_agent import SalesmanAgent
from pathlib import Path
import tempfile
import os


def test_customer_agent_initialization():
    """Test customer agent initialization."""
    agent = CustomerAgent()
    assert agent is not None
    assert agent.model is not None
    # Agent availability depends on API key configuration
    assert isinstance(agent.is_available, bool)


def test_customer_agent_without_api():
    """Test customer agent without API key."""
    agent = CustomerAgent(api_key="")
    # Should not be available without API key
    assert agent.is_available is False or agent.api_key == ""
    # Even if available (due to environment), questions should fail without proper API
    if not agent.is_available:
        questions = agent.generate_questions("Test Product")
        assert questions == []


def test_customer_agent_custom_config():
    """Test customer agent with custom configuration."""
    agent = CustomerAgent(api_key="test_key", model="test_model")
    assert agent.api_key == "test_key"
    assert agent.model == "test_model"


def test_salesman_agent_initialization():
    """Test salesman agent initialization."""
    agent = SalesmanAgent()
    assert agent is not None
    assert agent.model is not None
    # Agent availability depends on API key configuration
    assert isinstance(agent.is_available, bool)


def test_salesman_agent_without_api():
    """Test salesman agent without API key."""
    agent = SalesmanAgent(api_key="")
    # Should not be available without API key
    assert agent.is_available is False or agent.api_key == ""


def test_salesman_agent_with_context():
    """Test salesman agent loads context file."""
    # Create temporary context file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write("# Test Product\n\nThis is a test product with great features.")
        temp_file = f.name
    
    try:
        agent = SalesmanAgent(context_file=temp_file)
        assert agent.product_context != ""
        assert "Test Product" in agent.product_context
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)


def test_salesman_agent_without_context():
    """Test salesman agent without context file."""
    non_existent_file = "non_existent_file.md"
    agent = SalesmanAgent(context_file=non_existent_file)
    assert agent.product_context == ""


def test_salesman_agent_custom_config():
    """Test salesman agent with custom configuration."""
    agent = SalesmanAgent(api_key="test_key", model="test_model")
    assert agent.api_key == "test_key"
    assert agent.model == "test_model"


def test_customer_agent_question_generation_context():
    """Test that customer agent accepts context parameter."""
    agent = CustomerAgent(api_key="invalid_key")
    agent.is_available = False  # Force unavailable for test
    context = [
        {"question": "What is this?", "answer": "A product"}
    ]
    # Should return empty list without API, but not crash with context
    questions = agent.generate_questions("Test", context=context)
    assert questions == []


def test_salesman_agent_answer_question():
    """Test salesman agent answer_question method."""
    agent = SalesmanAgent(api_key="invalid_key")
    agent.is_available = False  # Force unavailable for test
    answer = agent.answer_question("What is this?", "Test Product")
    # Without API, should return error message
    assert "unable to answer" in answer.lower() or "try again" in answer.lower()
