import os
from pathlib import Path

import dotenv
from split_settings.tools import include

dotenv.load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("CASH_MANAGER_SECRET_KEY")
DEBUG = os.environ.get("CASH_MANAGER_DEBUG", False) == "True"

ALLOWED_HOSTS = os.environ.get(
    "CASH_MANAGER_HOSTS",
    ["localhost", "127.0.0.1"],
)
ROOT_URLCONF = 'service_cash_manager.urls'
WSGI_APPLICATION = 'service_cash_manager.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Components configs
include(
    "components/installed_apps.py",
    "components/middleware.py",
    "components/templates.py",
    "components/databases.py",
    "components/auth.py",
    "components/cors.py",
    "components/logging_format.py",
)
