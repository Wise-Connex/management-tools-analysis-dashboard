"""
Regeneration API Endpoints (Phase 4)

This module provides secure API endpoints for regeneration requests.
It includes authentication and rate limiting to prevent abuse.
"""

import hashlib
import hmac
import time
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

# Import database components
import sys

sys.path.insert(0, "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard")

try:
    from database_implementation.precomputed_findings_db import (
        get_precomputed_db_manager,
    )

    _precomputed_db_manager = get_precomputed_db_manager()
    logging.info("✅ Regeneration API: Precomputed database connected")
except ImportError as e:
    logging.warning(f"⚠️ Regeneration API: Database not available: {e}")
    _precomputed_db_manager = None

# Import existing Key Findings service
try:
    from key_findings.key_findings_service import KeyFindingsService

    KEY_FINDINGS_SERVICE_AVAILABLE = True
except ImportError as e:
    logging.warning(f"⚠️ Regeneration API: Key Findings service not available: {e}")
    KEY_FINDINGS_SERVICE_AVAILABLE = False


class RegenerationAPIAuth:
    """
    Simple API authentication using HMAC tokens.
    """

    def __init__(self, api_secret: str = None):
        """
        Initialize authentication with API secret.

        Args:
            api_secret: Secret key for HMAC authentication
        """
        self.api_secret = api_secret or "regeneration-secret-key-change-in-production"
        self.request_logs = {}  # Track requests per API key
        self.rate_limits = {"requests_per_hour": 50, "requests_per_day": 200}

    def generate_api_key(self, identifier: str = "admin") -> str:
        """
        Generate API key for authorized users.

        Args:
            identifier: User/agent identifier

        Returns:
            API key string
        """
        timestamp = str(int(time.time()))
        data = f"{identifier}:{timestamp}"
        signature = hmac.new(
            self.api_secret.encode(), data.encode(), hashlib.sha256
        ).hexdigest()
        return f"{identifier}:{timestamp}:{signature[:16]}"

    def validate_api_key(self, api_key: str) -> Dict[str, Any]:
        """
        Validate API key and check rate limits.

        Args:
            api_key: API key to validate

        Returns:
            Validation result with user info and limits
        """
        try:
            identifier, timestamp, signature = api_key.split(":")

            # Verify signature
            data = f"{identifier}:{timestamp}"
            expected_signature = hmac.new(
                self.api_secret.encode(), data.encode(), hashlib.sha256
            ).hexdigest()[:16]

            if not hmac.compare_digest(signature, expected_signature):
                return {"valid": False, "error": "Invalid signature"}

            # Check timestamp (keys expire after 24 hours)
            key_time = int(timestamp)
            now = int(time.time())
            if now - key_time > 86400:  # 24 hours
                return {"valid": False, "error": "API key expired"}

            # Check rate limits
            if identifier not in self.request_logs:
                self.request_logs[identifier] = []

            current_time = time.time()
            hour_ago = current_time - 3600
            day_ago = current_time - 86400

            # Clean old requests
            self.request_logs[identifier] = [
                req_time
                for req_time in self.request_logs[identifier]
                if req_time > day_ago
            ]

            recent_requests = len(
                [t for t in self.request_logs[identifier] if t > hour_ago]
            )
            daily_requests = len(self.request_logs[identifier])

            if recent_requests >= self.rate_limits["requests_per_hour"]:
                return {
                    "valid": False,
                    "error": f"Hourly rate limit exceeded ({self.rate_limits['requests_per_hour']}/hour)",
                }

            if daily_requests >= self.rate_limits["requests_per_day"]:
                return {
                    "valid": False,
                    "error": f"Daily rate limit exceeded ({self.rate_limits['requests_per_day']}/day)",
                }

            # Log successful validation
            self.request_logs[identifier].append(current_time)

            return {
                "valid": True,
                "identifier": identifier,
                "remaining_hourly": self.rate_limits["requests_per_hour"]
                - recent_requests
                - 1,
                "remaining_daily": self.rate_limits["requests_per_day"]
                - daily_requests
                - 1,
                "expires_at": key_time + 86400,
            }

        except Exception as e:
            return {"valid": False, "error": f"Key validation failed: {str(e)}"}


