#!/usr/bin/env python3
"""
Context File Generator

This script generates a standardized markdown context file from various input sources:
- Markdown (.md) files
- JSON (.json) files
- Web URLs (with HTML to markdown conversion)

The generated context file is suitable for AI agents and follows a standardized format.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Union
from urllib.parse import urlparse
import argparse


def remove_unwanted_html_sections(html_content: str) -> str:
    """
    Remove unwanted HTML sections like header, footer, nav, aside, sidebar.
    
    This is a preprocessing step before converting HTML to markdown.
    
    Args:
        html_content: Raw HTML content
        
    Returns:
        HTML content with unwanted sections removed
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        # If BeautifulSoup is not available, return content as-is
        # The convert_html_to_markdown will still work
        return html_content
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted tags
        unwanted_tags = ['header', 'footer', 'nav', 'aside', 'script', 'style', 'iframe']
        for tag in unwanted_tags:
            for element in soup.find_all(tag):
                element.decompose()
        
        # Remove elements by class or id that are typically unwanted
        unwanted_patterns = ['sidebar', 'navigation', 'menu', 'advertisement', 'ad-']
        for pattern in unwanted_patterns:
            for element in soup.find_all(class_=lambda c: c and pattern in c.lower()):
                element.decompose()
            for element in soup.find_all(id=lambda i: i and pattern in i.lower()):
                element.decompose()
        
        return str(soup)
    except Exception:
        # If parsing fails, return original content
        return html_content


def convert_html_to_markdown(html_content: str) -> str:
    """
    Convert HTML content to clean markdown format.
    
    Args:
        html_content: Raw HTML content
        
    Returns:
        Clean markdown text
        
    Raises:
        ImportError: If html2text library is not available
    """
    try:
        import html2text
        from html.parser import HTMLParser
    except ImportError:
        raise ImportError(
            "The 'html2text' library is required to convert HTML to markdown.\n"
            "Please install it using: uv add html2text"
        )
    
    # Configure html2text for clean output
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0  # Don't wrap lines
    h.skip_internal_links = True
    h.ignore_anchors = True
    h.single_line_break = False
    
    # Convert HTML to markdown
    markdown = h.handle(html_content)
    
    # Clean up excessive newlines
    lines = markdown.split('\n')
    cleaned_lines = []
    prev_empty = False
    
    for line in lines:
        stripped = line.strip()
        is_empty = len(stripped) == 0
        
        # Skip multiple consecutive empty lines
        if is_empty and prev_empty:
            continue
        
        # Skip common junk patterns
        if stripped.lower() in ['advertisement', 'loading...', 'skip to content', 'skip to main content']:
            continue
            
        cleaned_lines.append(line)
        prev_empty = is_empty
    
    # Join back and trim
    clean_markdown = '\n'.join(cleaned_lines).strip()
    
    return clean_markdown


def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url: The URL string to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def read_markdown_file(file_path: Path) -> Dict[str, Any]:
    """
    Read and parse a markdown file.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        Dictionary containing parsed content
        
    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file can't be read
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {file_path}")
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Parse markdown content
        lines = content.split('\n')
        parsed_data = {
            "source_type": "markdown",
            "source_path": str(file_path),
            "content": content,
            "metadata": {
                "line_count": len(lines),
                "character_count": len(content)
            }
        }
        
        # Extract title if present (first H1 heading)
        for line in lines:
            if line.startswith('# '):
                parsed_data["title"] = line[2:].strip()
                break
        
        return parsed_data
    except Exception as e:
        raise IOError(f"Error reading markdown file: {e}")


def read_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Read and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing parsed content
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If JSON is invalid
        IOError: If file can't be read
    """
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    
    try:
        content = file_path.read_text(encoding='utf-8')
        data = json.loads(content)
        
        return {
            "source_type": "json",
            "source_path": str(file_path),
            "data": data,
            "metadata": {
                "character_count": len(content)
            }
        }
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON format: {e.msg}", e.doc, e.pos)
    except Exception as e:
        raise IOError(f"Error reading JSON file: {e}")


