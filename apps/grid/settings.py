"""
This is an optional file that defined app level settings such as:
- database settings
- session settings
- i18n settings
This file is provided as an example:
"""
import os

# db settings
APP_FOLDER = os.path.dirname(__file__)
APP_NAME = os.path.split(APP_FOLDER)[-1]
# DB_FOLDER:    Sets the place where migration files will be created
#               and is the store location for SQLite databases
#DB_URI = "mysql://root:jabcpo@localhost/event_moderator"
#DB_POOL_SIZE = 10
#DB_MIGRATE = True
#DB_FAKE_MIGRATE = False  # maybe?

# location where static files are stored:

# location where to store uploaded files:
UPLOAD_FOLDER = os.path.join(APP_FOLDER, "uploads")
UPLOAD_PATH = os.path.join(APP_FOLDER, "static/images")

DOWNLOAD_FOLDER = os.path.join(APP_FOLDER, "downloads")

# send email on regstration
VERIFY_EMAIL = True

# account requires to be approved ?
REQUIRES_APPROVAL = False

# ALLOWED_ACTIONS:
# ["all"] 
# ["login", "logout", "request_reset_password", "reset_password", "change_password", "change_email", "update_profile"]
# if you add "login", add also "logout"
ALLOWED_ACTIONS = ["all"]


# email settings
SMTP_SSL = False
SMTP_SERVER = None
SMTP_SENDER = "you@example.com"
SMTP_LOGIN = "username:password"
SMTP_TLS = False

# session settings
SESSION_TYPE = "cookies"
SESSION_SECRET_KEY = "<session-secret-key>" # replace this with a uuid
MEMCACHE_CLIENTS = ["127.0.0.1:11211"]
REDIS_SERVER = "localhost:6379"

# logger settings
LOGGERS = [
    "warning:stdout"
]  # syntax "severity:filename" filename can be stderr or stdout

# Disable default login when using OAuth
DEFAULT_LOGIN_ENABLED = True

# single sign on Google (will be used if provided)
OAUTH2GOOGLE_CLIENT_ID = None
OAUTH2GOOGLE_CLIENT_SECRET = None

# single sign on Okta (will be used if provided. Please also add your tenant
# name to py4web/utils/auth_plugins/oauth2okta.py. You can replace the XXX
# instances with your tenant name.)
OAUTH2OKTA_CLIENT_ID = None
OAUTH2OKTA_CLIENT_SECRET = None

# single sign on Google (will be used if provided)
OAUTH2FACEBOOK_CLIENT_ID = None
OAUTH2FACEBOOK_CLIENT_SECRET = None

# enable PAM
USE_PAM = False

# enable LDAP
USE_LDAP = False
LDAP_SETTINGS = {
    "mode": "ad",
    "server": "my.domain.controller",
    "base_dn": "ou=Users,dc=domain,dc=com",
}

# Celery settings
USE_CELERY = False
CELERY_BROKER = "redis://localhost:6379/0"

# try import private settings
'''try:
    from .settings_private import *
except (ImportError, ModuleNotFoundError):
    pass'''
