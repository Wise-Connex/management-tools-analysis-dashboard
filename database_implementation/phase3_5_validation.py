#!/usr/bin/env python3
"""
Phase 3.5: Production Readiness Validation
Data Quality Validation and System Integrity Testing

This script performs comprehensive validation of all 1,302 precomputed combinations
to ensure production-grade data quality, integrity, and performance.
"""

import sqlite3
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime
import statistics
from contextlib import contextmanager


class ProductionValidator:
    """Comprehensive production readiness validator for precomputed findings database."""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.start_time = time.time()
        self.results = {
            "validation_timestamp": datetime.now().isoformat(),
            "total_combinations": 0,
            "data_quality": {},
            "performance": {},
            "integrity": {},
            "errors": [],
            "warnings": [],
            "summary": {},
        }

    @contextmanager
    def get_connection(self):
        """Get database connection with proper error handling."""
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_path,
                timeout=30.0,
                isolation_level=None,  # Autocommit mode
            )
            conn.row_factory = sqlite3.Row
            # Apply performance optimizations
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=-64000")  # 64MB cache
            conn.execute("PRAGMA temp_store=MEMORY")
            conn.execute("PRAGMA foreign_keys=ON")
            yield conn
        except Exception as e:
            self.results["errors"].append(f"Database connection error: {str(e)}")
            raise
        finally:
            if conn is not None:
                conn.close()

    def validate_data_quality(self) -> Dict[str, Any]:
        """Comprehensive data quality validation across all 1,302 combinations."""
        print("🔍 Starting Data Quality Validation...")

        with self.get_connection() as conn:
            # Count total combinations
            total_count = conn.execute(
                "SELECT COUNT(*) FROM precomputed_findings WHERE is_active = 1"
            ).fetchone()[0]
            self.results["total_combinations"] = total_count

            if total_count != 1302:
                self.results["warnings"].append(
                    f"Expected 1,302 combinations, found {total_count}"
                )

            # Check coverage by language
            lang_coverage = conn.execute("""
                SELECT language, COUNT(*) as count, COUNT(DISTINCT tool_id) as tools_covered
                FROM precomputed_findings WHERE is_active = 1
                GROUP BY language
            """).fetchall()

            # Check coverage by analysis type
            type_coverage = conn.execute("""
                SELECT analysis_type, COUNT(*) as count
                FROM precomputed_findings WHERE is_active = 1
                GROUP BY analysis_type
            """).fetchall()

            # Validate required fields
            required_fields = [
                "combination_hash",
                "tool_id",
                "tool_name",
                "tool_display_name",
                "sources_text",
                "sources_ids",
                "sources_count",
                "language",
                "executive_summary",
                "analysis_type",
            ]

            field_validation = {}
            for field in required_fields:
                null_count = conn.execute(f"""
                    SELECT COUNT(*) FROM precomputed_findings 
                    WHERE is_active = 1 AND ({field} IS NULL OR {field} = '')
                """).fetchone()[0]
                field_validation[field] = {
                    "null_count": null_count,
                    "coverage": ((total_count - null_count) / total_count * 100)
                    if total_count > 0
                    else 0,
                }

            # Check analysis content quality
            content_quality = {
                "executive_summary": self._check_content_length(
                    conn, "executive_summary", 100
                ),
                "temporal_analysis": self._check_content_length(
                    conn, "temporal_analysis", 200
                ),
                "seasonal_analysis": self._check_content_length(
                    conn, "seasonal_analysis", 200
                ),
                "fourier_analysis": self._check_content_length(
                    conn, "fourier_analysis", 200
                ),
                "pca_analysis": self._check_content_length(conn, "pca_analysis", 300),
                "heatmap_analysis": self._check_content_length(
                    conn, "heatmap_analysis", 300
                ),
            }

            # Hash consistency validation
            hash_validation = self._validate_hash_consistency(conn)

            # Language distribution validation
            language_validation = self._validate_language_distribution(
                conn, lang_coverage
            )

            self.results["data_quality"] = {
                "total_combinations": total_count,
                "expected_combinations": 1302,
                "language_coverage": [dict(row) for row in lang_coverage],
                "analysis_type_coverage": [dict(row) for row in type_coverage],
                "field_validation": field_validation,
                "content_quality": content_quality,
                "hash_validation": hash_validation,
                "language_validation": language_validation,
            }

        print(
            f"✅ Data Quality Validation Complete: {total_count}/1,302 combinations validated"
        )
        return self.results["data_quality"]

    def _check_content_length(
        self, conn: sqlite3.Connection, field: str, min_length: int
    ) -> Dict[str, Any]:
        """Check content length distribution for a field."""
        stats = conn.execute(f"""
            SELECT 
                COUNT(*) as total,
                AVG(LENGTH({field})) as avg_length,
                MIN(LENGTH({field})) as min_length,
                MAX(LENGTH({field})) as max_length,
                SUM(CASE WHEN LENGTH({field}) >= {min_length} THEN 1 ELSE 0 END) as meets_min_length
            FROM precomputed_findings 
            WHERE is_active = 1 AND {field} IS NOT NULL
        """).fetchone()

        return {
            "field": field,
            "total_records": stats[0],
            "avg_length": round(stats[1], 2) if stats[1] else 0,
            "min_length": stats[2] or 0,
            "max_length": stats[3] or 0,
            "meets_min_length": stats[4],
            "meets_min_percentage": round((stats[4] / stats[0] * 100), 2)
            if stats[0] > 0
            else 0,
        }

    def _validate_hash_consistency(self, conn: sqlite3.Connection) -> Dict[str, Any]:
        """Validate that hash generation is consistent and reproducible."""
        # Sample 50 combinations for detailed hash validation
        sample = conn.execute("""
            SELECT combination_hash, tool_name, sources_text, language
            FROM precomputed_findings 
            WHERE is_active = 1 
            ORDER BY RANDOM() 
            LIMIT 50
        """).fetchall()

        hash_validation_results = []
        for row in sample:
            # Recalculate expected hash
            expected_hash = self._calculate_expected_hash(
                row["tool_name"], row["sources_text"], row["language"]
            )
            is_consistent = expected_hash == row["combination_hash"]
            hash_validation_results.append(
                {
                    "original_hash": row["combination_hash"],
                    "expected_hash": expected_hash,
                    "is_consistent": is_consistent,
                }
            )

        consistent_count = sum(1 for r in hash_validation_results if r["is_consistent"])

        return {
            "sample_size": len(sample),
            "consistent_hashes": consistent_count,
            "inconsistent_hashes": len(sample) - consistent_count,
            "consistency_rate": round(consistent_count / len(sample) * 100, 2),
            "validation_results": hash_validation_results,
        }

    def _calculate_expected_hash(
        self, tool_name: str, sources_text: str, language: str
    ) -> str:
        """Recalculate expected hash for validation."""
        import hashlib
        import json

        # Parse sources
        sources_list = [s.strip() for s in sources_text.split(",")]
        source_names = sorted(
            [source.lower().replace(" ", "_") for source in sources_list]
        )
        tool_name_norm = tool_name.lower().replace(" ", "_")

        combination_data = {
            "tool": tool_name_norm,
            "sources": source_names,
            "language": language,
        }

        hash_input = json.dumps(combination_data, sort_keys=True)
        hash_hex = hashlib.md5(hash_input.encode()).hexdigest()[:10]

        return f"{tool_name_norm}_{'_'.join(source_names)}_{language}_{hash_hex}"

    def _validate_language_distribution(
        self, conn: sqlite3.Connection, lang_coverage: List
    ) -> Dict[str, Any]:
        """Validate language distribution is balanced."""
        total = sum(row["count"] for row in lang_coverage)

        lang_distribution = {}
        for row in lang_coverage:
            lang_distribution[row["language"]] = {
                "count": row["count"],
                "percentage": round(row["count"] / total * 100, 2) if total > 0 else 0,
            }

        # Check for balanced distribution (should be roughly 50/50)
        es_count = lang_distribution.get("es", {}).get("count", 0)
        en_count = lang_distribution.get("en", {}).get("count", 0)
        is_balanced = abs(es_count - en_count) <= total * 0.1  # Within 10% tolerance

        return {
            "total": total,
            "distribution": lang_distribution,
            "is_balanced": is_balanced,
            "balance_tolerance": "10%",
        }

    def validate_performance(self) -> Dict[str, Any]:
        """Comprehensive performance validation and optimization."""
        print("⚡ Starting Performance Validation...")

        performance_metrics = {}

        # Test single lookup performance
        single_lookup_times = []
        with self.get_connection() as conn:
            # Get sample combination hashes
            sample_hashes = conn.execute("""
                SELECT combination_hash FROM precomputed_findings 
                WHERE is_active = 1 
                ORDER BY RANDOM() 
                LIMIT 100
            """).fetchall()

            for row in sample_hashes[:50]:  # Test 50 lookups
                start_time = time.time()
                result = conn.execute(
                    """
                    SELECT * FROM precomputed_findings 
                    WHERE combination_hash = ? AND is_active = 1
                """,
                    (row["combination_hash"],),
                ).fetchone()
                lookup_time = (time.time() - start_time) * 1000  # Convert to ms
                single_lookup_times.append(lookup_time)

        # Test batch lookup performance
        batch_lookup_times = []
        if len(sample_hashes) >= 20:
            with self.get_connection() as conn:
                for i in range(
                    0, min(50, len(sample_hashes)), 10
                ):  # Test 5 batches of 10
                    batch = [
                        row["combination_hash"] for row in sample_hashes[i : i + 10]
                    ]
                    placeholders = ",".join(["?" for _ in batch])

                    start_time = time.time()
                    results = conn.execute(
                        f"""
                        SELECT combination_hash FROM precomputed_findings 
                        WHERE combination_hash IN ({placeholders}) AND is_active = 1
                    """,
                        batch,
                    ).fetchall()
                    batch_time = (time.time() - start_time) * 1000
                    batch_lookup_times.append(batch_time)

        # Test tool-based queries
        tool_query_times = []
        with self.get_connection() as conn:
            sample_tools = conn.execute("""
                SELECT DISTINCT tool_id FROM precomputed_findings 
                WHERE is_active = 1 
                ORDER BY RANDOM() 
                LIMIT 20
            """).fetchall()

            for row in sample_tools[:10]:  # Test 10 tool queries
                start_time = time.time()
                results = conn.execute(
                    """
                    SELECT COUNT(*) FROM precomputed_findings 
                    WHERE tool_id = ? AND is_active = 1
                """,
                    (row["tool_id"],),
                ).fetchone()
                query_time = (time.time() - start_time) * 1000
                tool_query_times.append(query_time)

        # Calculate performance statistics
        performance_metrics = {
            "single_lookup": {
                "sample_size": len(single_lookup_times),
                "avg_time_ms": round(statistics.mean(single_lookup_times), 3)
                if single_lookup_times
                else 0,
                "median_time_ms": round(statistics.median(single_lookup_times), 3)
                if single_lookup_times
                else 0,
                "min_time_ms": round(min(single_lookup_times), 3)
                if single_lookup_times
                else 0,
                "max_time_ms": round(max(single_lookup_times), 3)
                if single_lookup_times
                else 0,
                "std_dev": round(statistics.stdev(single_lookup_times), 3)
                if len(single_lookup_times) > 1
                else 0,
            },
            "batch_lookup": {
                "sample_size": len(batch_lookup_times),
                "avg_time_ms": round(statistics.mean(batch_lookup_times), 3)
                if batch_lookup_times
                else 0,
                "median_time_ms": round(statistics.median(batch_lookup_times), 3)
                if batch_lookup_times
                else 0,
                "min_time_ms": round(min(batch_lookup_times), 3)
                if batch_lookup_times
                else 0,
                "max_time_ms": round(max(batch_lookup_times), 3)
                if batch_lookup_times
                else 0,
            },
            "tool_query": {
                "sample_size": len(tool_query_times),
                "avg_time_ms": round(statistics.mean(tool_query_times), 3)
                if tool_query_times
                else 0,
                "median_time_ms": round(statistics.median(tool_query_times), 3)
                if tool_query_times
                else 0,
                "min_time_ms": round(min(tool_query_times), 3)
                if tool_query_times
                else 0,
                "max_time_ms": round(max(tool_query_times), 3)
                if tool_query_times
                else 0,
            },
        }

        # Performance targets validation
        targets_met = {
            "single_lookup_sub_1ms": performance_metrics["single_lookup"]["avg_time_ms"]
            < 1.0,
            "batch_lookup_sub_10ms": performance_metrics["batch_lookup"]["avg_time_ms"]
            < 10.0,
            "tool_query_sub_5ms": performance_metrics["tool_query"]["avg_time_ms"]
            < 5.0,
        }

        self.results["performance"] = {
            "metrics": performance_metrics,
            "targets_met": targets_met,
            "overall_performance": "EXCELLENT"
            if all(targets_met.values())
            else "GOOD"
            if any(targets_met.values())
            else "NEEDS_OPTIMIZATION",
        }

        print(
            f"✅ Performance Validation Complete: {self.results['performance']['overall_performance']}"
        )
        return self.results["performance"]

    def validate_integrity(self) -> Dict[str, Any]:
        """Database integrity and referential consistency validation."""
        print("🔐 Starting Database Integrity Validation...")

        with self.get_connection() as conn:
            integrity_checks = {}

            # Foreign key integrity
            fk_violations = conn.execute("""
                SELECT COUNT(*) FROM precomputed_findings pf
                LEFT JOIN management_tools mt ON pf.tool_id = mt.id
                WHERE mt.id IS NULL AND pf.is_active = 1
            """).fetchone()[0]

            # Unique constraint violations
            hash_duplicates = conn.execute("""
                SELECT combination_hash, COUNT(*) as cnt
                FROM precomputed_findings 
                WHERE is_active = 1
                GROUP BY combination_hash
                HAVING COUNT(*) > 1
            """).fetchall()

            # Data type consistency
            data_type_issues = conn.execute("""
                SELECT 
                    COUNT(CASE WHEN sources_count < 1 OR sources_count > 31 THEN 1 END) as invalid_source_count,
                    COUNT(CASE WHEN language NOT IN ('es', 'en') THEN 1 END) as invalid_language,
                    COUNT(CASE WHEN analysis_type NOT IN ('single_source', 'multi_source') THEN 1 END) as invalid_analysis_type
                FROM precomputed_findings 
                WHERE is_active = 1
            """).fetchone()

            # Range validation
            range_issues = conn.execute("""
                SELECT 
                    COUNT(CASE WHEN confidence_score < 0 OR confidence_score > 1 THEN 1 END) as invalid_confidence,
                    COUNT(CASE WHEN data_points_analyzed < 0 THEN 1 END) as invalid_data_points
                FROM precomputed_findings 
                WHERE is_active = 1 AND confidence_score IS NOT NULL
            """).fetchone()

            integrity_checks = {
                "foreign_key_integrity": {
                    "violations": fk_violations,
                    "status": "PASS" if fk_violations == 0 else "FAIL",
                },
                "hash_uniqueness": {
                    "duplicate_hashes": len(hash_duplicates),
                    "details": [dict(row) for row in hash_duplicates],
                    "status": "PASS" if len(hash_duplicates) == 0 else "FAIL",
                },
                "data_type_consistency": {
                    "invalid_source_count": data_type_issues[0],
                    "invalid_language": data_type_issues[1],
                    "invalid_analysis_type": data_type_issues[2],
                    "status": "PASS"
                    if all(x == 0 for x in data_type_issues)
                    else "FAIL",
                },
                "range_validation": {
                    "invalid_confidence": range_issues[0],
                    "invalid_data_points": range_issues[1],
                    "status": "PASS" if all(x == 0 for x in range_issues) else "FAIL",
                },
            }

            # Overall integrity status
            all_checks_pass = all(
                check["status"] == "PASS" for check in integrity_checks.values()
            )

            self.results["integrity"] = {
                "checks": integrity_checks,
                "overall_status": "PASS" if all_checks_pass else "FAIL",
                "critical_issues": sum(
                    1
                    for check in integrity_checks.values()
                    if check["status"] == "FAIL"
                ),
            }

        print(
            f"✅ Database Integrity Validation Complete: {self.results['integrity']['overall_status']}"
        )
        return self.results["integrity"]

    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive validation report."""
        duration = time.time() - self.start_time

        # Overall summary
        data_quality_score = self._calculate_data_quality_score()
        performance_score = self._calculate_performance_score()
        integrity_score = (
            100 if self.results["integrity"]["overall_status"] == "PASS" else 0
        )

        overall_score = round(
            (data_quality_score + performance_score + integrity_score) / 3, 2
        )

        self.results["summary"] = {
            "validation_duration_seconds": round(duration, 2),
            "overall_score": overall_score,
            "data_quality_score": data_quality_score,
            "performance_score": performance_score,
            "integrity_score": integrity_score,
            "production_ready": overall_score >= 95,
            "recommendations": self._generate_recommendations(),
        }

        return self._format_report()

    def _calculate_data_quality_score(self) -> float:
        """Calculate data quality score (0-100)."""
        dq = self.results.get("data_quality", {})

        # Base score starts at 100
        score = 100.0

        # Deduct for missing combinations
        if dq.get("total_combinations", 0) != 1302:
            score -= 10

        # Deduct for field validation issues
        field_validation = dq.get("field_validation", {})
        for field, validation in field_validation.items():
            if validation.get("coverage", 100) < 95:
                score -= 5

        # Deduct for hash consistency issues
        hash_validation = dq.get("hash_validation", {})
        if hash_validation.get("consistency_rate", 100) < 100:
            score -= 20

        # Deduct for content quality issues
        content_quality = dq.get("content_quality", {})
        for field, quality in content_quality.items():
            if quality.get("meets_min_percentage", 100) < 90:
                score -= 5

        return max(0, score)

    def _calculate_performance_score(self) -> float:
        """Calculate performance score (0-100)."""
        perf = self.results.get("performance", {})
        targets_met = perf.get("targets_met", {})

        score = 0
        if targets_met.get("single_lookup_sub_1ms", False):
            score += 40
        if targets_met.get("batch_lookup_sub_10ms", False):
            score += 30
        if targets_met.get("tool_query_sub_5ms", False):
            score += 30

        return score

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []

        # Data quality recommendations
        if self.results.get("data_quality", {}).get("total_combinations", 0) != 1302:
            recommendations.append(
                "Address missing combinations to reach target of 1,302"
            )

        # Performance recommendations
        if (
            not self.results.get("performance", {})
            .get("targets_met", {})
            .get("single_lookup_sub_1ms", True)
        ):
            recommendations.append(
                "Optimize single lookup queries for sub-millisecond performance"
            )

        # Integrity recommendations
        if self.results.get("integrity", {}).get("overall_status") != "PASS":
            recommendations.append(
                "Address database integrity violations before production deployment"
            )

        if not recommendations:
            recommendations.append(
                "No critical issues found - system is production ready"
            )

        return recommendations

    def _format_report(self) -> str:
        """Format the comprehensive validation report."""
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     PRODUCTION READINESS VALIDATION REPORT                   ║
║                           Phase 3.5 Comprehensive Analysis                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 OVERALL ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Validation Timestamp: {self.results["validation_timestamp"]}
Validation Duration: {self.results["summary"]["validation_duration_seconds"]} seconds
Overall Score: {self.results["summary"]["overall_score"]}/100
Production Ready: {"✅ YES" if self.results["summary"]["production_ready"] else "❌ NO"}

🔍 DATA QUALITY ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Combinations: {self.results["data_quality"]["total_combinations"]}/1,302
Data Quality Score: {self.results["summary"]["data_quality_score"]}/100

Language Distribution:"""

        for lang in self.results["data_quality"]["language_coverage"]:
            report += f"\n  • {lang['language'].upper()}: {lang['count']} combinations ({lang['tools_covered']} tools)"

        report += f"""

Hash Consistency: {self.results["data_quality"]["hash_validation"]["consistency_rate"]}% ({self.results["data_quality"]["hash_validation"]["consistent_hashes"]}/{self.results["data_quality"]["hash_validation"]["sample_size"]} samples)"""

        report += f"""

⚡ PERFORMANCE ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Performance Score: {self.results["summary"]["performance_score"]}/100
Single Lookup (avg): {self.results["performance"]["metrics"]["single_lookup"]["avg_time_ms"]}ms
Batch Lookup (avg): {self.results["performance"]["metrics"]["batch_lookup"]["avg_time_ms"]}ms
Tool Query (avg): {self.results["performance"]["metrics"]["tool_query"]["avg_time_ms"]}ms

Performance Targets Met:"""
        for target, met in self.results["performance"]["targets_met"].items():
            status = "✅" if met else "❌"
            report += f"\n  {status} {target.replace('_', ' ').title()}"

        report += f"""

🔐 INTEGRITY ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Integrity Score: {self.results["summary"]["integrity_score"]}/100
Overall Status: {self.results["integrity"]["overall_status"]}
Critical Issues: {self.results["integrity"]["critical_issues"]}

Integrity Checks:"""
        for check_name, check_result in self.results["integrity"]["checks"].items():
            status = "✅" if check_result["status"] == "PASS" else "❌"
            report += f"\n  {status} {check_name.replace('_', ' ').title()}"

        report += f"""

💡 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        for i, rec in enumerate(self.results["summary"]["recommendations"], 1):
            report += f"\n{i}. {rec}"

        report += f"""

