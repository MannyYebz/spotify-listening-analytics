from pathlib import Path
import json

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


def import_extended_streaming_history(export_dir):
    """Load Spotify's extracted extended-history JSON files into the history CSV."""
    export_dir = Path(export_dir)
    json_files = sorted(export_dir.glob("Streaming_History_*.json"))
    if not json_files:
        print(f"  Extended history: no JSON files found in {export_dir}")
        return pd.DataFrame(columns=HISTORY_COLUMNS)

    plays = []
    for json_file in json_files:
        with json_file.open(encoding="utf-8") as file:
            records = json.load(file)

        for record in records:
            track_uri = record.get("spotify_track_uri") or ""
            track_name = record.get("master_metadata_track_name")
            if not track_name or not track_uri.startswith("spotify:track:"):
                continue

            plays.append(
                {
                    "played_at": record.get("ts", ""),
                    "name": track_name,
                    "artist": record.get("master_metadata_album_artist_name") or "Unknown",
                    "album": record.get("master_metadata_album_album_name") or "Unknown",
                    "duration_min": round((record.get("ms_played") or 0) / 60000, 2),
                    "track_id": track_uri.removeprefix("spotify:track:"),
                }
            )

    imported = pd.DataFrame(plays, columns=HISTORY_COLUMNS)
    print(f"  Loaded: {len(imported)} plays from Spotify extended history")
    return imported


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


def update_listening_history(recently_played, imported_history=None):
    """Add newly fetched plays to the cumulative CSV and return all saved plays."""
    HISTORY_DIR.mkdir(exist_ok=True)

    if HISTORY_CSV.exists():
        history = pd.read_csv(HISTORY_CSV)
    else:
        history = pd.DataFrame(columns=HISTORY_COLUMNS)

    additions = []
    if imported_history is not None and not imported_history.empty:
        additions.append(imported_history.copy())
    if recently_played is not None and not recently_played.empty:
        additions.append(recently_played.copy())

    if additions:
        new_rows = pd.concat(additions, ignore_index=True)
        if "played_at_utc" in new_rows.columns:
            new_rows["played_at"] = new_rows["played_at_utc"].fillna(
                new_rows["played_at"]
            )

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


def print_listening_history(history, title, limit=10):
    """Print a compact, newest-first view of a listening-history DataFrame."""
    print()
    print("=" * 82)
    play_count = 0 if history is None else len(history)
    print(f"  {title} ({play_count} plays)")
    print("=" * 82)

    if history is None or history.empty:
        print("  No listening history found.")
        return

    display = history.copy().sort_values("played_at", ascending=False).head(limit)
    timestamps = pd.to_datetime(display["played_at"], utc=True, errors="coerce")
    display["played_at"] = timestamps.dt.tz_convert("America/New_York").dt.strftime(
        "%b %d  %I:%M %p"
    )
    header = f"{'PLAYED AT':<18}  {'TRACK':<34}  {'ARTIST':<26}"
    print(header)
    print("-" * len(header))
    for _, row in display.iterrows():
        print(
            f"{str(row['played_at']):<18}  "
            f"{str(row['name'])[:34]:<34}  "
            f"{str(row['artist'])[:26]:<26}"
        )


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
