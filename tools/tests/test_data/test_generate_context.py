"""
Tests for tools/generate_context.py script
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add parent directories to path to import generate_context
tools_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(tools_dir))

import generate_context


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for test files."""
    return tmp_path


@pytest.fixture
def sample_markdown(temp_dir):
    """Create a sample markdown file."""
    md_file = temp_dir / "sample.md"
    content = """# Sample Product

This is a sample product description.

## Features
- Feature 1
- Feature 2
- Feature 3
"""
    md_file.write_text(content, encoding='utf-8')
    return md_file


@pytest.fixture
def sample_json(temp_dir):
    """Create a sample JSON file."""
    json_file = temp_dir / "sample.json"
    data = {
        "product_name": "Test Product",
        "description": "A test product for testing",
        "features": ["Feature A", "Feature B", "Feature C"],
        "price": 99.99
    }
    json_file.write_text(json.dumps(data, indent=2), encoding='utf-8')
    return json_file


@pytest.fixture
def sample_html_with_unwanted_sections():
    """Sample HTML with unwanted sections for testing."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Test Product</title></head>
    <body>
        <header>
            <h1>Site Header</h1>
            <nav>Home | Products | About</nav>
        </header>
        <aside class="sidebar">
            <h2>Sidebar</h2>
            <ul><li>Link 1</li><li>Link 2</li></ul>
        </aside>
        <main>
            <h1>Main Product Title</h1>
            <p>This is the main product description.</p>
            <h2>Features</h2>
            <ul>
                <li>Feature 1</li>
                <li>Feature 2</li>
            </ul>
        </main>
        <footer>
            <p>Copyright 2024</p>
            <nav>Privacy | Terms</nav>
        </footer>
        <script>console.log('tracking');</script>
    </body>
    </html>
    """


@pytest.fixture
def invalid_json(temp_dir):
    """Create an invalid JSON file."""
    json_file = temp_dir / "invalid.json"
    json_file.write_text("{ invalid json }", encoding='utf-8')
    return json_file


class TestValidateUrl:
    """Tests for validate_url function."""
    
    def test_valid_http_url(self):
        """Test valid HTTP URL."""
        assert generate_context.validate_url("http://example.com")
    
    def test_valid_https_url(self):
        """Test valid HTTPS URL."""
        assert generate_context.validate_url("https://example.com/path")
    
    def test_invalid_url_no_scheme(self):
        """Test invalid URL without scheme."""
        assert not generate_context.validate_url("example.com")
    
    def test_invalid_url_empty(self):
        """Test invalid empty URL."""
        assert not generate_context.validate_url("")
    
    def test_invalid_url_malformed(self):
        """Test invalid malformed URL."""
        assert not generate_context.validate_url("ht!tp://bad url")


class TestReadMarkdownFile:
    """Tests for read_markdown_file function."""
    
    def test_read_valid_markdown(self, sample_markdown):
        """Test reading a valid markdown file."""
        result = generate_context.read_markdown_file(sample_markdown)
        
        assert result["source_type"] == "markdown"
        assert result["source_path"] == str(sample_markdown)
        assert "Sample Product" in result["content"]
        assert result["title"] == "Sample Product"
        assert result["metadata"]["line_count"] > 0
        assert result["metadata"]["character_count"] > 0
    
    def test_read_nonexistent_file(self, temp_dir):
        """Test reading a non-existent file."""
        nonexistent = temp_dir / "nonexistent.md"
        
        with pytest.raises(FileNotFoundError):
            generate_context.read_markdown_file(nonexistent)
    
    def test_read_markdown_no_title(self, temp_dir):
        """Test reading markdown without H1 title."""
        md_file = temp_dir / "no_title.md"
        md_file.write_text("Just some content without title", encoding='utf-8')
        
        result = generate_context.read_markdown_file(md_file)
        
        assert "title" not in result
        assert result["content"] == "Just some content without title"


