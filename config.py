"""
Campus Buddy Bot - Configuration File
Branch: Yeshi_Dot-et
Developer: Yeshi
"""

# ===== BOT INFO =====
BOT_NAME = "Campus_Buddy"
BOT_VERSION = "1.0"
BOT_DEVELOPER = "Yeshi"
BOT_BRANCH = "Yeshi_Dot-et"

# ===== DATABASE =====
DB_NAME = "assignments.db"
DB_TABLE = "assignments"

# ===== PRIORITY LEVELS =====
PRIORITIES = {
    "high": "🔴 High",
    "medium": "🟡 Medium",
    "low": "🟢 Low",
}

# ===== STATUS OPTIONS =====
STATUS_OPTIONS = {
    "pending": "Pending",
    "completed": "Completed",
}

# ===== DATE FORMAT =====
DATE_FORMAT = "%Y-%m-%d"

# ===== DEFAULT VALUES =====
DEFAULT_SUBJECT = "General"
DEFAULT_PRIORITY = "medium"

# ===== LOGGING =====
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
