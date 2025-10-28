# Test Data

This directory contains test data and example files for the `generate_context.py` script.

## Example Input Files

### Markdown Files

**product_smartwatch.md**
- Comprehensive product documentation
- Includes specifications, features, pricing
- Good example of structured markdown content

**product_headphones.md**
- Simple product description
- Demonstrates basic markdown usage
- Includes key features and use cases

### JSON Files

**product_vacuum.json**
- Complex nested JSON structure
- Includes arrays, objects, and various data types
- Good example for testing JSON parsing and extraction

## Generated Output Files

These files are generated during testing:

- `vacuum_context.md` - Output from processing product_vacuum.json
- `context_input_*.md` - Various numbered output files from tests
- `test_output.md` - Test output file

## Usage with generate_context.py

```bash
# Process markdown file
uv run python tools/generate_context.py tests/test_data/product_smartwatch.md

# Process JSON file
uv run python tools/generate_context.py tests/test_data/product_vacuum.json

# With custom output name
uv run python tools/generate_context.py tests/test_data/product_headphones.md --output headphones_context

# With preview
uv run python tools/generate_context.py tests/test_data/product_smartwatch.md --preview
```

## File Descriptions

| File | Type | Size | Description |
|------|------|------|-------------|
| product_smartwatch.md | Markdown | 2.3 KB | Detailed smartwatch product info |
| product_vacuum.json | JSON | 2.8 KB | Robot vacuum product data |
| product_headphones.md | Markdown | 1.7 KB | Wireless headphones description |

## Adding New Test Data

When adding new test data:

1. Place the file in this directory
2. Follow the naming convention: `product_<name>.<ext>`
3. Ensure the file is valid (valid JSON, proper markdown, etc.)
4. Add description to this README
5. Consider adding tests in `test_generate_context.py` if needed

## Testing

These files are used by the test suite in `tests/test_generate_context.py`:

```bash
# Run all tests
uv run pytest tests/test_generate_context.py -v

# Run specific test with these files
uv run pytest tests/test_generate_context.py::TestProcessInput -v
```
