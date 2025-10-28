# Context File Generator

A Python script to generate standardized markdown context files from various input sources for AI agents and content planning workflows.

## Overview

Successfully created `generate_context.py`, a comprehensive Python script that converts various input sources into standardized markdown context files for AI agents and content planning workflows.

## Features

- **Multiple Input Sources**: Accepts `.md` files, `.json` files, or web URLs
- **Validation**: Parses and validates source data for completeness and correctness
- **Standardized Output**: Converts input into a consistent markdown format (`context_input.md`)
- **Smart File Management**: 
  - Prompts before overwriting existing files
  - Auto-generates numbered filenames (`context_input_1.md`, `context_input_2.md`, etc.)
- **Preview Mode**: Optional preview of generated content before saving
- **Error Handling**: Graceful error handling with clear user feedback
- **Extensible**: Designed for easy integration and future enhancements
- **HTML to Markdown Conversion**: Automatic conversion of web content to clean markdown
- **Comprehensive Test Suite**: 41 tests covering all functionality

## Installation

The script is part of the content-planner project. Required dependencies:

```bash
# Install dependencies using uv
uv sync

# If you plan to fetch content from URLs, requests is already included
```

## Key Functions

- `validate_url()` - URL validation
- `read_markdown_file()` - Parse markdown files
- `read_json_file()` - Parse JSON files with validation
- `fetch_url_content()` - Fetch content from web URLs
- `convert_html_to_markdown()` - Convert HTML to markdown
- `remove_unwanted_html_sections()` - Clean HTML by removing unwanted sections
- `convert_to_markdown_context()` - Convert to standardized format
- `get_next_available_filename()` - Smart filename generation
- `save_context_file()` - Save with user confirmation
- `process_input()` - Main processing pipeline
- `main()` - CLI entry point

## Usage

### Basic Usage

```bash
# From a markdown file
uv run python tools/generate_context.py input.md

# From a JSON file
uv run python tools/generate_context.py data.json

# From a web URL
uv run python tools/generate_context.py https://example.com/api/product
```

### Advanced Options

```bash
# Show preview before saving
uv run python tools/generate_context.py input.md --preview

# Custom output filename
uv run python tools/generate_context.py data.json --output custom_context

# Both preview and custom output
uv run python tools/generate_context.py input.md --preview --output my_context

# Show help
uv run python tools/generate_context.py --help

# Show version
uv run python tools/generate_context.py --version
```

## Input Formats

### Markdown Files (.md)

The script reads markdown files and preserves their content structure:

```markdown
# Product Title

This is the product description.

## Features
- Feature 1
- Feature 2
```

### JSON Files (.json)

JSON files are parsed and formatted with special extraction for common fields:

```json
{
  "product_name": "My Product",
  "description": "Product description",
  "features": ["Feature A", "Feature B"],
  "price": 99.99
}
```

The script automatically extracts and highlights:
- `product_name`
- `description`
- `features` (as a bulleted list)

### Web URLs

The script can fetch content from web URLs and **automatically converts HTML to clean markdown**:
- Plain text content (preserved as-is)
- JSON responses (automatically formatted)
- HTML content (converted to clean, readable markdown)

**How it works:**
1. Fetches HTML from URL
2. Converts HTML to markdown
3. Cleans up excessive whitespace and junk patterns

**Example:**
```bash
# Fetch and convert HTML page to markdown
uv run python tools/generate_context.py https://example.com/product-page --preview
```

The HTML to markdown conversion:
- Removes unnecessary HTML tags and attributes
- Cleans up excessive whitespace
- Preserves headings, paragraphs, lists, and links
- Filters out common junk like "Advertisement", "Loading...", etc.
- Produces concise, AI-friendly markdown

**Optional HTML Cleaning:**
The `remove_unwanted_html_sections()` function is available for manual HTML preprocessing if needed:
- Removes `<header>`, `<footer>`, `<nav>`, `<aside>`, `<script>`, `<style>`, `<iframe>` tags
- Removes elements with classes: sidebar, navigation, menu, advertisement
- Extracts main content only
- Requires BeautifulSoup4 library

## Output Format

The generated `context_input.md` file follows this structure:

```markdown
# Context Input

**Source Type:** [markdown|json|url]
**Source File/URL:** [path or URL]

---

## Content

[Extracted and formatted content]

---

## Metadata

- **Line Count:** 42
- **Character Count:** 1234
```

## Interactive Features

### File Overwrite Protection

When `context_input.md` already exists, you'll be prompted:

```
⚠️  File 'context_input.md' already exists.
Overwrite? (y/n) [y]:
```

