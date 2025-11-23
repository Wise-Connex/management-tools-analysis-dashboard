# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a Python Dash-based Management Tools Analysis Dashboard for doctoral research on management tools trends. It provides interactive data visualization, AI-powered insights, and comprehensive statistical analysis across multiple data sources (Google Trends, Google Books, Bain Survey, Crossref).

## Common Development Commands

### Environment Setup
```bash
cd dashboard_app
uv sync  # Install dependencies with UV package manager
```

### Running the Application
```bash
# From dashboard_app directory
uv run python app.py

# Or from project root
./run_dashboard.sh
```

### Database Testing
```bash
# Test precomputed findings database performance
python3 database_implementation/test_database.py
# Expected: 5/5 tests passing, <100ms query performance
```

## High-Level Architecture

### Core Components
- **Dash Application** (`dashboard_app/app.py`): Main web interface with 339KB+ of callback logic
- **Database Layer** (`database.py`): SQLite with singleton pattern, connection pooling, and WAL mode
- **Configuration** (`config.py`): Centralized JSON-based config with environment overrides (DASHBOARD_ prefix)
- **AI Services** (`key_findings/`): Multi-provider integration (Groq, OpenRouter) with precomputed findings cache
- **Translation System** (`translations.py`): Bilingual Spanish/English support throughout

### Data Flow Architecture
1. **Data Sources** → CSV files in `dbase/` → SQLite database via `DatabaseManager`
2. **User Requests** → Dash callbacks → Data retrieval → Statistical analysis → Visualization
3. **AI Insights** → Data aggregation → Multi-provider AI calls → Cached findings → UI display

### Key Design Patterns
- **Singleton Pattern**: Database managers (`get_database_manager()`, `get_config()`)
- **Context Managers**: Database connections (`with self.get_connection():`)
- **Callback Chains**: Dash interactions with `prevent_initial_call=True`
- **Hash-based Caching**: Precomputed findings use combination hashing for instant lookup

### Performance Optimizations
- Precomputed findings database: 1,302 tool-source-language combinations, <2ms lookup
- Database indexes and connection pooling
- Data caching with `_processed_data_cache`
- Async AI service calls with proper error handling

## Critical Implementation Details

### Database Schema
- Main tables: `google_trends`, `google_books`, `crossref`, `bain_usability`, `bain_satisfaction`
- Precomputed findings: Separate SQLite DB with hash-based retrieval
- Numeric source mapping: 1=Google Trends, 2=Google Books, 3=Bain Usability, 4=Crossref, 5=Bain Satisfaction

### AI Integration Points
- `key_findings_service.py`: Main orchestrator with fallback logic
- `unified_ai_service.py`: Multi-provider abstraction
- `prompt_engineer.py`: Doctoral-level analysis prompts
- Precomputed database integration for performance

### Configuration Priority
1. Default JSON values (`config/*.json`)
2. Environment variables (DASHBOARD_ prefix)
3. Runtime configuration updates

### Error Handling Requirements
- Graceful degradation when AI services unavailable
- Database connection failures should return empty/default data
- User input validation in all Dash callbacks
- Comprehensive logging with appropriate levels

## Development Guidelines

### Code Style (from AGENTS.md)
- Follow PEP 8, use type hints for all functions
- Import order: standard library, third-party, local imports
- Naming: snake_case (functions/variables), PascalCase (classes), UPPER_SNAKE_CASE (constants)
- Private methods prefixed with underscore

### Testing Approach
- No formal test suite exists - manual testing required
- Database tests: Run `test_database.py` for performance validation
- UI testing: Verify all analysis tabs work with different tool combinations
- AI testing: Check fallback behavior when API keys missing

### Security Considerations
- Never commit API keys (use .env file)
- Validate all user inputs in callbacks
- Use parameterized database queries
- Environment variables for sensitive configuration

### Common Issues and Solutions
- **Port conflicts**: Kill process on 8050 or use DASHBOARD_PORT override
- **Database permissions**: Ensure write access to dashboard_app/data directory
- **Missing dependencies**: Use `uv sync` not pip for consistent environment
- **AI service failures**: Check GROQ_API_KEY and OPENROUTER_API_KEY environment variables