def fetch_url_content(url: str) -> Dict[str, Any]:
    """
    Fetch and parse content from a web URL.
    
    Args:
        url: The URL to fetch content from
        
    Returns:
        Dictionary containing fetched content
        
    Raises:
        ImportError: If requests library is not available
        Exception: If URL can't be reached or content can't be fetched
    """
    try:
        import requests
    except ImportError:
        raise ImportError(
            "The 'requests' library is required to fetch content from URLs.\n"
            "Please install it using: uv add requests"
        )
    
    if not validate_url(url):
        raise ValueError(f"Invalid URL format: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        content = response.text
        content_type = response.headers.get('content-type', '').lower()
        
        # Convert HTML to markdown if needed
        is_html = 'html' in content_type or content.strip().lower().startswith('<!doctype html') or content.strip().lower().startswith('<html')
        
        if is_html:
            try:
                markdown_content = convert_html_to_markdown(content)
                content = markdown_content
                content_type = 'text/markdown (converted from HTML)'
            except Exception as e:
                print(f"⚠️  Warning: Could not convert HTML to markdown: {e}")
                print("Using raw HTML content instead.")
        
        return {
            "source_type": "url",
            "source_url": url,
            "content": content,
            "metadata": {
                "content_type": content_type,
                "character_count": len(content),
                "status_code": response.status_code
            }
        }
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching URL content: {e}")


def convert_to_markdown_context(data: Dict[str, Any]) -> str:
    """
    Convert parsed data into a standardized markdown context format.
    
    Args:
        data: Dictionary containing parsed data from any source
        
    Returns:
        Formatted markdown string
    """
    source_type = data.get("source_type", "unknown")
    
    markdown_parts = []
    
    # Header
    markdown_parts.append("# Context Input\n")
    markdown_parts.append(f"**Source Type:** {source_type}\n")
    
    if source_type == "markdown":
        markdown_parts.append(f"**Source File:** {data.get('source_path', 'N/A')}\n")
        if "title" in data:
            markdown_parts.append(f"**Original Title:** {data['title']}\n")
        markdown_parts.append("\n---\n\n")
        markdown_parts.append("## Content\n\n")
        markdown_parts.append(data.get("content", ""))
        
    elif source_type == "json":
        markdown_parts.append(f"**Source File:** {data.get('source_path', 'N/A')}\n")
        markdown_parts.append("\n---\n\n")
        markdown_parts.append("## JSON Data\n\n")
        markdown_parts.append("```json\n")
        markdown_parts.append(json.dumps(data.get("data", {}), indent=2))
        markdown_parts.append("\n```\n\n")
        
        # If JSON contains specific fields, extract them
        json_data = data.get("data", {})
        if isinstance(json_data, dict):
            markdown_parts.append("## Extracted Information\n\n")
            
            if "product_name" in json_data:
                markdown_parts.append(f"**Product Name:** {json_data['product_name']}\n\n")
            
            if "description" in json_data:
                markdown_parts.append(f"**Description:** {json_data['description']}\n\n")
            
            if "features" in json_data and isinstance(json_data['features'], list):
                markdown_parts.append("**Features:**\n")
                for feature in json_data['features']:
                    markdown_parts.append(f"- {feature}\n")
                markdown_parts.append("\n")
        
    elif source_type == "url":
        markdown_parts.append(f"**Source URL:** {data.get('source_url', 'N/A')}\n")
        markdown_parts.append(f"**Content Type:** {data.get('metadata', {}).get('content_type', 'N/A')}\n")
        markdown_parts.append("\n---\n\n")
        markdown_parts.append("## Web Content\n\n")
        
        # Try to parse as JSON if content type suggests it
        content = data.get("content", "")
        content_type = data.get('metadata', {}).get('content_type', '')
        
        if 'json' in content_type:
            try:
                json_content = json.loads(content)
                markdown_parts.append("```json\n")
                markdown_parts.append(json.dumps(json_content, indent=2))
                markdown_parts.append("\n```\n")
            except json.JSONDecodeError:
                markdown_parts.append(content)
        else:
            markdown_parts.append(content)
    
    # Metadata footer
    markdown_parts.append("\n\n---\n\n")
    markdown_parts.append("## Metadata\n\n")
    
    metadata = data.get("metadata", {})
    for key, value in metadata.items():
        formatted_key = key.replace('_', ' ').title()
        markdown_parts.append(f"- **{formatted_key}:** {value}\n")
    
    return "".join(markdown_parts)


def get_next_available_filename(base_name: str = "context_input") -> Path:
    """
    Get the next available filename for context file.
    
    Args:
        base_name: Base name for the file (without extension)
        
    Returns:
        Path object for the next available filename
    """
    output_path = Path(f"{base_name}.md")
    
    if not output_path.exists():
        return output_path
    
    counter = 1
    while True:
        output_path = Path(f"{base_name}_{counter}.md")
        if not output_path.exists():
            return output_path
        counter += 1


def prompt_user(message: str, default: str = "y") -> str:
    """
    Prompt user for input with a default value.
    
    Args:
        message: The prompt message
        default: Default value if user just presses Enter
        
    Returns:
        User's response (lowercased)
    """
    response = input(f"{message} [{default}]: ").strip().lower()
    return response if response else default.lower()


def preview_content(content: str, max_lines: int = 20) -> None:
    """
    Display a preview of the content to the user.
    
    Args:
        content: The content to preview
        max_lines: Maximum number of lines to show
    """
    lines = content.split('\n')
    preview_lines = lines[:max_lines]
    
    print("\n" + "=" * 60)
    print("PREVIEW (first {} lines):".format(min(max_lines, len(lines))))
    print("=" * 60)
    print("\n".join(preview_lines))
    
    if len(lines) > max_lines:
        print(f"\n... ({len(lines) - max_lines} more lines)")
    
    print("=" * 60 + "\n")


def save_context_file(content: str, output_path: Path, preview: bool = False) -> bool:
    """
    Save the context file with user confirmation and preview.
    
    Args:
        content: The markdown content to save
        output_path: Path where to save the file
        preview: Whether to show preview before saving (default: False)
        
    Returns:
        True if file was saved successfully, False otherwise
    """
    if preview:
        preview_content(content)
        response = prompt_user("Do you want to preview the full content? (y/n)", "n")
        if response == "y":
            print("\n" + "=" * 60)
            print("FULL CONTENT:")
            print("=" * 60)
            print(content)
            print("=" * 60 + "\n")
    
    # Check if file exists
    if output_path.exists():
        print(f"\n⚠️  File '{output_path}' already exists.")
        response = prompt_user("Overwrite? (y/n)", "y")
        
        if response == "y":
            # Continue to save (overwrite)
            pass
        else:
            # n = create new numbered file
            base_name = output_path.stem
            output_path = get_next_available_filename(base_name)
            print(f"Creating new file: {output_path}")
    
    # Save the file
    try:
        output_path.write_text(content, encoding='utf-8')
        print(f"\n✅ Context file saved successfully: {output_path}")
        return True
    except Exception as e:
        print(f"\n❌ Error saving file: {e}")
        return False


def process_input(source: str, preview: bool = False, output_name: Optional[str] = None) -> bool:
    """
    Process input from file or URL and generate context file.
    
    Args:
        source: Path to file or URL
        preview: Whether to show preview before saving (default: False)
        output_name: Optional custom output filename (without extension)
        
    Returns:
        True if processing was successful, False otherwise
    """
    try:
        # Determine source type and read content
        if validate_url(source):
            print(f"📥 Fetching content from URL: {source}")
            data = fetch_url_content(source)
        else:
            source_path = Path(source)
            
            if not source_path.exists():
                print(f"❌ Error: Source not found: {source}")
                return False
            
            suffix = source_path.suffix.lower()
            
            if suffix == ".md":
                print(f"📄 Reading markdown file: {source}")
                data = read_markdown_file(source_path)
            elif suffix == ".json":
                print(f"📋 Reading JSON file: {source}")
                data = read_json_file(source_path)
            else:
                print(f"❌ Error: Unsupported file type: {suffix}")
                print("Supported types: .md, .json, or web URLs")
                return False
        
        print("✅ Source data loaded successfully")
        print("🔄 Converting to markdown context format...")
        
        # Convert to markdown context
        markdown_content = convert_to_markdown_context(data)
        
        # Determine output path
        base_name = output_name if output_name else "context_input"
        output_path = Path(f"{base_name}.md")
        
        # Save the file
        return save_context_file(markdown_content, output_path, preview)
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False
    except Exception as e:
        print(f"❌ Error processing input: {e}")
        return False


def main() -> int:
    """
    Main entry point for the script.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Generate standardized markdown context files from various sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.md
  %(prog)s data.json
  %(prog)s https://example.com/api/product
  %(prog)s input.md --preview
  %(prog)s data.json --output custom_context
        """
    )
    
    parser.add_argument(
        "source",
        help="Input source: path to .md or .json file, or a web URL"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Custom output filename (without extension)",
        default=None
    )
    
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show preview before saving"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Context File Generator")
    print("=" * 60 + "\n")
    
    success = process_input(
        source=args.source,
        preview=args.preview,
        output_name=args.output
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