Options:
- `y`: Overwrite the existing file (default)
- `n`: Create a new numbered file (`context_input_1.md`)

### Preview Mode

By default, files are saved without preview. To see a preview before saving, use the `--preview` flag:

```bash
uv run python generate_context.py input.md --preview
```

You'll see the first 20 lines:

```
============================================================
PREVIEW (first 20 lines):
============================================================
# Context Input
**Source Type:** markdown
...
============================================================

Do you want to preview the full content? (y/n) [n]:
```

## Examples

### Example 1: Product Markdown File

**Input** (`product.md`):
```markdown
# Smart Watch Pro

The ultimate fitness companion.

## Key Features
- Heart rate monitoring
- GPS tracking
- 7-day battery life
```

**Command**:
```bash
uv run python generate_context.py product.md
```

**Output** (`context_input.md`):
```markdown
# Context Input

**Source Type:** markdown
**Source File:** product.md
**Original Title:** Smart Watch Pro

---

## Content

# Smart Watch Pro

The ultimate fitness companion.

## Key Features
- Heart rate monitoring
- GPS tracking
- 7-day battery life

---

## Metadata

- **Line Count:** 9
- **Character Count:** 143
```

### Example 2: Product JSON File

**Input** (`product.json`):
```json
{
  "product_name": "Smart Watch Pro",
  "description": "The ultimate fitness companion",
  "features": [
    "Heart rate monitoring",
    "GPS tracking",
    "7-day battery life"
  ],
  "price": 299.99
}
```

**Command**:
```bash
uv run python generate_context.py product.json --output smartwatch_context
```

**Output** (`smartwatch_context.md`):
Includes the JSON data in a code block plus extracted fields in markdown format.

### Example 3: Web URL (HTML to Markdown)

**Command**:
```bash
uv run python tools/generate_context.py https://example.com/products/smartwatch --preview
```

**What happens:**
1. Fetches HTML from the URL
2. Removes unwanted sections (header, footer, nav, sidebar)
3. Extracts main content only
4. Automatically converts HTML to clean markdown
5. Shows preview of the converted markdown
6. Saves as `context_input.md`

**Output** (`context_input.md`):
```markdown
# Context Input

**Source Type:** url
**Source URL:** https://example.com/products/smartwatch
**Content Type:** text/markdown (converted from HTML)

---

## Web Content

# Smart Watch Pro

The ultimate fitness companion...

[Clean markdown content without HTML tags]

---

## Metadata

- **Content Type:** text/markdown (converted from HTML)
- **Character Count:** 2350
- **Status Code:** 200
```

## Integration with Content Planner

This script integrates seamlessly with the main content planner workflow:

1. **Prepare Context**: Use `generate_context.py` to create standardized input
2. **Run Content Planner**: Load the generated `context_input.md` in the main application
3. **Generate Ideas**: The AI uses the standardized context to generate content ideas

## Error Handling

The script provides clear error messages for common issues:

- **File Not Found**: `❌ File not found: input.md`
- **Invalid JSON**: `❌ Invalid JSON format: Expecting property name enclosed in double quotes`
- **Invalid URL**: `❌ Error: Invalid URL format: not-a-url`
- **Network Error**: `❌ Error fetching URL content: Connection timeout`
- **Unsupported Format**: `❌ Error: Unsupported file type: .txt`

## Testing

Run the test suite:

```bash
# Run all tests
uv run pytest tests/test_data/test_generate_context.py -v

# Run specific test class
uv run pytest tests/test_data/test_generate_context.py::TestReadMarkdownFile -v

# Run with coverage
uv run pytest tests/test_data/test_generate_context.py --cov=generate_context
```

### Test Coverage

**Test Suite:** `tests/test_data/test_generate_context.py`

**Test Results:**
- ✅ 41 tests total, all passing
- ✅ URL validation (5 tests)
- ✅ Markdown file reading (3 tests)
- ✅ JSON file reading (3 tests)
- ✅ URL content fetching (4 tests)
- ✅ HTML to markdown conversion (5 tests)
- ✅ HTML section removal (3 tests)
- ✅ Markdown conversion (3 tests)
- ✅ Filename generation (4 tests)
- ✅ Input processing (5 tests)
- ✅ File saving (4 tests)
- ✅ Main function (2 tests)

**Test Execution:**
```bash
# Run all generate_context tests
uv run pytest tests/test_data/test_generate_context.py -v

# Run all project tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/test_data/test_generate_context.py --cov=generate_context
```

## Development

### Adding New Input Formats

To add support for a new input format:

1. Create a new parsing function (e.g., `read_xml_file()`)
2. Add format detection in `process_input()`
3. Update `convert_to_markdown_context()` to handle the new source type
4. Add corresponding tests

