import os

DEBUG = True if os.environ.get("DEBUG") in ("1", 'true', 'True') else False

TOKEN = os.environ.get("TOKEN")

DATA_PATH = os.environ.get("DATA_PATH", "")

BASE_URL_API = os.environ.get("BASE_URL_API", "http://localhost:8000/api/v1")

PARSE_MODE = os.environ.get("PARSE_MODE", "HTML")

_DB_USER = os.environ.get('DB_USER')
_DB_HOST = os.environ.get('DB_HOST')
_DB_PORT = os.environ.get('DB_PORT')
_DB_SERVICE_NAME = os.environ.get('DB_SERVICE_NAME')
_DB_PASSWORD = os.environ.get('DB_PASSWORD')

DB_URI = f"{_DB_USER}/{_DB_PASSWORD}@{_DB_HOST}:{_DB_PORT}/{_DB_SERVICE_NAME}"


