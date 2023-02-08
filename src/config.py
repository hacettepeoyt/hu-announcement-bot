# Telegram Bot Token
TELEGRAM_API_KEY: str = ''

# MongoDB Connection String
DB_STRING: str = ''

# Feedback Chat ID
FEEDBACK_CHAT_ID: int = 0

# Admin Chat ID
ADMIN_ID: int = 0

# Logger Chat ID
LOGGER_CHAT_ID: int = 0

# Default Department List
DEFAULT_DEPS: list[str] = []

# Time Configurations for the Announcement Checking Task (in seconds)
ANNOUNCEMENT_CHECK_INTERVAL: int = 0
ANNOUNCEMENT_CHECK_FIRST: int = 0

# Polling or Webhook?
WEBHOOK_CONNECTED: bool = False
PORT: str = ''
WEBHOOK_URL: str = '' + TELEGRAM_API_KEY
