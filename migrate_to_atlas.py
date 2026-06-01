"""Load Slack JSON data directly into MongoDB Atlas."""
import os
import json
import sys
from pymongo import MongoClient

ATLAS_URI = sys.argv[1] if len(sys.argv) > 1 else ""
DATA_PATH = os.path.join(os.path.dirname(__file__), "anonymized")
DB_NAME = "gebeya_slack"


def load_all_messages():
    messages, replies, reactions = [], [], []
    for channel in os.listdir(DATA_PATH):
        channel_path = os.path.join(DATA_PATH, channel)
        if not os.path.isdir(channel_path):
            continue
        for fname in os.listdir(channel_path):
            if not fname.endswith(".json"):
                continue
            with open(os.path.join(channel_path, fname)) as f:
                for msg in json.load(f):
                    msg["channel"] = channel
                    msg.pop("_id", None)

                    if msg.get("type") != "message":
                        continue

                    messages.append({
                        "channel": channel,
                        "type": msg.get("type", "message"),
                        "user": msg.get("user"),
                        "text": msg.get("text"),
                        "ts": msg.get("ts"),
                        "reply_count": msg.get("reply_count", 0),
                    })

                    for reply in msg.get("replies", []):
                        replies.append({
                            "channel": channel,
                            "parent_ts": msg.get("ts"),
                            "user": reply.get("user"),
                            "ts": reply.get("ts"),
                        })

                    for reaction in msg.get("reactions", []):
                        reactions.append({
                            "channel": channel,
                            "message_ts": msg.get("ts"),
                            "name": reaction.get("name"),
                            "count": reaction.get("count", 1),
                        })

    return messages, replies, reactions


def migrate():
    if not ATLAS_URI:
        print("Usage: python migrate_to_atlas.py <atlas_connection_string>")
        sys.exit(1)

    print("Loading data from JSON files...")
    messages, replies, reactions = load_all_messages()
    print(f"Found: {len(messages)} messages, {len(replies)} replies, {len(reactions)} reactions")

    print("Connecting to Atlas...")
    client = MongoClient(ATLAS_URI)
    db = client[DB_NAME]

    for col_name, docs in [("messages", messages), ("replies", replies), ("reactions", reactions)]:
        if docs:
            db[col_name].drop()
            db[col_name].insert_many(docs)
            print(f"{col_name}: inserted {len(docs)} documents")

    client.close()
    print("Migration complete.")


if __name__ == "__main__":
    migrate()