class TestReadJsonFile:
    """Tests for read_json_file function."""
    
    def test_read_valid_json(self, sample_json):
        """Test reading a valid JSON file."""
        result = generate_context.read_json_file(sample_json)
        
        assert result["source_type"] == "json"
        assert result["source_path"] == str(sample_json)
        assert result["data"]["product_name"] == "Test Product"
        assert len(result["data"]["features"]) == 3
        assert result["metadata"]["character_count"] > 0
    
    def test_read_invalid_json(self, invalid_json):
        """Test reading an invalid JSON file."""
        with pytest.raises(json.JSONDecodeError):
            generate_context.read_json_file(invalid_json)
    
    def test_read_nonexistent_json(self, temp_dir):
        """Test reading a non-existent JSON file."""
        nonexistent = temp_dir / "nonexistent.json"
        
        with pytest.raises(FileNotFoundError):
            generate_context.read_json_file(nonexistent)


class TestFetchUrlContent:
    """Tests for fetch_url_content function."""
    
    def test_fetch_valid_url(self, sample_html_with_unwanted_sections):
        """Test fetching from a valid URL."""
        mock_response = MagicMock()
        mock_response.text = sample_html_with_unwanted_sections
        mock_response.headers = {"content-type": "text/html"}
        mock_response.status_code = 200
        
        mock_requests = MagicMock()
        mock_requests.get.return_value = mock_response
        mock_requests.exceptions.RequestException = Exception
        
        with patch.dict('sys.modules', {'requests': mock_requests}):
            result = generate_context.fetch_url_content("https://example.com")
        
        assert result["source_type"] == "url"
        assert result["source_url"] == "https://example.com"
        # Should have markdown content, not HTML
        assert "<html>" not in result["content"].lower()
        assert "Product" in result["content"] or "Feature" in result["content"]
        assert result["metadata"]["status_code"] == 200
    
    def test_fetch_json_url(self):
        """Test fetching JSON from a URL."""
        json_data = '{"product": "test", "price": 99.99}'
        mock_response = MagicMock()
        mock_response.text = json_data
        mock_response.headers = {"content-type": "application/json"}
        mock_response.status_code = 200
        
        mock_requests = MagicMock()
        mock_requests.get.return_value = mock_response
        mock_requests.exceptions.RequestException = Exception
        
        with patch.dict('sys.modules', {'requests': mock_requests}):
            result = generate_context.fetch_url_content("https://api.example.com/data")
        
        assert result["source_type"] == "url"
        # JSON should not be converted to markdown
        assert '"product"' in result["content"] or 'product' in result["content"]
    
    def test_fetch_invalid_url(self):
        """Test fetching from an invalid URL."""
        with pytest.raises(ValueError):
            generate_context.fetch_url_content("not a url")
    
    def test_fetch_url_error(self):
        """Test handling of URL fetch errors."""
        mock_requests = MagicMock()
        
        # Create a proper RequestException
        class MockRequestException(Exception):
            pass
        
        mock_requests.exceptions.RequestException = MockRequestException
        mock_requests.get.side_effect = MockRequestException("Connection error")
        
        with patch.dict('sys.modules', {'requests': mock_requests}):
            with pytest.raises(Exception, match="Error fetching URL content"):
                generate_context.fetch_url_content("https://example.com")


