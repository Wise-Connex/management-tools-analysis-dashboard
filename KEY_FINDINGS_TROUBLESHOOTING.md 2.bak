# Key Findings Modal - Troubleshooting Guide

## 🔧 Common Issues and Solutions

### Issue 1: "No precomputed findings found for [tool] with [N] sources"

**Symptoms:**
- Modal shows error message about missing precomputed data
- Database miss occurs when clicking "Key Findings" button

**Causes:**
1. Combination not yet precomputed in database
2. Tool name translation issues
3. Source ordering mismatch
4. Language code issues

**Solutions:**

```python
# Debug the combination
retrieval_result = retrieval_service.retrieve_precomputed_findings(
    tool_name="Calidad Total",
    selected_sources=["Google Trends"],
    language="es"
)

if not retrieval_result["success"]:
    print(f"Error: {retrieval_result['error']}")
    print(f"Suggestion: {retrieval_result.get('suggestion', '')}")
    
    # Check if combination exists
    exists = retrieval_service.validate_combination_exists(
        tool_name="Calidad Total",
        selected_sources=["Google Trends"],
        language="es"
    )
    print(f"Combination exists: {exists}")
```

**Resolution Steps:**
1. Verify tool name is in Spanish (database stores Spanish names)
2. Check source names match database format exactly
3. Ensure language code is 'es' or 'en'
4. Run precomputation pipeline for missing combinations

### Issue 2: Content parsing fails with "Insufficient content"

**Symptoms:**
- Parser returns error about insufficient sections
- Modal shows incomplete content

**Causes:**
1. Database content is too short or empty
2. Required sections are missing
3. Content was corrupted during storage

**Solutions:**

```python
# Validate content structure
parse_result = content_parser.parse_modal_content(data, "es")
validation_result = content_parser.validate_content_structure(parse_result)

if not validation_result["valid"]:
    print(f"Validation issues: {validation_result['issues']}")
    print(f"Validation warnings: {validation_result['warnings']}")
    print(f"Content stats: {validation_result['stats']}")
```

**Resolution Steps:**
1. Check database content length for each section
2. Verify minimum content threshold (10 characters)
3. Regenerate content if sections are missing
4. Validate content during precomputation

### Issue 3: Performance issues (slow modal display)

**Symptoms:**
- Modal takes longer than 100ms to display
- User experiences noticeable delay

**Causes:**
1. Database query performance degradation
2. Network latency issues
3. Complex parsing operations
4. Resource constraints

**Solutions:**

```python
# Check performance metrics
metrics = retrieval_service.get_performance_metrics()
print(f"Average response time: {metrics['average_response_time_ms']:.2f}ms")
print(f"Total requests: {metrics['total_requests']}")
print(f"Successful retrievals: {metrics['successful_retrievals']}")
print(f"Database misses: {metrics['database_misses']}")
```

**Resolution Steps:**
1. Check database indexes are optimized
2. Verify SQLite is in WAL mode for better concurrency
3. Monitor system resources (CPU, memory, disk I/O)
4. Consider database connection pooling

### Issue 4: Language display issues

**Symptoms:**
- Section titles appear in wrong language
- Mixed language content in modal
- Translation inconsistencies

**Causes:**
1. Language parameter not passed correctly
2. Translation system issues
3. Section header mappings incorrect

**Solutions:**

```python
# Check language-specific sections
all_sections_es = content_parser.get_all_sections("es")
all_sections_en = content_parser.get_all_sections("en")

print("Spanish sections:")
for section in all_sections_es:
    print(f"  {section['name']}: {section['title']}")

print("\nEnglish sections:")
for section in all_sections_en:
    print(f"  {section['name']}: {section['title']}")
```

**Resolution Steps:**
1. Verify language parameter is 'es' or 'en'
2. Check translation mappings in section configs
3. Ensure consistent language throughout workflow
4. Test both languages with same combination

### Issue 5: Content formatting corruption

**Symptoms:**
- Markdown formatting lost
- Special characters garbled
- Paragraph breaks missing
- Bullet points not displaying

**Causes:**
1. Content cleaning too aggressive
2. Character encoding issues
3. Text transformation errors
4. Database storage problems

**Solutions:**

```python
# Test content cleaning
test_content = "This   has   excessive   spaces.\n\n\n\nMultiple lines.   "
cleaned = content_parser._clean_text_content(test_content)
print(f"Original: '{test_content}'")
print(f"Cleaned: '{cleaned}'")
print(f"Length change: {len(test_content)} -> {len(cleaned)}")
```

**Resolution Steps:**
1. Review content cleaning algorithm
2. Check character encoding (UTF-8)
3. Verify database text field types
4. Test with various content formats

## 📊 Performance Optimization

### Database Performance

