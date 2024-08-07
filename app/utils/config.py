import os

DB_USER = os.getenv('DB_USER', 'admin_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'secure_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'epicevents')