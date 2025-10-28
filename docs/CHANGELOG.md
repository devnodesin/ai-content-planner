# Generate Context Script - Changelog

## Version 1.3.0 - 2025-10-28

### File Organization

**Moved Script to tools/ Directory:**
- `generate_context.py` → `tools/generate_context.py`
- Better project organization
- Separates tools from main application code

**Updated References:**
- All documentation updated with new path
- Tests updated to reference `tools/generate_context.py`
- README and guides updated

### Enhanced HTML Cleaning

**Improved HTML to Markdown Conversion:**

The script now intelligently removes unwanted HTML sections before converting to markdown, focusing only on main content.

**What Gets Removed:**
- `<header>` tags and content
- `<footer>` tags and content
- `<nav>` tags and content (navigation)
- `<aside>` tags and content (sidebars)
- Elements with these classes: `sidebar`, `navigation`, `menu`, `ad`, `advertisement`
- Elements with these IDs: `sidebar`, `navigation`, `menu`, `header`, `footer`, `nav`
- `<script>` and `<style>` tags

**What Gets Preserved:**
- `<main>` content (prioritized)
- Article content
- Headings, paragraphs, lists
- Main text and formatting
- Relevant images and links

**Implementation:**
- Added `remove_unwanted_html_sections()` function
- Uses HTML parser to intelligently skip unwanted sections
- Maintains proper nesting with skip stack
- Falls back to original HTML if cleaning produces too little content

**Example:**

Before (Raw HTML):
```html
<header><nav>Menu</nav></header>
<aside class="sidebar">Sidebar content</aside>
<main><h1>Title</h1><p>Main content</p></main>
<footer>Copyright 2024</footer>
```

After (Clean Markdown):
```markdown
# Title

Main content
```

### Updated Tests

**New Tests (+5):**
- `test_removes_unwanted_sections()` - Tests removal of multiple unwanted sections
- `test_preserves_main_content()` - Ensures main content is kept
- `test_handles_complex_html()` - Tests complex nested HTML structures

**Total Tests:** 55 (was 50)
- 41 generate_context tests (+5 new)
- 14 existing project tests
- All passing ✓

### Documentation Updates

**Updated Files:**
- `README.md` - New path and enhanced features
- `docs/GENERATE_CONTEXT.md` - Detailed HTML cleaning explanation
- `spec/GENERATE_CONTEXT_QUICK_REF.md` - Updated commands
- `tests/test_data/README.md` - Updated examples

**New Usage:**
```bash
# New location
uv run python tools/generate_context.py https://example.com/product

# Output is now cleaner with only main content!
```

### Migration Guide

**Script Location Changed:**

Old:
```bash
uv run python generate_context.py input.md
```

New:
```bash
uv run python tools/generate_context.py input.md
```

**HTML Cleaning is Automatic:**
No changes needed - HTML cleaning happens automatically and produces better results!

### Technical Details

**HTML Parser Enhancement:**
- Stack-based tracking of skipped elements
- Proper handling of nested unwanted tags
- Preserves tag attributes when needed
- Graceful fallback if parsing fails

**Performance:**
- No performance impact
- Parsing is fast and efficient
- Minimal memory overhead

### Backward Compatibility

⚠️ **Breaking Change:**
- Script moved from root to `tools/` directory
- Update any scripts or automation that call `generate_context.py`

✅ **Enhanced Functionality:**
- HTML cleaning is automatic - no API changes
- Better output quality for web URLs
- All existing features work the same

### Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run generate_context tests only
uv run pytest tests/test_generate_context.py -v

