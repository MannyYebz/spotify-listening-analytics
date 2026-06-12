import requests
import pandas as pd
from auth import get_valid_token

BASE_URL = "https://api.spotify.com/v1"


def get_headers():
    token = get_valid_token()
    return {
        "Authorization": f"Bearer {token}"
    }


def print_header(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_table(df, columns, col_widths):
    header = "  ".join(f"{col:<{col_widths[i]}}" for i, col in enumerate(columns))
    print(header)
    print("-" * len(header))
    for _, row in df.iterrows():
        line = "  ".join(
            f"{str(row[col])[:col_widths[i]]:<{col_widths[i]}}"
            for i, col in enumerate(columns)
        )
        print(line)


def get_user_profile():
    url = f"{BASE_URL}/me"
    response = requests.get(url, headers=get_headers())

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.json()}")
        return None

    data = response.json()

    print_header("YOUR SPOTIFY PROFILE")
    print(f"  Name         : {data.get('display_name', 'Unknown')}")
    print(f"  Account Type : {data.get('product', 'unknown').title()}")
    print(f"  Followers    : {data.get('followers', {}).get('total', 0)}")
    print()
    return data


def get_top_artists(time_range="medium_term", limit=20):
    url = f"{BASE_URL}/me/top/artists"
    params = {
        "time_range": time_range,
        "limit": limit,
    }

    response = requests.get(url, headers=get_headers(), params=params)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.json()}")
        return None

    data = response.json()
    label = time_range.replace("_", " ").title()
    print_header(f"TOP ARTISTS ({label})")

    if not data.get("items"):
        print("  No data yet. Listen to more music and try again.")
        print()
        return pd.DataFrame()

    artists = []
    for i, artist in enumerate(data["items"]):
        artists.append({
            "rank": i + 1,
            "name": artist.get("name", "Unknown"),
            "genres": ", ".join(artist.get("genres", [])[:2]) if artist.get("genres") else "N/A",
            "popularity": artist.get("popularity", 0),
            "followers": f"{artist.get('followers', {}).get('total', 0):,}",
        })

    df = pd.DataFrame(artists)
    print_table(df, ["rank", "name", "genres", "popularity"], [4, 25, 30, 10])
    print()
    return df


def get_top_tracks(time_range="medium_term", limit=20):
    url = f"{BASE_URL}/me/top/tracks"
    params = {
        "time_range": time_range,
        "limit": limit,
    }

    response = requests.get(url, headers=get_headers(), params=params)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.json()}")
        return None

    data = response.json()
    label = time_range.replace("_", " ").title()
    print_header(f"TOP TRACKS ({label})")

    if not data.get("items"):
        print("  No data yet. Listen to more music and try again.")
        print()
        return pd.DataFrame()

    tracks = []
    for i, track in enumerate(data["items"]):
        tracks.append({
            "rank": i + 1,
            "name": track.get("name", "Unknown"),
            "artist": ", ".join([a.get("name", "Unknown") for a in track.get("artists", [])]),
            "album": track.get("album", {}).get("name", "Unknown"),
            "popularity": track.get("popularity", 0),
            "duration_min": round(track.get("duration_ms", 0) / 60000, 2),
            "track_id": track.get("id", ""),
        })

    df = pd.DataFrame(tracks)
    print_table(df, ["rank", "name", "artist", "popularity"], [4, 30, 25, 10])
    print()
    return df


def get_recently_played(limit=50):
    url = f"{BASE_URL}/me/player/recently-played"
    params = {"limit": limit}

    response = requests.get(url, headers=get_headers(), params=params)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.json()}")
        return None

    data = response.json()
    print_header("RECENTLY PLAYED")

    if not data.get("items"):
        print("  No listening history found yet.")
        print()
        return pd.DataFrame()

    tracks = []
    for item in data["items"]:
        track = item.get("track", {})
        tracks.append({
            "played_at": item.get("played_at", ""),
            "name": track.get("name", "Unknown"),
            "artist": ", ".join([a.get("name", "Unknown") for a in track.get("artists", [])]),
            "album": track.get("album", {}).get("name", "Unknown"),
            "duration_min": round(track.get("duration_ms", 0) / 60000, 2),
            "track_id": track.get("id", ""),
        })

    df = pd.DataFrame(tracks)
    df["played_at"] = (
    pd.to_datetime(df["played_at"]).dt.tz_convert("America/New_York").dt.strftime("%b %d  %I:%M %p"))
    print_table(df.head(10), ["played_at", "name", "artist"], [16, 30, 25])
    print()
    return df


if __name__ == "__main__":
    print()
    print("  SPOTIFY LISTENING PROFILE DASHBOARD")
    print("  ====================================")

    get_user_profile()
    get_top_artists("short_term", 20)
    get_top_tracks("short_term", 20)
    get_recently_played(50)