# =============================================================
#  SMART HR SYSTEM - Database Configuration
#  Copy this file to config.py and fill in your own values.
# =============================================================

# Oracle connection settings
DB_HOST     = "localhost"       # hostname or IP where Oracle is running
DB_PORT     = 1521              # default Oracle listener port
DB_SERVICE  = "xe"              # service name (XE for Oracle XE, ORCL for other)
DB_USER     = "your_username"   # Oracle schema username
DB_PASSWORD = "your_password"   # Oracle schema password

# Flask settings
SECRET_KEY  = "change_this_to_a_random_secret_key"  # used for session signing
DEBUG       = True