class RegenerationAPIService:
    """
    Service for handling regeneration requests via API.
    """

    def __init__(self, auth: RegenerationAPIAuth):
        """
        Initialize regeneration API service.

        Args:
            auth: Authentication instance
        """
        self.auth = auth
        self.precomputed_db = _precomputed_db_manager
        self.request_queue = []  # Queue for regeneration requests
        self.processing_status = {}  # Track processing status

    def request_regeneration(
        self,
        api_key: str,
        tool_name: str,
        selected_sources: List[str],
        language: str = "es",
        priority: int = 5,
    ) -> Dict[str, Any]:
        """
        Request regeneration via API.

        Args:
            api_key: API authentication key
            tool_name: Management tool name
            selected_sources: List of data sources
            language: Analysis language
            priority: Priority level (1-10)

        Returns:
            Request response
        """
        # Validate authentication
        auth_result = self.auth.validate_api_key(api_key)
        if not auth_result["valid"]:
            return {
                "success": False,
                "error": f"Authentication failed: {auth_result['error']}",
            }

        # Validate parameters
        if not tool_name or not selected_sources:
            return {
                "success": False,
                "error": "Missing required parameters: tool_name, selected_sources",
            }

        if language not in ["es", "en"]:
            return {"success": False, "error": 'Language must be "es" or "en"'}

        if not (1 <= priority <= 10):
            return {"success": False, "error": "Priority must be between 1 and 10"}

        try:
            # Check if combination already exists
            if self.precomputed_db:
                combination_hash = self.precomputed_db.generate_combination_hash(
                    tool_name, selected_sources, language
                )
                existing = self.precomputed_db.get_combination_by_hash(combination_hash)

                if existing:
                    return {
                        "success": True,
                        "message": "Analysis already exists in database",
                        "combination_hash": combination_hash,
                        "existing_analysis": True,
                    }

            # Create regeneration job
            if self.precomputed_db:
                job_id = self.precomputed_db.create_computation_job(
                    tool_name, selected_sources, language, priority=priority
                )

                request_info = {
                    "job_id": job_id,
                    "tool_name": tool_name,
                    "selected_sources": selected_sources,
                    "language": language,
                    "priority": priority,
                    "created_at": datetime.now().isoformat(),
                    "status": "pending",
                    "requester": auth_result["identifier"],
                }

                self.request_queue.append(request_info)

                logging.info(
                    f"🔄 Regeneration requested: {tool_name} (job {job_id}) by {auth_result['identifier']}"
                )

                return {
                    "success": True,
                    "message": "Regeneration request submitted",
                    "job_id": job_id,
                    "estimated_completion": "2-5 minutes",
                    "remaining_hourly_requests": auth_result["remaining_hourly"],
                    "remaining_daily_requests": auth_result["remaining_daily"],
                }
            else:
                return {
                    "success": False,
                    "error": "Database not available for regeneration requests",
                }

        except Exception as e:
            logging.error(f"Regeneration request failed: {e}")
            return {"success": False, "error": f"Regeneration request failed: {str(e)}"}

    def get_regeneration_status(self, api_key: str, job_id: str) -> Dict[str, Any]:
        """
        Get status of regeneration request.

        Args:
            api_key: API authentication key
            job_id: Job ID to check

        Returns:
            Status response
        """
        # Validate authentication
        auth_result = self.auth.validate_api_key(api_key)
        if not auth_result["valid"]:
            return {
                "success": False,
                "error": f"Authentication failed: {auth_result['error']}",
            }

        try:
            if self.precomputed_db:
                # Get job status from database
                next_job = self.precomputed_db.get_next_pending_job()

                # Check if this job is being processed
                status = "unknown"
                if next_job and str(next_job.get("id", "")) == str(job_id):
                    status = "processing"
                else:
                    status = "pending"

                return {
                    "success": True,
                    "job_id": job_id,
                    "status": status,
                    "queried_at": datetime.now().isoformat(),
                }
            else:
                return {
                    "success": False,
                    "error": "Database not available for status checks",
                }

        except Exception as e:
            logging.error(f"Status check failed: {e}")
            return {"success": False, "error": f"Status check failed: {str(e)}"}

    def request_batch_regeneration(
        self, api_key: str, combinations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Request batch regeneration for multiple combinations.

        Args:
            api_key: API authentication key
            combinations: List of combination dictionaries

        Returns:
            Batch response
        """
        # Validate authentication
        auth_result = self.auth.validate_api_key(api_key)
        if not auth_result["valid"]:
            return {
                "success": False,
                "error": f"Authentication failed: {auth_result['error']}",
            }

        if len(combinations) > 10:  # Limit batch size
            return {
                "success": False,
                "error": "Maximum 10 combinations per batch request",
            }

        successful_requests = 0
        failed_requests = 0
        job_ids = []

        for combo in combinations:
            try:
                result = self.request_regeneration(
                    api_key=api_key,
                    tool_name=combo.get("tool_name", ""),
                    selected_sources=combo.get("selected_sources", []),
                    language=combo.get("language", "es"),
                    priority=combo.get("priority", 5),
                )

                if result["success"]:
                    successful_requests += 1
                    if "job_id" in result:
                        job_ids.append(result["job_id"])
                else:
                    failed_requests += 1

            except Exception as e:
                failed_requests += 1
                logging.error(f"Batch request failed for combination: {e}")

        return {
            "success": True,
            "message": f"Batch processing initiated",
            "total_combinations": len(combinations),
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "job_ids": job_ids,
            "estimated_completion": "5-15 minutes for batch",
        }


# Initialize authentication and API service
regeneration_auth = RegenerationAPIAuth()
regeneration_api = RegenerationAPIService(regeneration_auth)


# Helper function to get API key for authorized users
def get_admin_api_key() -> str:
    """Generate API key for admin access."""
    return regeneration_auth.generate_api_key("admin")


def get_developer_api_key() -> str:
    """Generate API key for developer access."""
    return regeneration_auth.generate_api_key("developer")


# API endpoint functions (for integration with web framework)
def handle_regeneration_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle regeneration request from web endpoint.

    Args:
        request_data: Request data containing API key and parameters

    Returns:
        API response
    """
    api_key = request_data.get("api_key")
    tool_name = request_data.get("tool_name")
    selected_sources = request_data.get("selected_sources", [])
    language = request_data.get("language", "es")
    priority = request_data.get("priority", 5)

    return regeneration_api.request_regeneration(
        api_key=api_key,
        tool_name=tool_name,
        selected_sources=selected_sources,
        language=language,
        priority=priority,
    )


def handle_batch_regeneration_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle batch regeneration request from web endpoint.

    Args:
        request_data: Request data containing API key and combinations

    Returns:
        API response
    """
    api_key = request_data.get("api_key")
    combinations = request_data.get("combinations", [])

    return regeneration_api.request_batch_regeneration(
        api_key=api_key, combinations=combinations
    )


def handle_status_check(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle status check request from web endpoint.

    Args:
        request_data: Request data containing API key and job ID

    Returns:
        API response
    """
    api_key = request_data.get("api_key")
    job_id = request_data.get("job_id")

    return regeneration_api.get_regeneration_status(api_key=api_key, job_id=job_id)
