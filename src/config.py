import sys

import toml

config_path = sys.argv[1] if len(sys.argv) > 1 else "config.toml"
config = toml.load(config_path)

# Telegram Bot Token
TELEGRAM_API_KEY: str = config["TELEGRAM_API_KEY"]

# MongoDB Connection String
DB_STRING: str = config["DB_STRING"]

# Feedback Chat ID
FEEDBACK_CHAT_ID: int = config["FEEDBACK_CHAT_ID"]

# Admin Chat ID
ADMIN_ID: int = config["ADMIN_ID"]

# Logger Chat ID
LOGGER_CHAT_ID: int = config["LOGGER_CHAT_ID"]

# Default Department List
DEFAULT_DEPS: list[str] = config["DEFAULT_DEPS"]

# Time Configurations for the Announcement Checking Task (in seconds)
ANNOUNCEMENT_CHECK_INTERVAL: int = config["ANNOUNCEMENT_CHECK_INTERVAL"]
ANNOUNCEMENT_CHECK_FIRST: int = config["ANNOUNCEMENT_CHECK_FIRST"]

# Polling or Webhook?
WEBHOOK_CONNECTED: bool = config["WEBHOOK_CONNECTED"]
PORT: str = config["PORT"]
WEBHOOK_URL: str = config["WEBHOOK_URL"]