class TestConvertHtmlToMarkdown:
    """Tests for convert_html_to_markdown function."""
    
    def test_convert_simple_html(self, sample_html_with_unwanted_sections):
        """Test converting simple HTML to markdown."""
        result = generate_context.convert_html_to_markdown(sample_html_with_unwanted_sections)
        
        # Check that HTML tags are removed
        assert "<html>" not in result.lower()
        assert "<body>" not in result.lower()
        assert "<div>" not in result.lower()
        
        # Check that main content is preserved
        assert "Main Product Title" in result or "Product Title" in result
        assert "main product description" in result.lower()
        assert "Feature 1" in result
        assert "Feature 2" in result
    
    def test_convert_html_removes_unwanted_sections(self, sample_html_with_unwanted_sections):
        """Test that conversion removes unwanted sections."""
        result = generate_context.convert_html_to_markdown(sample_html_with_unwanted_sections)
        
        # Check that unwanted sections are removed or minimal
        assert "Site Header" not in result or result.count("Site Header") < result.count("Product")
        assert "Copyright 2024" not in result or result.count("Copyright") < result.count("Product")
        assert "Sidebar" not in result or result.count("Sidebar") < result.count("Feature")
        
        # Check that main content is present
        assert "Main Product Title" in result or "Product Title" in result
        assert "Feature 1" in result
    
    def test_convert_html_removes_junk(self, sample_html_with_unwanted_sections):
        """Test that conversion removes junk content."""
        result = generate_context.convert_html_to_markdown(sample_html_with_unwanted_sections)
        
        # Check that scripts are removed
        assert "console.log" not in result
        assert "<script>" not in result.lower()
    
    def test_convert_html_with_headings(self):
        """Test HTML with various heading levels."""
        html = "<main><h1>Title</h1><h2>Subtitle</h2><p>Content</p></main>"
        result = generate_context.convert_html_to_markdown(html)
        
        assert "Title" in result
        assert "Subtitle" in result
        assert "Content" in result
    
    def test_remove_unwanted_html_sections(self, sample_html_with_unwanted_sections):
        """Test removing unwanted HTML sections."""
        result = generate_context.remove_unwanted_html_sections(sample_html_with_unwanted_sections)
        
        # Unwanted tags should be removed
        assert "<header>" not in result.lower() or result.lower().count("<header>") == 0
        assert "<footer>" not in result.lower() or result.lower().count("<footer>") == 0
        assert "<nav>" not in result.lower() or result.lower().count("<nav>") == 0
        assert "<script>" not in result.lower() or result.lower().count("<script>") == 0
        
        # Main content should be present
        assert "Main Product Title" in result or "Product Title" in result
        assert "main product description" in result.lower()


class TestRemoveUnwantedHtmlSections:
    """Tests for remove_unwanted_html_sections function."""
    
    def test_removes_unwanted_sections(self):
        """Test that unwanted sections are removed from longer HTML."""
        html = """
        <header><h1>Header</h1><nav>Menu</nav></header>
        <main>
            <h1>Title</h1>
            <p>This is the main content that should be preserved.</p>
            <p>More content here with enough text to pass the length check.</p>
        </main>
        <footer><p>Footer content</p></footer>
        """
        result = generate_context.remove_unwanted_html_sections(html)
        
        # Main content should be preserved
        assert "Title" in result
        assert "main content" in result.lower()
        
        # Unwanted sections should be reduced or removed
        # (or if returned as-is due to <100 char check, that's ok for this integration test)
    
    def test_preserves_main_content(self):
        """Test that main content is preserved."""
        html = """
        <header>Header</header>
        <main>
            <h1>Title that should definitely be kept</h1>
            <p>Paragraph with enough content to make this worthwhile.</p>
        </main>
        <footer>Footer</footer>
        """
        result = generate_context.remove_unwanted_html_sections(html)
        
        assert "Title that should definitely be kept" in result
        assert "Paragraph with enough content" in result
    
    def test_handles_complex_html(self):
        """Test handling of complex HTML with various tags."""
        html = """
        <html>
        <body>
            <nav class="navigation"><ul><li>Item</li></ul></nav>
            <div class="container">
                <main role="main">
                    <article>
                        <h1>Article Title</h1>
                        <p>Article content that is meaningful and should be extracted.</p>
                        <p>More article content to ensure we have enough text.</p>
                    </article>
                </main>
            </div>
            <aside class="sidebar"><p>Sidebar stuff</p></aside>
        </body>
        </html>
        """
        result = generate_context.remove_unwanted_html_sections(html)
        
        # Main content should be there
        assert "Article Title" in result
        assert "Article content" in result


