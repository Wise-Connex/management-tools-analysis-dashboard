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
- **Database Tests**: Well-established test suite for precomputed findings
- **Single test approach**: Create test files in root directory and run directly
- **Integration testing**: Run application and verify functionality in browser

**Database Testing:**
```bash
# Test precomputed findings database implementation
cd /Users/Dimar/Documents/python-code/MTSA/tools-dashboard
python3 database_implementation/test_database.py

# Expected output: All tests PASSED with performance metrics
# Current status: 5/5 tests passing, 1.59ms average query time
```

**Database Test Coverage:**
- ✅ Database creation and schema validation
- ✅ Hash generation consistency testing
- ✅ CRUD operations verification
- ✅ Performance benchmarking (<100ms target)
- ✅ Job queue system validation

**Other Test Patterns:**
```bash
# Run specific integration tests
python3 comprehensive_key_findings_test.py          # Full integration test
python3 populate_database_test.py                   # Database population test
python3 test_ai_integration.py                      # AI service integration
```

### Code Quality
- **Linting**: Consider adding `ruff` or `black` for code formatting
- **Type checking**: Consider adding `mypy` for static type checking
- **Current practice**: Type hints are widely used with `from typing import` patterns

## Code Style Guidelines

### Import Organization
- Standard library imports first, then third-party, then local imports
- Group related imports together
- Use `from typing import` for type hints
- Add parent directory to sys.path when importing across directories
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

**Actual patterns from codebase:**
```python
# From app.py - grouped by functionality
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, List, Any

# Add path for database imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import tool_file_dic, get_tool_options, translate_tool_key, get_tool_name
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

### Precomputed Findings Database (Key Findings Cache)
- **Purpose**: Pre-populated SQLite database for 1,302 tool-source-language combinations
- **Location**: `/data/precomputed_findings.db` 
- **Manager**: `PrecomputedFindingsDBManager` from `database_implementation/precomputed_findings_db.py`
- **Performance**: Sub-2ms lookup time (target <100ms)
- **Hash Generation**: Consistent, reproducible combination hashing system

**Key Usage Patterns:**
```python
# Get database manager
from database_implementation.precomputed_findings_db import get_precomputed_db_manager
db_manager = get_precomputed_db_manager()

# Generate combination hash
hash_value = db_manager.generate_combination_hash(
    tool_name="Benchmarking", 
    selected_sources=["Google Trends", "Bain Usability"], 
    language="es"
)

# Store analysis result
db_manager.store_precomputed_analysis(
    combination_hash=hash_value,
    tool_name="Benchmarking",
    selected_sources=["Google Trends", "Bain Usability"],
    language="es",
    analysis_data={"executive_summary": "...", "confidence_score": 0.85}
)

