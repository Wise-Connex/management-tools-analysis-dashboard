# Project Analysis: Management Tools Analysis Dashboard

## Overview
The Management Tools Analysis Dashboard is a Python-based Dash application designed to analyze management tools data from multiple sources (Google Trends, Google Books, Bain Survey, Crossref, Bain Satisfaction). It provides interactive visualizations, statistical analysis, and AI-powered insights.

## Architecture
The project follows a modular architecture:

### 1. Core Application (`dashboard_app/`)
- **`app.py`**: The main entry point. Initializes the Dash app, defines the layout, and handles callbacks. It integrates various components like the database manager and key findings service.
- **`config.py`**: Centralized configuration management. Loads settings from JSON files (`config/`) and environment variables.
- **`database.py`**: Manages SQLite database operations, including connection pooling, schema creation, and data retrieval.
- **`tools.py`**: Defines the dictionary of management tools and their associated data files. Handles tool selection logic.
- **`translations.py`**: Provides bilingual support (Spanish/English) for the UI.

### 2. Data Layer
- **SQLite Database**: The primary data store (`data.db`, `precomputed_findings.db`).
- **Database-First Strategy**: A recent major improvement (Phase 4) that prioritizes fetching precomputed AI analysis results from the database to reduce latency and cost.
- **Data Sources**:
    - Google Trends (GT)
    - Google Books (GB)
    - Bain Usage (BU)
    - Crossref (CR)
    - Bain Satisfaction (BS)

### 3. AI & Key Findings (`dashboard_app/key_findings/`)
- **`key_findings_service.py`**: Orchestrates the generation of key findings.
- **`database_first_service.py`**: Implements the logic to check the database for existing analysis before calling the AI service.
- **`ai_service.py`**: Handles interactions with AI providers (Groq, OpenRouter).
- **`prompt_engineer.py`**: Manages prompt generation for AI analysis.

### 4. Deployment
- **Docker**: The project is containerized for easy deployment.
    - `Dockerfile`: Defines the image.
    - `docker-compose.yml`: Orchestrates services (dashboard, monitoring, nginx).
    - `DOCKER_DEPLOYMENT.md`: Detailed guide for Docker deployment.

## Technical Stack
- **Backend/Frontend**: Python, Dash, Plotly, Flask.
- **Data Manipulation**: Pandas, NumPy.
- **Database**: SQLite.
- **AI Integration**: Groq, OpenRouter APIs.
- **Package Management**: `uv` (recommended) or `pip`.
- **Containerization**: Docker.

## Key Features
- **Interactive Visualizations**: Time series, 3D plots, heatmaps.
- **Statistical Analysis**: PCA, regression, Fourier analysis.
- **Bilingual Support**: Full Spanish and English interface.
- **AI Insights**: Automated generation of executive summaries and findings.
- **Performance**: Optimized with database caching and precomputation.

## Recent Improvements (Database-First Strategy)
- Transitioned from live AI queries to a precomputed database approach.
- **Performance**: Sub-2ms response times for cached queries (vs. 6+ seconds for live AI).
- **Cost**: Significant reduction in API costs.
- **Reliability**: Fallback to live AI ensures availability even if the cache misses.

## Next Steps (Reference)
- **Video Integration (Phase 5)**: Adding support for video explanations linked to analysis.
- **CI/CD**: Implementing automated testing and deployment pipelines.
- **Monitoring**: Enhancing production monitoring and alerting.

## Conclusion
The project is a mature, well-structured analytical tool with advanced features. The recent shift to a database-first strategy for AI insights significantly enhances user experience and performance. The codebase is clean, modular, and well-documented.

## Visual Documentation

### System Architecture
```mermaid
graph TD
    User[User] --> UI[Dash UI]
    UI --> App[app.py]
    
    subgraph "Core Application"
        App --> Config[config.py]
        App --> Tools[tools.py]
        App --> Trans[translations.py]
        App --> DBMan[database.py]
    end
    
    subgraph "Data Layer"
        DBMan --> MainDB[(data.db)]
        KF_Service --> KF_DB[(key_findings.db)]
        KF_Service --> PrecompDB[(precomputed_findings.db)]
    end
    
    subgraph "AI & Analysis Services"
        App --> KF_Service[KeyFindingsService]
        KF_Service --> DataAgg[DataAggregator]
        KF_Service --> PromptEng[PromptEngineer]
        KF_Service --> AIService[UnifiedAIService]
        AIService --> ExtAI[External AI APIs]
    end
    
    DataAgg --> DBMan
```

### Key Findings Generation Process
```mermaid
sequenceDiagram
    participant User
    participant App
    participant KF as KeyFindingsService
    participant Cache as Cache (SQLite)
    participant Precomp as Precomputed DB
    participant AI as AI Service
    
    User->>App: Request Key Findings
    App->>KF: generate_key_findings()
    KF->>KF: Generate Scenario Hash
    
    KF->>Cache: Check Cache
    alt Cache Hit
        Cache-->>KF: Return Cached Report
        KF-->>App: Return Findings
        App-->>User: Display Results (⚡ Cached)
    else Cache Miss
        KF->>Precomp: Check Precomputed DB
        alt Precomputed Found
            Precomp-->>KF: Return Precomputed Analysis
            KF-->>App: Return Findings
            App-->>User: Display Results (⚡ Database)
        else Precomputed Miss
            KF->>AI: Generate Live Analysis
            AI-->>KF: Return New Analysis
            KF->>Cache: Store in Cache
            KF-->>App: Return Findings
            App-->>User: Display Results (✨ Live AI)
        end
    end
```

### Database Schema (Key Findings)
```mermaid
erDiagram
    management_tools ||--o{ precomputed_findings : "has analysis"
    management_tools ||--o{ computation_jobs : "has jobs"
    
    management_tools {
        int id PK
        string name
        string display_name_es
        string display_name_en
        json keywords
        json files_mapping
    }
    
    precomputed_findings ||--o{ usage_analytics : "tracked by"
    precomputed_findings ||--o{ video_assets : "has video"
    
    precomputed_findings {
        int id PK
        string combination_hash UK
        int tool_id FK
        string sources_text
        string language
        text executive_summary
        text principal_findings
        text pca_analysis
        float confidence_score
        string model_used
    }
    
    data_sources {
        int id PK
        string name
        string source_type
    }
    
    computation_jobs {
        int id PK
        int tool_id FK
        string status
        int priority
        datetime created_at
    }
    
    usage_analytics {
        int id PK
        string combination_hash FK
        int response_time_ms
        boolean found_in_cache
    }
    
    video_assets {
        int id PK
        string combination_hash FK
        string file_path
        boolean active
    }
```
