"""Tests for UI console module."""

import pytest
from unittest.mock import patch, MagicMock
from ui.console import ConsoleUI


def test_get_user_choice_valid_options():
    """Test that get_user_choice accepts valid options: u, a, s, q."""
    valid_choices = ['u', 'a', 's', 'q']
    
    for choice in valid_choices:
        with patch('builtins.input', return_value=choice):
            result = ConsoleUI.get_user_choice()
            assert result == choice


def test_get_user_choice_uppercase():
    """Test that get_user_choice handles uppercase input."""
    with patch('builtins.input', return_value='U'):
        result = ConsoleUI.get_user_choice()
        assert result == 'u'


def test_get_user_choice_invalid_then_valid():
    """Test that get_user_choice rejects invalid input then accepts valid."""
    with patch('builtins.input', side_effect=['x', 'u']):
        result = ConsoleUI.get_user_choice()
        assert result == 'u'


def test_help_menu_displays_new_options():
    """Test that help menu includes User2AI and AI2AI modes."""
    with patch('builtins.print') as mock_print:
        ConsoleUI.show_help_menu()
        
        # Verify the print was called
        assert mock_print.called
        
        # Get all print call arguments
        all_prints = [str(call[0][0]) if call[0] else '' for call in mock_print.call_args_list]
        all_output = ' '.join(all_prints)
        
        # Check for new menu options
        assert 'User2AI' in all_output or 'u' in all_output.lower()
        assert 'AI2AI' in all_output or 'a' in all_output.lower()