**Monitoring Queries:**
```sql
-- Check query performance
EXPLAIN QUERY PLAN 
SELECT * FROM precomputed_findings 
WHERE tool_name = 'Calidad Total' 
AND sources_text = 'Google Trends' 
AND language = 'es';

-- Check index usage
PRAGMA index_list('precomputed_findings');
PRAGMA index_info('idx_findings_lookup');
```

**Optimization Steps:**
1. Ensure indexes are properly configured
2. Verify hash-based lookups are used
3. Check for table fragmentation
4. Monitor connection pool usage

### Memory Usage

**Monitoring Memory:**
```python
import psutil
import os

# Check current process memory
process = psutil.Process(os.getpid())
print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
print(f"CPU usage: {process.cpu_percent()}%")
```

**Memory Optimization:**
1. Implement connection pooling
2. Use streaming for large datasets
3. Optimize data structures
4. Implement caching where appropriate

## 🔍 Debugging Tools

### Enable Debug Logging

```python
import logging

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In your service calls
retrieval_result = retrieval_service.retrieve_precomputed_findings(
    tool_name="Calidad Total",
    selected_sources=["Google Trends"],
    language="es"
)
```

### Performance Profiling

```python
import time
import cProfile

# Profile a function call
def profile_retrieval():
    result = retrieval_service.retrieve_precomputed_findings(
        tool_name="Calidad Total",
        selected_sources=["Google Trends"],
        language="es"
    )
    return result

cProfile.run('profile_retrieval()')
```

### Database Inspection

```python
# Check database statistics
def check_database_health():
    from database_implementation.precomputed_findings_db import get_precomputed_db_manager
    
    db_manager = get_precomputed_db_manager()
    stats = db_manager.get_statistics()
    
    print("Database Statistics:")
    print(f"Total findings: {stats.get('total_findings', 0)}")
    print(f"Database size: {stats.get('database_size_mb', 0):.2f} MB")
    print(f"Findings by language: {stats.get('findings_by_language', {})}")
    print(f"Findings by type: {stats.get('findings_by_type', {})}")
    
    return stats
```

## 🚨 Emergency Procedures

### Database Corruption

**Symptoms:**
- SQLite errors during queries
- Inconsistent data retrieval
- Database file corruption messages

**Immediate Actions:**
1. Stop the application
2. Backup current database
3. Check database integrity
4. Restore from backup if needed

```bash
# Backup current database
cp data/precomputed_findings.db data/precomputed_findings.db.backup

# Check integrity
sqlite3 data/precomputed_findings.db "PRAGMA integrity_check;"

# If corrupted, restore from backup
cp data/precomputed_findings.db.backup data/precomputed_findings.db
```

### Service Unavailability

**Symptoms:**
- Import errors for new services
- Service initialization failures
- Module not found errors

**Immediate Actions:**
1. Check Python path and imports
2. Verify service files exist
3. Check for dependency issues
4. Restart application services

```python
# Test service availability
try:
    from dashboard_app.key_findings.retrieval_service import get_key_findings_retrieval_service
    from dashboard_app.key_findings.content_parser import get_key_findings_content_parser
    print("✅ Services available")
except ImportError as e:
    print(f"❌ Service import error: {e}")
```

## 📈 Monitoring and Alerting

### Key Metrics to Monitor

1. **Performance Metrics**
   - Average response time
   - 95th percentile response time
   - Error rate
   - Database hit rate

2. **Content Quality Metrics**
   - Section completeness rate
   - Content validation success rate
   - Language consistency

3. **System Health Metrics**
   - Memory usage
   - CPU utilization
   - Database connection health
   - Service availability

### Alerting Thresholds

```python
# Example alerting configuration
ALERT_THRESHOLDS = {
    "response_time_ms": 100,      # Alert if >100ms
    "error_rate": 0.01,           # Alert if >1%
    "content_validation": 0.95,   # Alert if <95%
    "memory_usage_mb": 500,       # Alert if >500MB
    "database_miss_rate": 0.05    # Alert if >5%
}
```

## 🔧 Maintenance Procedures

### Regular Maintenance Tasks

1. **Weekly**: Check performance metrics and optimize if needed
2. **Monthly**: Review error logs and fix recurring issues
3. **Quarterly**: Update documentation and run comprehensive tests
4. **Annually**: Architecture review and potential upgrades

### Database Maintenance

```sql
-- Weekly database maintenance
VACUUM;  -- Reclaim space and defragment
PRAGMA integrity_check;  -- Check database integrity
ANALYZE;  -- Update query planner statistics

-- Monthly index maintenance
REINDEX;  -- Rebuild all indexes
```

### Service Updates

1. **Backup current services**
2. **Test new services in staging**
3. **Deploy with rollback plan**
4. **Monitor post-deployment**
5. **Update documentation**

---

## 📞 Support Contacts

- **Technical Issues**: Check logs and run diagnostics first
- **Performance Problems**: Use profiling tools and metrics
- **Database Issues**: Check integrity and connection health
- **Content Problems**: Validate structure and formatting

Remember: Always test in a non-production environment first!