### Extending Markdown Output

Modify `convert_to_markdown_context()` to customize the output format or add new sections.

## Requirements

- Python 3.13+
- ollama >= 0.4.0
- python-dotenv >= 1.0.0
- requests >= 2.32.3 (for URL fetching)
- html2text >= 2024.2.26 (for HTML to markdown conversion)
- beautifulsoup4 >= 4.14.2 (optional, for HTML section removal)
- pytest >= 8.0.0 (for testing)

## Technical Specifications

### Language & Tools
- Python 3.13+
- Type hints throughout
- Docstrings for all functions
- PEP 8 compliant code
- uv for dependency management

### Architecture
```
Input Source → Validation → Parsing → Conversion → Preview → Save
     ↓              ↓           ↓          ↓          ↓        ↓
(.md/json/url)   (format)   (extract)  (markdown)  (user)  (file)
```

### Code Quality Standards
- ✅ Type hints on all functions
- ✅ Comprehensive docstrings
- ✅ PEP 8 style compliance
- ✅ Descriptive variable names
- ✅ Modular design
- ✅ Error handling throughout
- ✅ User-friendly messages
- ✅ Extensive test coverage

### Best Practices
- ✅ No hardcoded values
- ✅ Environment-safe (no secrets in code)
- ✅ Cross-platform compatible (uses pathlib)
- ✅ Modern Python features (f-strings, Path, type hints)
- ✅ Organized code structure
- ✅ Clear function separation

## License

See LICENSE.md in the project root.

## Contributing

1. Follow the coding guidelines in AGENTS.md
2. Add tests for new features
3. Run the test suite before submitting PRs
4. Use descriptive commit messages

## Troubleshooting

**Issue**: `ImportError: No module named 'requests'`  
**Solution**: Install requests using `uv add requests`

**Issue**: `ImportError: No module named 'html2text'`  
**Solution**: Install html2text using `uv add html2text`

**Issue**: `ImportError: No module named 'bs4'` (BeautifulSoup)  
**Solution**: Install beautifulsoup4 using `uv add beautifulsoup4` (optional dependency)

**Issue**: Permission denied when saving file  
**Solution**: Check file permissions or specify a different output location

**Issue**: URL fetch timeout  
**Solution**: Check network connection or increase timeout in the code

**Issue**: HTML conversion produces messy output  
**Solution**: The script automatically cleans HTML. For additional cleaning, use the `remove_unwanted_html_sections()` function manually

## Quick Reference

### Quick Start Commands

```bash
# Basic usage
uv run python tools/generate_context.py <input_file_or_url>

# With options
uv run python tools/generate_context.py <input> --output <name> --preview
```

### Common Commands

```bash
# Generate from markdown file (no preview)
uv run python tools/generate_context.py input.md

# Generate from JSON with custom name
uv run python tools/generate_context.py data.json --output product_context

# Generate with preview before saving
uv run python tools/generate_context.py data.json --preview

# Generate from URL
uv run python tools/generate_context.py https://example.com/product

# Show help
uv run python tools/generate_context.py --help
```

### Command Options Summary

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--output` | `-o` | Custom output filename (without .md) | `-o my_context` |
| `--preview` | N/A | Show preview before saving | `--preview` |
| `--help` | `-h` | Show help message | `--help` |
| `--version` | N/A | Show version | `--version` |

### File Handling Quick Guide

**When file exists:**
```
⚠️  File 'context_input.md' already exists.
Overwrite? (y/n) [y]:
```

**Options:**
- `y` - Overwrite existing file (default)
- `n` - Create numbered file (`context_input_1.md`)

**Output files:**
- Default: `context_input.md`
- Custom: `<your_name>.md`
- Numbered: `context_input_1.md`, `context_input_2.md`, etc.

### Tips & Tricks

1. **Fast workflow**: Default is no preview for quick processing
2. **Review important files**: Use `--preview` for critical content
3. **Batch work**: Use custom output names to avoid overwriting
4. **JSON APIs**: Direct URL fetching works with JSON APIs
5. **Markdown files**: H1 headers are automatically extracted as titles
6. **Version tracking**: Numbered files help track different versions

## Future Enhancements

- [ ] Support for XML files
- [ ] Support for CSV files
- [ ] Batch processing of multiple files
- [ ] Custom templates for output format
- [ ] Configuration file support
- [ ] Integration with cloud storage (S3, Drive, etc.)
- [ ] GUI interface
- [ ] Plugin system for custom parsers

## Contact

For issues or questions, refer to the main project documentation or create an issue in the repository.
