import requests
import pandas as pd
from auth import get_valid_token

BASE_URL = "https://api.spotify.com/v1"


def get_headers():
    token = get_valid_token()
    return {
        "Authorization": f"Bearer {token}"
    }


def get_user_profile():
    url = f"{BASE_URL}/me"
    response = requests.get(url, headers=get_headers())

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.json()}")
        return None

    data = response.json()
    print(f"Logged in as: {data['display_name']}")
    print(f"Account type: {data.get('product', 'unknown')}")
    print(f"Followers: {data.get('followers', {}).get('total', 0)}")
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

    if not data["items"]:
        print(f"\nTop Artists ({time_range}): No data yet. Listen to more music and try again.")
        return pd.DataFrame()

    artists = []
    for i, artist in enumerate(data["items"]):
        artists.append({
            "rank": i + 1,
            "name": artist["name"],
            "genres": ", ".join(artist["genres"]) if artist["genres"] else "N/A",
            "popularity": artist["popularity"],
            "followers": artist["followers"]["total"],
        })

    df = pd.DataFrame(artists)
    print(f"\nTop {len(df)} Artists ({time_range}):")
    print(df[["rank", "name", "genres", "popularity"]].to_string(index=False))
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

    if not data["items"]:
        print(f"\nTop Tracks ({time_range}): No data yet. Listen to more music and try again.")
        return pd.DataFrame()

    tracks = []
    for i, track in enumerate(data["items"]):
        tracks.append({
            "rank": i + 1,
            "name": track["name"],
            "artist": ", ".join([a["name"] for a in track["artists"]]),
            "album": track["album"]["name"],
            "popularity": track["popularity"],
            "duration_min": round(track["duration_ms"] / 60000, 2),
            "track_id": track["id"],
        })

    df = pd.DataFrame(tracks)
    print(f"\nTop {len(df)} Tracks ({time_range}):")
    print(df[["rank", "name", "artist", "popularity"]].to_string(index=False))
    return df


def get_recently_played(limit=50):
    url = f"{BASE_URL}/me/player/recently-played"
    params = {"limit": limit}

    response = requests.get(url, headers=get_headers(), params=params)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.json()}")
        return None

    data = response.json()

    if not data["items"]:
        print("\nRecently Played: No listening history found yet.")
        return pd.DataFrame()

    tracks = []
    for item in data["items"]:
        track = item["track"]
        tracks.append({
            "played_at": item["played_at"],
            "name": track["name"],
            "artist": ", ".join([a["name"] for a in track["artists"]]),
            "album": track["album"]["name"],
            "duration_min": round(track["duration_ms"] / 60000, 2),
            "track_id": track["id"],
        })

    df = pd.DataFrame(tracks)
    df["played_at"] = pd.to_datetime(df["played_at"])
    print(f"\nLast {len(df)} Recently Played Tracks:")
    print(df[["played_at", "name", "artist"]].head(10).to_string(index=False))
    return df


if __name__ == "__main__":
    print("=" * 50)
    print("FETCHING YOUR SPOTIFY DATA")
    print("=" * 50)

    get_user_profile()
    get_top_artists("short_term", 20)
    get_top_tracks("short_term", 20)
    get_recently_played(50)