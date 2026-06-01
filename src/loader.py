import os
import json
import pandas as pd
from src.config import DATA_PATH, MONGO_URI, MONGO_DB


class SlackDataLoader:
    """Loads Slack message data from local JSON files or MongoDB Atlas."""

    def __init__(self, data_path: str = DATA_PATH, source: str = "auto"):
        self.data_path = data_path
        # "auto" uses Atlas if MONGO_URI is set, otherwise falls back to local files
        if source == "auto":
            self.source = "mongo" if MONGO_URI else "local"
        else:
            self.source = source

    def get_channels(self) -> list:
        """Return list of available channel names."""
        if self.source == "mongo":
            return self._get_channels_mongo()
        return [
            d for d in os.listdir(self.data_path)
            if os.path.isdir(os.path.join(self.data_path, d))
        ]

    def load_channel(self, channel: str) -> pd.DataFrame:
        """Load all messages from a single channel into a DataFrame."""
        if self.source == "mongo":
            return self._load_channel_mongo(channel)
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
        if self.source == "mongo":
            return self._load_all_mongo()
        frames = []
        for channel in self.get_channels():
            df = self.load_channel(channel)
            if not df.empty:
                frames.append(df)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    def _get_mongo_client(self):
        from pymongo import MongoClient
        return MongoClient(MONGO_URI)

    def _get_channels_mongo(self) -> list:
        client = self._get_mongo_client()
        channels = client[MONGO_DB]["messages"].distinct("channel")
        client.close()
        return sorted(channels)

    def _load_channel_mongo(self, channel: str) -> pd.DataFrame:
        client = self._get_mongo_client()
        docs = list(client[MONGO_DB]["messages"].find(
            {"channel": channel}, {"_id": 0}
        ))
        client.close()
        return pd.DataFrame(docs)

    def _load_all_mongo(self) -> pd.DataFrame:
        client = self._get_mongo_client()
        docs = list(client[MONGO_DB]["messages"].find({}, {"_id": 0}))
        client.close()
        return pd.DataFrame(docs) if docs else pd.DataFrame()