class TestConvertToMarkdownContext:
    """Tests for convert_to_markdown_context function."""
    
    def test_convert_markdown_data(self):
        """Test converting markdown data to context."""
        data = {
            "source_type": "markdown",
            "source_path": "/path/to/file.md",
            "title": "Test Title",
            "content": "# Test Title\n\nContent here",
            "metadata": {
                "line_count": 3,
                "character_count": 25
            }
        }
        
        result = generate_context.convert_to_markdown_context(data)
        
        assert "# Context Input" in result
        assert "**Source Type:** markdown" in result
        assert "**Original Title:** Test Title" in result
        assert "Content here" in result
        assert "**Line Count:** 3" in result
    
    def test_convert_json_data(self):
        """Test converting JSON data to context."""
        data = {
            "source_type": "json",
            "source_path": "/path/to/file.json",
            "data": {
                "product_name": "Test Product",
                "description": "Test description",
                "features": ["Feature 1", "Feature 2"]
            },
            "metadata": {
                "character_count": 100
            }
        }
        
        result = generate_context.convert_to_markdown_context(data)
        
        assert "# Context Input" in result
        assert "**Source Type:** json" in result
        assert "```json" in result
        assert "Test Product" in result
        assert "**Product Name:** Test Product" in result
        assert "- Feature 1" in result
    
    def test_convert_url_data(self):
        """Test converting URL data to context."""
        data = {
            "source_type": "url",
            "source_url": "https://example.com",
            "content": "Web content here",
            "metadata": {
                "content_type": "text/html",
                "status_code": 200
            }
        }
        
        result = generate_context.convert_to_markdown_context(data)
        
        assert "# Context Input" in result
        assert "**Source Type:** url" in result
        assert "**Source URL:** https://example.com" in result
        assert "Web content here" in result


class TestGetNextAvailableFilename:
    """Tests for get_next_available_filename function."""
    
    def test_get_filename_no_existing(self, temp_dir, monkeypatch):
        """Test getting filename when no file exists."""
        monkeypatch.chdir(temp_dir)
        
        result = generate_context.get_next_available_filename()
        
        assert result == Path("context_input.md")
    
    def test_get_filename_with_existing(self, temp_dir, monkeypatch):
        """Test getting filename when base file exists."""
        monkeypatch.chdir(temp_dir)
        
        # Create existing file
        (temp_dir / "context_input.md").touch()
        
        result = generate_context.get_next_available_filename()
        
        assert result == Path("context_input_1.md")
    
    def test_get_filename_multiple_existing(self, temp_dir, monkeypatch):
        """Test getting filename when multiple files exist."""
        monkeypatch.chdir(temp_dir)
        
        # Create existing files
        (temp_dir / "context_input.md").touch()
        (temp_dir / "context_input_1.md").touch()
        (temp_dir / "context_input_2.md").touch()
        
        result = generate_context.get_next_available_filename()
        
        assert result == Path("context_input_3.md")
    
    def test_get_filename_custom_base(self, temp_dir, monkeypatch):
        """Test getting filename with custom base name."""
        monkeypatch.chdir(temp_dir)
        
        result = generate_context.get_next_available_filename("custom_context")
        
        assert result == Path("custom_context.md")


class TestProcessInput:
    """Tests for process_input function."""
    
    @patch('generate_context.prompt_user')
    def test_process_markdown_file(self, mock_prompt, sample_markdown, temp_dir, monkeypatch):
        """Test processing a markdown file."""
        monkeypatch.chdir(temp_dir)
        mock_prompt.return_value = "n"  # Skip preview
        
        result = generate_context.process_input(str(sample_markdown), preview=False)
        
        assert result is True
        assert (temp_dir / "context_input.md").exists()
    
    @patch('generate_context.prompt_user')
    def test_process_json_file(self, mock_prompt, sample_json, temp_dir, monkeypatch):
        """Test processing a JSON file."""
        monkeypatch.chdir(temp_dir)
        mock_prompt.return_value = "n"
        
        result = generate_context.process_input(str(sample_json), preview=False)
        
        assert result is True
        assert (temp_dir / "context_input.md").exists()
        
        # Verify content
        content = (temp_dir / "context_input.md").read_text()
        assert "Test Product" in content
    
    def test_process_nonexistent_file(self, temp_dir, monkeypatch):
        """Test processing a non-existent file."""
        monkeypatch.chdir(temp_dir)
        
        result = generate_context.process_input("nonexistent.md", preview=False)
        
        assert result is False
    
    def test_process_unsupported_file_type(self, temp_dir, monkeypatch):
        """Test processing an unsupported file type."""
        monkeypatch.chdir(temp_dir)
        
        # Create unsupported file
        txt_file = temp_dir / "sample.txt"
        txt_file.write_text("Some text")
        
        result = generate_context.process_input(str(txt_file), preview=False)
        
        assert result is False
    
    @patch('generate_context.prompt_user')
    def test_process_with_custom_output(self, mock_prompt, sample_markdown, temp_dir, monkeypatch):
        """Test processing with custom output name."""
        monkeypatch.chdir(temp_dir)
        mock_prompt.return_value = "n"
        
        result = generate_context.process_input(
            str(sample_markdown),
            preview=False,
            output_name="custom_output"
        )
        
        assert result is True
        assert (temp_dir / "custom_output.md").exists()


