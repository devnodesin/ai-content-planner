#!/usr/bin/env python3
"""
Content Planner - Interactive AI-powered content idea generation tool.

This application helps content creators generate ideas for e-commerce products
through AI-guided Q&A sessions and automated content ideation.
"""

from agents import ContentPlannerAgent


def main():
    """Main entry point for the application."""
    try:
        agent = ContentPlannerAgent()
        agent.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
