"""
Production Settings
"""

from decouple import config, Csv
from dj_database_url import parse as db_url
from rrc.settings.dev import *

DATABASES = {"default": config("DATABASE_URL", cast=db_url)}

DEBUG = config("SECRET_KEY")

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

JWT_AUTH["JWT_EXPIRATION_DELTA"] = datetime.timedelta(seconds=600)