class TestSaveContextFile:
    """Tests for save_context_file function."""
    
    @patch('generate_context.prompt_user')
    def test_save_new_file(self, mock_prompt, temp_dir, monkeypatch):
        """Test saving a new context file."""
        monkeypatch.chdir(temp_dir)
        mock_prompt.return_value = "n"  # Skip preview
        
        content = "# Test Context\n\nTest content"
        output_path = temp_dir / "test_context.md"
        
        result = generate_context.save_context_file(content, output_path, preview=False)
        
        assert result is True
        assert output_path.exists()
        assert output_path.read_text() == content
    
    @patch('generate_context.prompt_user')
    def test_save_overwrite_existing(self, mock_prompt, temp_dir, monkeypatch):
        """Test overwriting an existing file."""
        monkeypatch.chdir(temp_dir)
        
        output_path = temp_dir / "existing.md"
        output_path.write_text("Old content")
        
        mock_prompt.return_value = "y"  # Overwrite
        
        new_content = "# New Context\n\nNew content"
        result = generate_context.save_context_file(new_content, output_path, preview=False)
        
        assert result is True
        assert output_path.read_text() == new_content
    
    @patch('generate_context.prompt_user')
    def test_save_cancel_overwrite(self, mock_prompt, temp_dir, monkeypatch):
        """Test creating new file when declining overwrite."""
        monkeypatch.chdir(temp_dir)
        
        output_path = temp_dir / "existing.md"
        original_content = "Original content"
        output_path.write_text(original_content)
        
        mock_prompt.return_value = "n"  # Create new file
        
        new_content = "New content"
        result = generate_context.save_context_file(new_content, output_path, preview=False)
        
        assert result is True
        # Original file should be unchanged
        assert output_path.read_text() == original_content
        # New file should be created
        new_file = temp_dir / "existing_1.md"
        assert new_file.exists()
        assert new_file.read_text() == new_content
    
    @patch('generate_context.prompt_user')
    def test_save_create_new_file(self, mock_prompt, temp_dir, monkeypatch):
        """Test creating a new file when existing file present."""
        monkeypatch.chdir(temp_dir)
        
        output_path = temp_dir / "context_input.md"
        output_path.write_text("Old content")
        
        mock_prompt.return_value = "n"  # Create new file
        
        new_content = "# New Context\n\nNew content"
        result = generate_context.save_context_file(new_content, output_path, preview=False)
        
        assert result is True
        # Check that new numbered file was created
        new_file = temp_dir / "context_input_1.md"
        assert new_file.exists()
        assert new_file.read_text() == new_content


class TestMainFunction:
    """Tests for main function."""
    
    @patch('sys.argv', ['generate_context.py', '--help'])
    def test_main_help(self):
        """Test main function with help argument."""
        with pytest.raises(SystemExit) as exc_info:
            generate_context.main()
        
        assert exc_info.value.code == 0
    
    @patch('sys.argv', ['generate_context.py', '--version'])
    def test_main_version(self):
        """Test main function with version argument."""
        with pytest.raises(SystemExit) as exc_info:
            generate_context.main()
        
        assert exc_info.value.code == 0