# Retrieve cached analysis
cached_result = db_manager.get_combination_by_hash(hash_value)
```

**Integration Points:**
- Replace live AI queries with database lookups in `key_findings_service.py`
- Use hash-based retrieval for instant analysis results
- Fallback to live analysis for missing combinations
- Job queue system for manual regeneration requests

**Testing:**
```bash
# Run database tests
cd /Users/Dimar/Documents/python-code/MTSA/tools-dashboard
python3 database_implementation/test_database.py
```

**Database Schema:**
- `precomputed_findings` - Main analysis results storage
- `management_tools` - Tool reference data (21 tools)
- `data_sources` - Source reference data (5 sources)
- `computation_jobs` - Precomputation pipeline tracking
- `usage_analytics` - Performance and access monitoring
- `video_assets` - Future video integration support

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

### Dashboard App Structure
```
dashboard_app/
├── app.py                    # Main Dash app entry point
├── layout.py                 # App layout definitions
├── tools.py                  # Tool data and mappings
├── translations.py           # I18N support
├── utils.py                  # Utility functions and caching
├── callbacks/                # Callback modules
│   ├── main_callbacks.py     # Primary content callbacks
│   ├── graph_callbacks.py    # Visualization callbacks
│   ├── kf_callbacks.py       # Key findings callbacks
│   └── ui_callbacks.py       # UI interaction callbacks
├── key_findings/             # AI analysis components
│   ├── key_findings_service.py      # Main analysis service
│   ├── database_manager.py          # Precomputed findings DB
│   ├── unified_ai_service.py        # AI service integration
│   └── ...
└── assets/                   # Static files (logos, icons, styles)
```

### Database Implementation Files
- `database_implementation/schema.sql` - Precomputed findings database schema
- `database_implementation/precomputed_findings_db.py` - Database manager class
- `database_implementation/test_database.py` - Database test suite
- `data/precomputed_findings.db` - SQLite database file (auto-created)
- `IMPLEMENTATION_PLAN.md` - Database implementation roadmap and progress

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

### API Key Management
- **Groq API Key**: Required for AI analysis, loaded via `os.getenv("GROQ_API_KEY")`
- **Environment Setup**: Copy `.env.example` to `.env` and add API keys
- **Security**: Never commit `.env` files to version control
- **Fallback**: System works in database-only mode without API key
- **Loading**: Automatic via `python-dotenv` in app startup
- **Verification**: Use `python3 -c "import os; print('GROQ_API_KEY loaded:', 'GROQ_API_KEY' in os.environ)"`

### Database-First Architecture
- **Implementation**: Precomputed findings database with 1,302 combinations
- **Performance**: Sub-2ms query time vs 5-15s live AI generation
- **Hash System**: Consistent hash generation for tool-source-language combinations
- **Fallback**: Live AI generation only for missing combinations
- **Integration**: `database_first_service.py` handles database-first logic
- **Testing**: All combinations verified with comprehensive test suite

### Documentation Maintenance
- **Keep README.md current** when making changes to:
  - Installation procedures or dependencies
  - Configuration options or environment variables
  - API interfaces or function signatures
  - Project structure or file organization
  - Docker deployment or build processes
- Update screenshots and examples when UI changes
- Maintain version compatibility information
- Update troubleshooting section for common issues

### Development References
- **IMPLEMENTATION_PLAN.md** - Comprehensive database implementation roadmap with:
  - 5-phase implementation timeline
  - Task tracking checklists
  - Success criteria and metrics
  - Current implementation progress
  - Technical specifications and examples

**For Database Development:**
- Use `IMPLEMENTATION_PLAN.md` to track implementation phases
- Reference test results and performance metrics
- Follow established patterns from Phase 1 implementation
- Update progress tracking as work advances through phases

**Current Status (Phase 5 Complete):**
- ✅ Database foundation implemented and tested
- ✅ Performance targets exceeded (1.59ms vs 100ms target)
- ✅ Key Findings Modal Architecture refactored with new services
- ✅ Full test suite passing with comprehensive validation

### Key Findings Modal Architecture (NEW - 2025-12-10)

**New Service-Oriented Architecture:**
- **KeyFindingsRetrievalService**: Dedicated database retrieval (1.59ms avg)
- **KeyFindingsContentParser**: Robust content transformation (0.56ms avg)
- **RefactoredModalCallback**: Clean orchestration layer

**Architecture Benefits:**
- **100% Database-Driven**: No live AI calls, sub-2ms performance
- **Flawless Formatting**: Zero parsing artifacts, perfect content preservation
- **Perfect Section Structure**: 6 sections (single-source) / 7 sections (multi-source)
- **Comprehensive Error Handling**: Graceful degradation with clear messages
- **Performance Monitoring**: Built-in metrics and validation

**Implementation Guidelines:**
```python
# New workflow - clean and simple
def handle_key_findings_modal(tool_name, sources, language):
    # Step 1: Retrieve from database
    retrieval_result = retrieval_service.retrieve_precomputed_findings(
        tool_name=tool_name,
        selected_sources=sources,
        language=language
    )
    
    if retrieval_result["success"]:
        # Step 2: Parse content
        parse_result = content_parser.parse_modal_content(
            retrieval_result["data"],
            language
        )
        
        if parse_result["success"]:
            # Step 3: Create modal content
            return create_modal_content_from_parsed(parse_result["data"], language)
    
    # Handle errors gracefully
    return create_error_modal_content(retrieval_result.get("error"), language)
```

**Performance Targets:**
- Database queries: <100ms (achieved: 1.59ms - 61x better)
- Content parsing: <10ms (achieved: 0.56ms - 18x better)
- Total response time: <200ms (achieved: <2.2ms)
- Zero parsing errors: 100% formatting preservation

**Testing Requirements:**
- Unit tests for both services (95%+ coverage)
- Integration tests for complete workflow
- Performance benchmarks under load
- Content validation and formatting preservation
- Error handling and edge case coverage

**Migration Path:**
1. Replace complex callback logic with service calls
2. Remove embedded parsing functions
3. Use dedicated services for retrieval and parsing
4. Maintain backward compatibility during transition
5. Monitor performance metrics post-deployment

### Precomputation Pipeline
- **Pipeline**: `database_implementation/phase3_precomputation_pipeline.py`
- **Purpose**: Automated generation of precomputed findings for all tool-source-language combinations
- **Coverage**: 1,302 unique combinations (21 tools × 5 sources × multiple languages)
- **Job Tracking**: Computation jobs stored in database with status monitoring
- **Integration**: Seamlessly integrates with AI services for batch processing

**Pipeline Usage:**
```python
# Run precomputation pipeline
python3 database_implementation/phase3_precomputation_pipeline.py

# Monitor progress via computation_jobs table
# Analyze usage via usage_analytics table
```