import pandas as pd


def get_top_users(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    """Return top n users by a given count column."""
    return df.groupby("user")[column].sum().nlargest(n).reset_index()


def get_bottom_users(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    """Return bottom n users by a given count column."""
    return df.groupby("user")[column].sum().nsmallest(n).reset_index()


def parse_timestamp(ts: str) -> pd.Timestamp:
    """Convert a Slack Unix timestamp string to a pandas Timestamp."""
    return pd.to_datetime(float(ts), unit="s")


def add_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add datetime, date, and hour columns from the Slack 'ts' field."""
    df = df.copy()
    df["datetime"] = df["ts"].apply(parse_timestamp)
    df["date"] = df["datetime"].dt.date
    df["hour"] = df["datetime"].dt.hour
    return df
