-- New Key Findings Database Schema
-- Designed to properly handle both single-source and multi-source analysis

-- Drop existing table (for migration)
-- DROP TABLE IF EXISTS key_findings_reports;

-- Create new improved schema
CREATE TABLE key_findings_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_hash TEXT UNIQUE NOT NULL,
    tool_name TEXT NOT NULL,
    selected_sources TEXT NOT NULL,  -- JSON array of source IDs
    source_display_names TEXT,       -- JSON array of display names
    date_range_start TEXT,
    date_range_end TEXT,
    language TEXT DEFAULT 'es',

    -- Core Content Fields (Always Present)
    executive_summary TEXT NOT NULL,
    principal_findings TEXT NOT NULL,  -- Main narrative findings
    strategic_synthesis TEXT,
    conclusions TEXT,

    -- Multi-Source Specific Fields
    heatmap_analysis TEXT,              -- Correlation analysis for multi-source
    pca_analysis TEXT,                  -- PCA analysis for multi-source

    -- Individual Analysis Fields (Available for both, but usage varies)
    temporal_analysis TEXT,             -- Time series analysis
    seasonal_analysis TEXT,             -- Seasonal patterns
    fourier_analysis TEXT,              -- Spectral/frequency analysis

    -- Analysis Type Classification
    analysis_type TEXT NOT NULL,        -- 'single_source' or 'multi_source'
    sources_count INTEGER NOT NULL,
    analysis_depth TEXT,                -- 'basic', 'comprehensive', 'advanced'

    -- Technical Metadata
    model_used TEXT NOT NULL,
    api_latency_ms INTEGER NOT NULL,
    confidence_score REAL,
    data_points_analyzed INTEGER NOT NULL,

    -- Cache Management
    generation_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cache_version TEXT DEFAULT '2.0',
    access_count INTEGER DEFAULT 0,
    last_accessed DATETIME,

    -- User Interaction
    user_rating INTEGER,                -- 1-5 stars
    user_feedback TEXT,

    -- Content Validation
    content_validation_status TEXT DEFAULT 'valid',  -- 'valid', 'partial', 'invalid'
    validation_errors TEXT              -- JSON array of validation issues
);

-- Create indexes for performance
CREATE INDEX idx_reports_scenario_hash ON key_findings_reports(scenario_hash);
CREATE INDEX idx_reports_tool_name ON key_findings_reports(tool_name);
CREATE INDEX idx_reports_analysis_type ON key_findings_reports(analysis_type);
CREATE INDEX idx_reports_generation_timestamp ON key_findings_reports(generation_timestamp);
CREATE INDEX idx_reports_language ON key_findings_reports(language);

-- Content validation view
CREATE VIEW content_validation_summary AS
SELECT
    tool_name,
    analysis_type,
    language,
    COUNT(*) as total_reports,
    SUM(CASE WHEN content_validation_status = 'valid' THEN 1 ELSE 0 END) as valid_reports,
    SUM(CASE WHEN content_validation_status = 'partial' THEN 1 ELSE 0 END) as partial_reports,
    SUM(CASE WHEN content_validation_status = 'invalid' THEN 1 ELSE 0 END) as invalid_reports,
    AVG(LENGTH(executive_summary)) as avg_exec_summary_length,
    AVG(LENGTH(principal_findings)) as avg_principal_length,
    AVG(data_points_analyzed) as avg_data_points
FROM key_findings_reports
GROUP BY tool_name, analysis_type, language;

-- Usage analytics view
CREATE VIEW usage_analytics AS
SELECT
    DATE(generation_timestamp) as date,
    analysis_type,
    COUNT(*) as reports_generated,
    AVG(access_count) as avg_access_count,
    SUM(CASE WHEN user_rating IS NOT NULL THEN 1 ELSE 0 END) as rated_reports,
    AVG(user_rating) as avg_rating
FROM key_findings_reports
GROUP BY DATE(generation_timestamp), analysis_type
ORDER BY date DESC;

