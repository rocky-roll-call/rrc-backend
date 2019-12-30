"""
Test Settings
"""

from rrc.settings.dev import *

MEDIA_ROOT = BASE_DIR / "test-media"

REST_FRAMEWORK["TEST_REQUEST_DEFAULT_FORMAT"] = "json"
