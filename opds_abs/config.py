"""Configuration settings for the application.

This module provides configuration settings for the application, loaded from
environment variables.
"""
# Standard library imports
import os
import pathlib

# Optional deployment path prefix for the application.
# Example: BASE_PATH=/service will expose OPDS at /service/opds
BASE_PATH = os.getenv("BASE_PATH", "").strip()
if BASE_PATH and not BASE_PATH.startswith("/"):
    BASE_PATH = "/" + BASE_PATH
BASE_PATH = BASE_PATH.rstrip("/")

# Audiobookshelf URL configuration
_abs_url = os.getenv("AUDIOBOOKSHELF_URL")
_abs_internal = os.getenv("AUDIOBOOKSHELF_INTERNAL_URL")
_abs_external = os.getenv("AUDIOBOOKSHELF_EXTERNAL_URL")

# Prioritize specific variables, fallback to the legacy AUDIOBOOKSHELF_URL, and ensure no trailing slashes
AUDIOBOOKSHELF_INTERNAL_URL = (_abs_internal or _abs_url or "http://localhost").rstrip("/")
AUDIOBOOKSHELF_EXTERNAL_URL = (_abs_external or _abs_url or AUDIOBOOKSHELF_INTERNAL_URL).rstrip("/")

# External URL for the OPDS service (for absolute links in feeds)
OPDS_EXTERNAL_URL = (AUDIOBOOKSHELF_EXTERNAL_URL + BASE_PATH).rstrip("/") if AUDIOBOOKSHELF_EXTERNAL_URL else ""

# API endpoints
AUDIOBOOKSHELF_API = AUDIOBOOKSHELF_INTERNAL_URL + "/api"

# Derived path helpers for OPDS and static content.
OPDS_BASE_PATH = f"{BASE_PATH}/opds" if BASE_PATH else "/opds"
STATIC_BASE_PATH = f"{BASE_PATH}/static" if BASE_PATH else "/static"

# Authentication configuration
AUTH_ENABLED = os.getenv("AUTH_ENABLED", "true").lower() == "true"
AUTH_CACHE_EXPIRY = int(os.getenv("AUTH_CACHE_EXPIRY", "86400"))  # Default: 24 hours
API_KEY_AUTH_ENABLED = os.getenv("API_KEY_AUTH_ENABLED", "true").lower() == "true"  # Enable API key authentication
AUTH_TOKEN_CACHING = os.getenv("AUTH_TOKEN_CACHING", "true").lower() == "true"  # Enable token caching

# Cache configuration (in seconds)
AUTHORS_CACHE_EXPIRY = int(os.getenv("AUTHORS_CACHE_EXPIRY", "1800"))  # 30 minutes for collections
COLLECTIONS_CACHE_EXPIRY = int(os.getenv("COLLECTIONS_CACHE_EXPIRY", "1800"))  # 30 minutes for collections
DEFAULT_CACHE_EXPIRY = int(os.getenv("DEFAULT_CACHE_EXPIRY", "3600"))  # Default: 1 hour
LIBRARIES_CACHE_EXPIRY = int(os.getenv("LIBRARIES_CACHE_EXPIRY", "3600")) # Default: 1 hour
LIBRARY_ITEMS_CACHE_EXPIRY = int(os.getenv("LIBRARY_ITEMS_CACHE_EXPIRY", "1800"))  # Default: 30 minutes
SEARCH_RESULTS_CACHE_EXPIRY = int(os.getenv("SEARCH_RESULTS_CACHE_EXPIRY", "600"))  # Default: 10 minutes
SERIES_DETAILS_CACHE_EXPIRY = int(os.getenv("SERIES_DETAILS_CACHE_EXPIRY", "3600"))  # Default: 1 hour
SERIES_ITEMS_CACHE_EXPIRY = int(os.getenv("SERIES_ITEMS_CACHE_EXPIRY", "1800"))  # Default: 30 minutes

# Cache persistence configuration
CACHE_PERSISTENCE_ENABLED = os.getenv("CACHE_PERSISTENCE_ENABLED", "true").lower() == "true"
CACHE_FILE_PATH = os.getenv("CACHE_FILE_PATH", str(pathlib.Path(__file__).parent / "data" / "cache.pkl"))
CACHE_SAVE_INTERVAL = int(os.getenv("CACHE_SAVE_INTERVAL", "300"))  # Save cache every 5 minutes by default

# Pagination configuration
PAGINATION_ENABLED = os.getenv("PAGINATION_ENABLED", "true").lower() == "true"  # Enable/disable pagination
ITEMS_PER_PAGE = int(os.getenv("ITEMS_PER_PAGE", "25"))  # Default: 25 items per page

# Logging configuration
LOG_LEVEL = os.environ.get("OPDS_LOG_LEVEL", "INFO").upper()
