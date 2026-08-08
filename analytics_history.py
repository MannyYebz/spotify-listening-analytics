from pathlib import Path

import pandas as pd


HISTORY_DIR = Path("analytics_history")
HISTORY_CSV = HISTORY_DIR / "listening_history.csv"
RECENT_HISTORY_DIR = Path("recent_history")
RECENT_HISTORY_CSV = RECENT_HISTORY_DIR / "recent_listening_history.csv"
HISTORY_COLUMNS = [
    "played_at",
    "name",
    "artist",
    "album",
    "duration_min",
    "track_id",
]


def save_recent_listening_history(recently_played):
    """Replace the recent-history CSV with the latest Spotify snapshot."""
    RECENT_HISTORY_DIR.mkdir(exist_ok=True)

    if recently_played is None or recently_played.empty:
        recent_history = pd.DataFrame(columns=HISTORY_COLUMNS)
    else:
        recent_history = recently_played.copy()
        if "played_at_utc" in recent_history.columns:
            recent_history["played_at"] = recent_history["played_at_utc"]

        for column in HISTORY_COLUMNS:
            if column not in recent_history.columns:
                recent_history[column] = ""

        recent_history = recent_history[HISTORY_COLUMNS]

    recent_history.to_csv(RECENT_HISTORY_CSV, index=False)
    print(f"  Saved: {RECENT_HISTORY_CSV} ({len(recent_history)} recent plays)")
    return recent_history


def update_listening_history(recently_played):
    """Add newly fetched plays to the cumulative CSV and return all saved plays."""
    HISTORY_DIR.mkdir(exist_ok=True)

    if HISTORY_CSV.exists():
        history = pd.read_csv(HISTORY_CSV)
    else:
        history = pd.DataFrame(columns=HISTORY_COLUMNS)

    if recently_played is not None and not recently_played.empty:
        new_rows = recently_played.copy()
        if "played_at_utc" in new_rows.columns:
            new_rows["played_at"] = new_rows["played_at_utc"]

        for column in HISTORY_COLUMNS:
            if column not in new_rows.columns:
                new_rows[column] = ""

        history = pd.concat(
            [history, new_rows[HISTORY_COLUMNS]], ignore_index=True
        )
        history = history.drop_duplicates(
            subset=["played_at", "track_id"], keep="last"
        )
        history = history.sort_values("played_at", ascending=False)

    history.to_csv(HISTORY_CSV, index=False)
    print(f"  Updated: {HISTORY_CSV} ({len(history)} total plays)")
    return history


def all_time_top_artists(history, limit=20):
    if history is None or history.empty:
        return pd.DataFrame()

    return (
        history.assign(artist=history["artist"].str.split(",").str[0].str.strip())
        .groupby("artist", as_index=False)
        .size()
        .sort_values("size", ascending=False)
        .head(limit)
        .rename(columns={"artist": "name", "size": "play_count"})
    )


def all_time_top_tracks(history, limit=20):
    if history is None or history.empty:
        return pd.DataFrame()

    return (
        history.groupby(["track_id", "name", "artist"], as_index=False)
        .size()
        .sort_values("size", ascending=False)
        .head(limit)
        .rename(columns={"size": "play_count"})
    )
