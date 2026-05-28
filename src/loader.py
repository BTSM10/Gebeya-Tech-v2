import os
import json
import pandas as pd
from src.config import DATA_PATH


class SlackDataLoader:
    """Loads Slack message data from the anonymized export directory."""

    def __init__(self, data_path: str = DATA_PATH):
        self.data_path = data_path

    def get_channels(self) -> list:
        """Return list of available channel names."""
        return [
            d for d in os.listdir(self.data_path)
            if os.path.isdir(os.path.join(self.data_path, d))
        ]

    def load_channel(self, channel: str) -> pd.DataFrame:
        """Load all messages from a single channel into a DataFrame."""
        channel_path = os.path.join(self.data_path, channel)
        records = []
        for fname in os.listdir(channel_path):
            if fname.endswith(".json"):
                with open(os.path.join(channel_path, fname), "r") as f:
                    messages = json.load(f)
                    for msg in messages:
                        msg["channel"] = channel
                        records.append(msg)
        return pd.DataFrame(records)

    def load_all_channels(self) -> pd.DataFrame:
        """Load all messages from all channels into a single DataFrame."""
        frames = []
        for channel in self.get_channels():
            df = self.load_channel(channel)
            if not df.empty:
                frames.append(df)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
