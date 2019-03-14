"""
Production Settings
"""

import dj_database_url
from rrc.settings.dev import *

DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}

DEBUG = bool(os.getenv("DJANGO_DEBUG", ""))

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", SECRET_KEY)

ALLOWED_HOSTS = ["*"]

JWT_AUTH["JWT_EXPIRATION_DELTA"] = datetime.timedelta(seconds=600)