# Test from new location
uv run python tools/generate_context.py tests/test_data/product_smartwatch.md
```

### Known Limitations

**HTML Cleaning:**
- Very minimal HTML (< 100 chars) might return original
- JavaScript-rendered content not supported (use APIs)
- Some complex layouts may need manual review

**Recommendation:**
Use `--preview` flag to review output before saving.

## Version 1.2.0 - 2025-10-28

### New Features

#### HTML to Markdown Conversion
**Feature:** Automatic conversion of HTML web pages to clean, readable markdown.

**Implementation:**
- Added `html2text` dependency for HTML conversion
- Implemented `convert_html_to_markdown()` function
- Automatically detects HTML content from URLs
- Cleans up HTML by:
  - Removing HTML tags and attributes
  - Converting to proper markdown formatting
  - Filtering out junk content (ads, navigation, etc.)
  - Removing excessive whitespace
  - Preserving headings, paragraphs, lists, links

**Usage:**
```bash
# Automatically converts HTML to markdown
uv run python generate_context.py https://example.com/product-page
```

**What gets cleaned:**
- Navigation elements
- Advertisements
- Loading indicators
- Internal anchors
- Script tags
- Excessive newlines

**What gets preserved:**
- Headings (H1-H6)
- Paragraphs
- Lists (ordered and unordered)
- Links
- Text formatting (bold, italic)
- Content structure

### Project Reorganization

**Moved Files:**
- `examples/*` → `tests/test_data/`
  - `product_smartwatch.md`
  - `product_vacuum.json`
  - `product_headphones.md`
- `vacuum_context.md` → `tests/test_data/`
- Generated test files → `tests/test_data/`

**Moved Documentation:**
- `docs/GENERATE_CONTEXT_IMPLEMENTATION.md` → `spec/`
- `docs/GENERATE_CONTEXT_QUICK_REF.md` → `spec/`

**Rationale:**
- Test data should be in `tests/` directory
- Implementation specs belong in `spec/` directory
- Cleaner project structure
- Better separation of concerns

### Updated Tests

**New Tests Added:**
- `test_fetch_json_url()` - Test JSON URL fetching
- `TestConvertHtmlToMarkdown` class with 3 tests:
  - `test_convert_simple_html()` - Basic HTML conversion
  - `test_convert_html_removes_junk()` - Junk removal
  - `test_convert_html_with_headings()` - Heading preservation

**Total Tests:** 36 (was 32)
- Added 4 new tests for HTML conversion
- All tests passing ✓

### Documentation Updates

**README.md:**
- Updated quick usage to mention HTML conversion
- Updated links to moved files
- Added html2text to features

**docs/GENERATE_CONTEXT.md:**
- Added detailed HTML to markdown conversion section
- Updated Web URLs section with conversion details
- Added Example 3 showing HTML conversion
- Updated Requirements section
- Updated Troubleshooting section

**spec/GENERATE_CONTEXT_QUICK_REF.md:**
- Updated all file path references
- Maintained as quick reference guide

**spec/GENERATE_CONTEXT_IMPLEMENTATION.md:**
- Maintained as implementation details
- Moved to spec directory

### Dependencies

**Added:**
- `html2text >= 2024.2.26` - HTML to markdown conversion

**Existing:**
- `requests >= 2.32.3` - HTTP requests
- `ollama >= 0.4.0` - AI integration
- `python-dotenv >= 1.0.0` - Environment variables
- `pytest >= 8.0.0` - Testing

### Migration Notes

**If you have references to moved files, update them:**

Old:
```bash
examples/product_smartwatch.md
docs/GENERATE_CONTEXT_QUICK_REF.md
docs/GENERATE_CONTEXT_IMPLEMENTATION.md
```

New:
```bash
tests/test_data/product_smartwatch.md
spec/GENERATE_CONTEXT_QUICK_REF.md
spec/GENERATE_CONTEXT_IMPLEMENTATION.md
```

**For HTML URLs:**
No changes needed - HTML conversion is automatic!

### Breaking Changes

None. This version is backward compatible with v1.1.0.

### Testing

```bash
# Install new dependency
uv sync

# Run all tests
uv run pytest tests/test_generate_context.py -v

# Test HTML conversion
uv run python generate_context.py https://example.com --preview
```

## Version 1.1.0 - 2025-10-28

### Fixed Issues

#### Issue #1: Simplified Overwrite Prompt
**Previous Behavior:**
```
Overwrite? (y/n/new) [n]:
  - y = Overwrite
  - n = Cancel operation
  - new = Create new numbered file
```

**New Behavior:**
```
Overwrite? (y/n) [y]:
  - y = Overwrite (default)
  - n = Create new numbered file
```

**Rationale:**
- Simplified from 3 options to 2
- Default changed to `y` (overwrite) for common use case
- Removed "cancel" option - users can use Ctrl+C if needed
- `n` now creates numbered file instead of canceling

#### Issue #2: Changed Preview Default Behavior
**Previous Behavior:**
- Preview shown by default
- Use `--no-preview` flag to skip preview

**New Behavior:**
- No preview by default (fast mode)
- Use `--preview` flag to show preview

**Rationale:**
- Faster workflow for batch processing
- Preview is optional feature, not default
- More intuitive flag naming (positive instead of negative)

### Changes Summary

#### Script Changes (generate_context.py)
1. Modified `save_context_file()` function:
   - Changed default `preview` parameter from `True` to `False`
   - Updated overwrite prompt from `(y/n/new)` to `(y/n)`
   - Changed default response from `n` to `y`
   - Removed "cancel" logic (now `n` creates new file)

2. Modified `process_input()` function:
   - Changed default `preview` parameter from `True` to `False`

3. Modified argument parser:
   - Replaced `--no-preview` with `--preview` flag
   - Updated flag from negative to positive logic
   - Updated help examples

#### Test Changes (tests/test_generate_context.py)
1. Updated `test_save_overwrite_existing()`:
   - Changed to use single prompt return value
   - Removed preview=False, now using default

2. Updated `test_save_cancel_overwrite()`:
   - Renamed to better reflect new behavior
   - Now expects new file creation instead of cancellation
   - Verifies original file unchanged and new file created

3. Updated `test_save_create_new_file()`:
   - Updated to use single prompt return
   - Simplified test logic

All 32 tests still passing ✓

#### Documentation Changes

**README.md:**
- Updated Quick Usage examples
- Changed `--no-preview` to `--preview`
- Updated example commands

**docs/GENERATE_CONTEXT.md:**
- Updated Advanced Options section
- Updated File Overwrite Protection section
- Updated Preview Mode section
- Removed mentions of `--no-preview`
- Updated all examples and use cases

**docs/GENERATE_CONTEXT_QUICK_REF.md:**
- Updated Command Options table
- Updated Common Commands section
- Updated File Handling section
- Updated Preview Mode section
- Updated Tips & Tricks
- Updated Use Cases

### Migration Guide

If you were using the old version:

**Old Command:**
```bash
uv run python generate_context.py input.md
# (showed preview by default)

uv run python generate_context.py input.md --no-preview
# (skipped preview)
```

**New Command:**
```bash
uv run python generate_context.py input.md
# (no preview, saves directly)

uv run python generate_context.py input.md --preview
# (shows preview)
```

**Overwrite Prompt:**

Old behavior:
```
Overwrite? (y/n/new) [n]: new
# Created new file
```

New behavior:
```
Overwrite? (y/n) [y]: n
# Creates new file
```

### Testing

All tests passing:
- 32 generate_context tests ✓
- 14 existing project tests ✓
- Total: 46/46 tests passing ✓

### Backward Compatibility

⚠️ **Breaking Changes:**
- `--no-preview` flag removed (use default behavior instead)
- Default behavior changed from preview to no-preview
- Overwrite prompt changed from 3 options to 2

These are intentional UX improvements based on user feedback.

### Usage Examples

**Basic usage (no preview, saves directly):**
```bash
uv run python generate_context.py product.md
```

**With preview:**
```bash
uv run python generate_context.py product.md --preview
```

**Custom output name:**
```bash
uv run python generate_context.py product.md --output custom_name
```

**Overwrite existing file:**
```bash
uv run python generate_context.py product.md
# When prompted: y (default)
```

**Create new numbered file:**
```bash
uv run python generate_context.py product.md
# When prompted: n
# Creates: context_input_1.md
```

## Version 1.0.0 - 2025-10-28

### Initial Release

- Created `generate_context.py` script
- Support for .md, .json files, and URLs
- Comprehensive test suite (32 tests)
- Full documentation
- Example files
- Integration-ready

---

For full documentation, see:
- [docs/GENERATE_CONTEXT.md](../docs/GENERATE_CONTEXT.md)
- [spec/GENERATE_CONTEXT_QUICK_REF.md](../spec/GENERATE_CONTEXT_QUICK_REF.md)


### Fixed Issues

#### Issue #1: Simplified Overwrite Prompt
**Previous Behavior:**
```
Overwrite? (y/n/new) [n]:
  - y = Overwrite
  - n = Cancel operation
  - new = Create new numbered file
```

**New Behavior:**
```
Overwrite? (y/n) [y]:
  - y = Overwrite (default)
  - n = Create new numbered file
```

**Rationale:**
- Simplified from 3 options to 2
- Default changed to `y` (overwrite) for common use case
- Removed "cancel" option - users can use Ctrl+C if needed
- `n` now creates numbered file instead of canceling

#### Issue #2: Changed Preview Default Behavior
**Previous Behavior:**
- Preview shown by default
- Use `--no-preview` flag to skip preview

**New Behavior:**
- No preview by default (fast mode)
- Use `--preview` flag to show preview

**Rationale:**
- Faster workflow for batch processing
- Preview is optional feature, not default
- More intuitive flag naming (positive instead of negative)

### Changes Summary

#### Script Changes (generate_context.py)
1. Modified `save_context_file()` function:
   - Changed default `preview` parameter from `True` to `False`
   - Updated overwrite prompt from `(y/n/new)` to `(y/n)`
   - Changed default response from `n` to `y`
   - Removed "cancel" logic (now `n` creates new file)

2. Modified `process_input()` function:
   - Changed default `preview` parameter from `True` to `False`

3. Modified argument parser:
   - Replaced `--no-preview` with `--preview` flag
   - Updated flag from negative to positive logic
   - Updated help examples

#### Test Changes (tests/test_generate_context.py)
1. Updated `test_save_overwrite_existing()`:
   - Changed to use single prompt return value
   - Removed preview=False, now using default

2. Updated `test_save_cancel_overwrite()`:
   - Renamed to better reflect new behavior
   - Now expects new file creation instead of cancellation
   - Verifies original file unchanged and new file created

3. Updated `test_save_create_new_file()`:
   - Updated to use single prompt return
   - Simplified test logic

All 32 tests still passing ✓

#### Documentation Changes

**README.md:**
- Updated Quick Usage examples
- Changed `--no-preview` to `--preview`
- Updated example commands

**docs/GENERATE_CONTEXT.md:**
- Updated Advanced Options section
- Updated File Overwrite Protection section
- Updated Preview Mode section
- Removed mentions of `--no-preview`
- Updated all examples and use cases

**docs/GENERATE_CONTEXT_QUICK_REF.md:**
- Updated Command Options table
- Updated Common Commands section
- Updated File Handling section
- Updated Preview Mode section
- Updated Tips & Tricks
- Updated Use Cases

### Migration Guide

If you were using the old version:

**Old Command:**
```bash
uv run python generate_context.py input.md
# (showed preview by default)

uv run python generate_context.py input.md --no-preview
# (skipped preview)
```

**New Command:**
```bash
uv run python generate_context.py input.md
# (no preview, saves directly)

uv run python generate_context.py input.md --preview
# (shows preview)
```

**Overwrite Prompt:**

Old behavior:
```
Overwrite? (y/n/new) [n]: new
# Created new file
```

New behavior:
```
Overwrite? (y/n) [y]: n
# Creates new file
```

### Testing

All tests passing:
- 32 generate_context tests ✓
- 14 existing project tests ✓
- Total: 46/46 tests passing ✓

### Backward Compatibility

⚠️ **Breaking Changes:**
- `--no-preview` flag removed (use default behavior instead)
- Default behavior changed from preview to no-preview
- Overwrite prompt changed from 3 options to 2

These are intentional UX improvements based on user feedback.

### Usage Examples

**Basic usage (no preview, saves directly):**
```bash
uv run python generate_context.py product.md
```

**With preview:**
```bash
uv run python generate_context.py product.md --preview
```

**Custom output name:**
```bash
uv run python generate_context.py product.md --output custom_name
```

**Overwrite existing file:**
```bash
uv run python generate_context.py product.md
# When prompted: y (default)
```

**Create new numbered file:**
```bash
uv run python generate_context.py product.md
# When prompted: n
# Creates: context_input_1.md
```

## Version 1.0.0 - 2025-10-28

### Initial Release

- Created `generate_context.py` script
- Support for .md, .json files, and URLs
- Comprehensive test suite (32 tests)
- Full documentation
- Example files
- Integration-ready

---

For full documentation, see:
- [docs/GENERATE_CONTEXT.md](GENERATE_CONTEXT.md)
- [docs/GENERATE_CONTEXT_QUICK_REF.md](GENERATE_CONTEXT_QUICK_REF.md)
