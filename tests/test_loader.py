import pandas as pd
import pytest
from src.loader import SlackDataLoader


EXPECTED_COLUMNS = {"type", "user", "text", "ts", "channel"}


def test_load_channel_returns_dataframe():
    loader = SlackDataLoader()
    channels = loader.get_channels()
    assert len(channels) > 0, "No channels found"
    df = loader.load_channel(channels[0])
    assert isinstance(df, pd.DataFrame)


def test_load_channel_has_expected_columns():
    loader = SlackDataLoader()
    channels = loader.get_channels()
    df = loader.load_channel(channels[0])
    missing = EXPECTED_COLUMNS - set(df.columns)
    assert not missing, f"Missing columns: {missing}"


def test_load_all_channels_returns_dataframe():
    loader = SlackDataLoader()
    df = loader.load_all_channels()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_load_all_channels_has_expected_columns():
    loader = SlackDataLoader()
    df = loader.load_all_channels()
    missing = EXPECTED_COLUMNS - set(df.columns)
    assert not missing, f"Missing columns: {missing}"


def test_channel_column_matches_channel_name():
    loader = SlackDataLoader()
    channels = loader.get_channels()
    channel = channels[0]
    df = loader.load_channel(channel)
    assert (df["channel"] == channel).all()
