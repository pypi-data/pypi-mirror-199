# coding=utf-8

OPENAPI_URL = "/openapi.json"
DOCS_URL = "/docs"
REDOC_URL = "/redoc"

ENABLE_GZIP = False
ENABLE_CORS = False
CORS_WHITELIST_DOMAINS = ["*"]
ACCESS_CONTROL_MAX_AGE = 60

STATIC_DIR = "./static"
TEMPLATE_FOLDER = "templates"

SESSION_SECRET_KEY = "session_secret_key"
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_MAXAGE = 60 * 60 * 24 * 30  # expire after 30 days
SESSION_COOKIE_HTTPONLY = True  # access denied from js
SESSION_COOKIE_SECURE = False  # visible only for https
SESSION_COOKIE_SAMESITE = "Strict"  # no cookie in cross site
SESSION_COOKIE_DOMAIN = None

SESSION_KEY_PREFIX = "session:"
SESSION_REDIS_ALIAS = "session"
