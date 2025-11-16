-- Key Findings Database Schema
-- Pre-populated SQLite database for Management Tools Dashboard
-- Scale: 21 tools × 5 sources × 2 languages = 1,302 combinations

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Main findings table (stores all pre-computed analyses)
CREATE TABLE IF NOT EXISTS precomputed_findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Combination Identification (Primary lookup)
    combination_hash TEXT UNIQUE NOT NULL,           -- Hash: tool_sources_language
    tool_id INTEGER NOT NULL,
    tool_name TEXT NOT NULL,                        -- Spanish name (from tools.py)
    tool_display_name TEXT NOT NULL,                -- User-facing name
    
    -- Source Selection (flexible storage)
    sources_text TEXT NOT NULL,                     -- "Google Trends, Bain Usability"
    sources_ids TEXT NOT NULL,                      -- JSON: [1,3,5]
    sources_bitmask TEXT NOT NULL,                  -- "10101" (5-bit binary)
    sources_count INTEGER NOT NULL,
    
    -- Language & Time Context
    language TEXT NOT NULL,                         -- 'es' or 'en'
    date_range_start TEXT,
    date_range_end TEXT,
    
    -- Analysis Content (Markdown formatted)
    executive_summary TEXT NOT NULL,                -- Main findings summary
    principal_findings TEXT,                        -- Multi-source PCA results
    temporal_analysis TEXT,                         -- Single source temporal analysis
    seasonal_analysis TEXT,                         -- Single source seasonal patterns
    fourier_analysis TEXT,                          -- Single source Fourier analysis
    pca_analysis TEXT,                             -- Multi-source component analysis
    heatmap_analysis TEXT,                         -- Data distribution analysis
    
    -- Analysis Metadata
    analysis_type TEXT NOT NULL,                   -- 'single_source' | 'multi_source'
    data_points_analyzed INTEGER,
    confidence_score REAL,                         -- AI confidence in results
    model_used TEXT,                                -- Which AI model generated this
    
    -- Video Integration (Future - Phase 5)
    video_info TEXT,                              -- JSON: {path, duration, format, etc.}
    video_file_path TEXT,                         -- Direct file path reference
    video_available BOOLEAN DEFAULT 0,           -- Quick boolean check for UI
    
    -- System Fields
    version INTEGER DEFAULT 1,                    -- For future updates
    is_active BOOLEAN DEFAULT 1,                  -- Soft delete flag
    computation_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Usage Analytics
    access_count INTEGER DEFAULT 0,
    last_accessed DATETIME,
    original_computation_time_ms INTEGER,         -- How long original AI took
    cache_hit_count INTEGER DEFAULT 0,
    
    -- Error Handling
    generation_error TEXT,                        -- If AI generation failed
    retry_count INTEGER DEFAULT 0,
    
    FOREIGN KEY (tool_id) REFERENCES management_tools(id)
);

-- Reference table: Management tools (from tools.py)
CREATE TABLE IF NOT EXISTS management_tools (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,                    -- Spanish name (key)
    display_name_es TEXT NOT NULL,                -- Spanish display name
    display_name_en TEXT,                         -- English display name
    keywords TEXT,                               -- JSON array of keywords
    files_mapping TEXT,                          -- JSON: file paths per source
    tool_order INTEGER,                          -- Display order in UI
    active BOOLEAN DEFAULT 1,                    -- Tool availability
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Reference table: Data sources
CREATE TABLE IF NOT EXISTS data_sources (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,                   -- Internal identifier
    display_name TEXT NOT NULL,                  -- User-facing name
    source_type TEXT NOT NULL,                   -- trends, books, usage, academic, satisfaction
    color_code TEXT,                            -- Visualization color
    file_suffix TEXT,                           -- File extension pattern
    active BOOLEAN DEFAULT 1,                   -- Source availability
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Precomputation job tracking
CREATE TABLE IF NOT EXISTS computation_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_id INTEGER NOT NULL,
    sources_bitmask TEXT NOT NULL,              -- 5-bit binary: "10101"
    language TEXT NOT NULL,                     -- 'es' or 'en'
    status TEXT DEFAULT 'pending',             -- pending, running, completed, failed, retry
    priority INTEGER DEFAULT 0,                -- Higher = more important (0-100)
    started_at DATETIME,
    completed_at DATETIME,
    estimated_completion DATETIME,             -- For progress estimation
    error_message TEXT,                        -- Error details if failed
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    progress_percent INTEGER DEFAULT 0,        -- 0-100
    progress_details TEXT,                     -- JSON: detailed progress info
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (tool_id) REFERENCES management_tools(id),
    UNIQUE(tool_id, sources_bitmask, language)
);

-- Usage analytics and performance monitoring
CREATE TABLE IF NOT EXISTS usage_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    combination_hash TEXT NOT NULL,
    query_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    response_time_ms INTEGER,
    found_in_cache BOOLEAN DEFAULT 1,
    language_requested TEXT,
    user_session TEXT,                         -- Session tracking
    user_agent TEXT,                          -- Browser/client info
    ip_address TEXT,                          -- For usage patterns
    
    FOREIGN KEY (combination_hash) REFERENCES precomputed_findings(combination_hash)
);

-- Video assets (for Phase 5)
CREATE TABLE IF NOT EXISTS video_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    combination_hash TEXT NOT NULL,           -- Links to analysis
    file_path TEXT NOT NULL,                  -- Relative path to video file
    file_name TEXT NOT NULL,                  -- Original filename
    file_size_bytes INTEGER,                  -- File size in bytes
    duration_seconds INTEGER,                 -- Video duration
    video_metadata TEXT,                     -- JSON: resolution, format, etc.
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT 1,
    
    FOREIGN KEY (combination_hash) REFERENCES precomputed_findings(combination_hash),
    UNIQUE(combination_hash, file_path)
);

-- System configuration
CREATE TABLE IF NOT EXISTS system_config (
    id INTEGER PRIMARY KEY,
    config_key TEXT UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    description TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Performance Indexes

-- Primary lookup indexes
CREATE INDEX IF NOT EXISTS idx_findings_lookup ON precomputed_findings(tool_id, sources_text, language);
CREATE INDEX IF NOT EXISTS idx_findings_hash ON precomputed_findings(combination_hash);
CREATE INDEX IF NOT EXISTS idx_findings_active ON precomputed_findings(is_active, language);

-- Job queue indexes
CREATE INDEX IF NOT EXISTS idx_jobs_status ON computation_jobs(status, priority, created_at);
CREATE INDEX IF NOT EXISTS idx_jobs_pending ON computation_jobs(status) WHERE status = 'pending';

-- Analytics indexes
CREATE INDEX IF NOT EXISTS idx_analytics_performance ON usage_analytics(query_timestamp, response_time_ms);
CREATE INDEX IF NOT EXISTS idx_analytics_usage ON usage_analytics(combination_hash, query_timestamp);

-- Video indexes
CREATE INDEX IF NOT EXISTS idx_videos_available ON video_assets(combination_hash, active);

-- Foreign key indexes
CREATE INDEX IF NOT EXISTS idx_findings_tool ON precomputed_findings(tool_id);
CREATE INDEX IF NOT EXISTS idx_jobs_tool ON computation_jobs(tool_id);

-- SQLite Configuration (applied separately in code)
-- PRAGMA journal_mode=WAL;      -- Write-Ahead Logging for better concurrency
-- PRAGMA synchronous=NORMAL;    -- Balance between performance and safety
-- PRAGMA cache_size=-64000;     -- 64MB cache
-- PRAGMA temp_store=MEMORY;     -- Store temp tables in memory