📈 VALIDATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Database contains {self.results["data_quality"]["total_combinations"]} precomputed combinations
✅ {self.results["performance"]["metrics"]["single_lookup"]["sample_size"]} performance tests completed
✅ {len(self.results["integrity"]["checks"])} integrity checks performed
✅ Production readiness score: {self.results["summary"]["overall_score"]}/100

Status: {"🎉 PRODUCTION READY" if self.results["summary"]["production_ready"] else "⚠️  REQUIRES ATTENTION"}
"""

        return report


def main():
    """Main validation execution."""
    db_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"

    if not Path(db_path).exists():
        print(f"❌ Database not found at: {db_path}")
        print("Please ensure the precomputed findings database has been created.")
        return

    print("🚀 Starting Phase 3.5: Production Readiness Validation")
    print("=" * 80)

    validator = ProductionValidator(db_path)

    try:
        # Run all validation phases
        validator.validate_data_quality()
        validator.validate_performance()
        validator.validate_integrity()

        # Generate comprehensive report
        report = validator.generate_comprehensive_report()
        print(report)

        # Save detailed results to JSON
        results_path = Path(db_path).parent / "validation_results.json"
        with open(results_path, "w") as f:
            json.dump(validator.results, f, indent=2, default=str)

        print(f"\n📄 Detailed results saved to: {results_path}")

        # Return exit code based on production readiness
        return 0 if validator.results["summary"]["production_ready"] else 1

    except Exception as e:
        print(f"❌ Validation failed with error: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
