# AGENTS.md - Management Tools Analysis Dashboard

This file contains guidelines for agentic coding agents working on this Python Dash dashboard project.

## Build/Lint/Test Commands

### Environment Setup
```bash
cd dashboard_app
uv sync  # Install dependencies
```

### Running the Application
```bash
cd dashboard_app
uv run python app.py                    # Main application
# OR
./run_dashboard.sh                         # Convenience script
```

### Testing
- **No formal test suite currently exists** - tests should be added manually
- For testing changes: run the application and verify functionality in browser
- Single test approach: Create test files in `tests/` directory and run with `python -m pytest tests/`

### Code Quality
- **No linting configured** - consider adding `ruff` or `black` for code formatting
- **No type checking configured** - consider adding `mypy` for static type checking

## Code Style Guidelines

### Import Organization
- Standard library imports first, then third-party, then local imports
- Group related imports together
- Use `from typing import` for type hints
```python
import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import dash
from dash import html, dcc

from config import get_config
from database import get_database_manager
```

### Naming Conventions
- **Variables**: `snake_case` (e.g., `selected_sources`, `data_manager`)
- **Functions**: `snake_case` (e.g., `get_data_for_keyword()`, `update_language_store()`)
- **Classes**: `PascalCase` (e.g., `DatabaseManager`, `KeyFindingsDBManager`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DISPLAY_NAMES`, `TRANSLATIONS`)
- **Private methods**: prefix with underscore (e.g., `_load_config()`, `_get_schema_sql()`)

### Type Hints
- Use type hints for all function signatures and class attributes
- Import from `typing` module: `Dict`, `List`, `Any`, `Optional`, `Tuple`
- Use `Path` from `pathlib` for file paths
```python
def get_data_for_keyword(self, keyword: str, sources: List[int]) -> Tuple[Dict[int, pd.DataFrame], List[int]]:
    """Retrieve data for keyword and sources."""
```

### Error Handling
- Use context managers for database connections
- Log errors with appropriate level using `logging` module
- Return empty/default values when operations fail gracefully
- Include try/except blocks for external API calls and file operations

### Documentation
- Use docstrings for all classes and public methods
- Follow Google-style docstring format
- Include Args, Returns, and Raises sections where applicable
```python
def create_schema(self):
    """
    Create database schema with all required tables and indexes.
    
    This includes data tables for each source and metadata table.
    """
```

### Database Patterns
- Use singleton pattern for database managers (`get_database_manager()`)
- Use context managers for connections (`with self.get_connection():`)
- Parameterize queries to prevent SQL injection
- Use WAL mode and connection pooling for performance

### Dash/React Patterns
- Use `dcc.Store()` for sharing data between callbacks
- Implement proper callback chains with `prevent_initial_call=True`
- Use clientside callbacks for JavaScript functionality
- Handle loading states with `dcc.Loading()` components
- Use `dash_bootstrap_components` for consistent styling

### Configuration Management
- Use centralized `Config` class from `config.py`
- Support environment variable overrides with `DASHBOARD_` prefix
- Store configuration in JSON files under `config/` directory
- Use property accessors for common configuration values

### File Organization
- `app.py` - Main Dash application and callbacks
- `database.py` - Database operations and schema
- `config.py` - Configuration management
- `tools.py` - Tool definitions and mappings
- `translations.py` - Internationalization support
- `key_findings/` - AI analysis modules
- `assets/` - Static assets (images, icons)

### Performance Considerations
- Implement caching for expensive operations (`_processed_data_cache`)
- Use database indexes for query optimization
- Batch database operations where possible
- Use async patterns for AI service calls with proper error handling

### Security
- Never commit API keys or sensitive configuration
- Use environment variables for secrets
- Validate user inputs in callbacks
- Implement proper CORS headers for production deployment