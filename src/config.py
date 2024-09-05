import sys

import toml

config_path = sys.argv[1] if len(sys.argv) > 1 else "config.toml"
config = toml.load(config_path)

# Telegram Bot Token
TELEGRAM_API_KEY: str = config["TELEGRAM_API_KEY"]

# Database configurations
DB_STRING: str = config["DB_STRING"]
DB_NAME: str = config["DB_NAME"]

# Admin Chat ID
ADMIN_ID: int = config["ADMIN_ID"]

# Feedback Chat ID
FEEDBACK_CHAT_ID: int = config.get("FEEDBACK_CHAT_ID", ADMIN_ID)

# Logger Chat ID
LOGGER_CHAT_ID: int = config.get("LOGGER_CHAT_ID", ADMIN_ID)

# Default Department List
DEFAULT_DEPS: list[str] = config.get("DEFAULT_DEPS", [])

# Time Configurations for the Announcement Checking Task (in seconds)
ANNOUNCEMENT_CHECK_INTERVAL: int = config.get("ANNOUNCEMENT_CHECK_INTERVAL", 1800)
ANNOUNCEMENT_CHECK_FIRST: int = config.get("ANNOUNCEMENT_CHECK_FIRST", 5)

# Polling or Webhook?
WEBHOOK_CONNECTED: bool = config.get("WEBHOOK_CONNECTED", False)
PORT: int = config.get("PORT", 31415)
WEBHOOK_URL: str = config.get("WEBHOOK_URL", "") + "/" + TELEGRAM_API_KEY

# Conversation timeout values
FEEDBACK_TIMEOUT: int = config.get("FEEDBACK_TIMEOUT", 300)
ADMIN_ANNOUNCEMENT_TIMEOUT: int = config.get("ADMIN_ANNOUNCEMENT_TIMEOUT", 300)
ADD_TIMEOUT: int = config.get("ADD_TIMEOUT", 60)
REMOVE_TIMEOUT: int = config.get("REMOVE_TIMEOUT", 60)

# Default language
DEFAULT_LANGUAGE: str = config.get("DEFAULT_LANGUAGE", "en")
