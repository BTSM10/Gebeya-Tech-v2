import os

# Path to the anonymized Slack data (not tracked by git)
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "anonymized")

# MongoDB Atlas connection string — set via environment variable
MONGO_URI = os.environ.get("MONGO_URI", "")
MONGO_DB = "gebeya_slack"