-- Content quality metrics
CREATE VIEW content_quality_metrics AS
SELECT
    id,
    tool_name,
    analysis_type,
    language,

    -- Content completeness scores (0-100)
    CASE
        WHEN LENGTH(executive_summary) > 100 THEN 25
        WHEN LENGTH(executive_summary) > 50 THEN 15
        ELSE 0
    END as exec_summary_score,

    CASE
        WHEN LENGTH(principal_findings) > 1000 THEN 50
        WHEN LENGTH(principal_findings) > 500 THEN 35
        WHEN LENGTH(principal_findings) > 200 THEN 20
        ELSE 0
    END as principal_score,

    CASE
        WHEN analysis_type = 'multi_source' THEN
            CASE
                WHEN LENGTH(heatmap_analysis) > 500 AND LENGTH(pca_analysis) > 500 THEN 25
                WHEN LENGTH(heatmap_analysis) > 200 OR LENGTH(pca_analysis) > 200 THEN 15
                ELSE 0
            END
        WHEN analysis_type = 'single_source' THEN
            CASE
                WHEN LENGTH(temporal_analysis) = 0 AND LENGTH(pca_analysis) = 0 AND LENGTH(heatmap_analysis) = 0 THEN 25
                ELSE 0
            END
        ELSE 0
    END as analysis_specific_score,

    -- Data quality indicators
    CASE WHEN data_points_analyzed >= 100 THEN 10 ELSE 0 END as data_points_score,
    CASE WHEN confidence_score >= 0.8 THEN 10 ELSE 0 END as confidence_score,
    CASE WHEN model_used != 'unknown' THEN 5 ELSE 0 END as model_score
FROM key_findings_reports;

-- Migration helper function (conceptual - would need implementation)
-- This would help migrate from old schema to new schema
/*
CREATE FUNCTION migrate_from_old_schema()
RETURNS VOID AS $$
BEGIN
    -- Copy existing data with proper field mapping
    INSERT INTO key_findings_reports (
        scenario_hash, tool_name, selected_sources, date_range_start, date_range_end,
        language, executive_summary, principal_findings, pca_insights, model_used,
        api_latency_ms, confidence_score, generation_timestamp, data_points_analyzed,
        sources_count, analysis_depth, analysis_type
    )
    SELECT
        scenario_hash, tool_name, selected_sources, date_range_start, date_range_end,
        language, executive_summary,
        CASE
            WHEN LENGTH(principal_findings) > 10 THEN principal_findings
            ELSE temporal_analysis || '\n\n' || seasonal_analysis || '\n\n' || fourier_analysis
        END as principal_findings,
        pca_insights, model_used, api_latency_ms, confidence_score, generation_timestamp,
        data_points_analyzed, sources_count, analysis_depth,
        CASE WHEN sources_count = 1 THEN 'single_source' ELSE 'multi_source' END as analysis_type
    FROM old_key_findings_reports;
END;
$$ LANGUAGE plpgsql;
*/

-- Sample queries for the new schema:

-- Get single-source reports with complete content
SELECT tool_name, language, executive_summary, principal_findings,
       model_used, data_points_analyzed, generation_timestamp
FROM key_findings_reports
WHERE analysis_type = 'single_source'
  AND content_validation_status = 'valid'
ORDER BY generation_timestamp DESC;

-- Get multi-source reports with heatmap and PCA analysis
SELECT tool_name, language, executive_summary, principal_findings,
       heatmap_analysis, pca_analysis, model_used, data_points_analyzed
FROM key_findings_reports
WHERE analysis_type = 'multi_source'
  AND content_validation_status = 'valid'
ORDER BY generation_timestamp DESC;

-- Find reports with incomplete content
SELECT id, tool_name, analysis_type, language,
       CASE WHEN LENGTH(executive_summary) < 50 THEN 'Missing Executive Summary' END as issue,
       CASE WHEN LENGTH(principal_findings) < 200 THEN 'Short Principal Findings' END as issue2,
       CASE WHEN analysis_type = 'multi_source' AND (LENGTH(heatmap_analysis) < 200 OR LENGTH(pca_analysis) < 200)
            THEN 'Missing Multi-Source Analysis' END as issue3
FROM key_findings_reports
WHERE content_validation_status != 'valid';