-- Add missing columns to precomputed_findings table
ALTER TABLE precomputed_findings ADD COLUMN strategic_synthesis TEXT DEFAULT '';
ALTER TABLE precomputed_findings ADD COLUMN conclusions TEXT DEFAULT '';

-- Update existing records with default empty content for new columns
UPDATE precomputed_findings SET strategic_synthesis = '', conclusions = '' WHERE strategic_synthesis IS NULL OR conclusions IS NULL;

-- Verify the changes
SELECT name FROM sqlite_master WHERE type='table' AND name='precomputed_findings';
PRAGMA table_info(precomputed_findings);
