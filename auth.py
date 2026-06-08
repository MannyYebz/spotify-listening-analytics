import os
import json
import time
import base64
import urllib.parse
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
TOKEN_CACHE = ".token_cache.json"

SCOPES = [
    "user-top-read",
    "user-read-recently-played",
    "user-read-private",
]


def get_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
    }
    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"


def exchange_code_for_token(code):
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

    token_data = response.json()
    token_data["obtained_at"] = time.time()

    with open(TOKEN_CACHE, "w") as f:
        json.dump(token_data, f, indent=2)

    print("Token obtained and cached!")
    return token_data


def refresh_access_token(refresh_token):
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code != 200:
        print(f"Error refreshing: {response.status_code}")
        return None

    token_data = response.json()
    token_data["obtained_at"] = time.time()

    if "refresh_token" not in token_data:
        token_data["refresh_token"] = refresh_token

    with open(TOKEN_CACHE, "w") as f:
        json.dump(token_data, f, indent=2)

    return token_data


def get_valid_token():
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, "r") as f:
            token_data = json.load(f)

        elapsed = time.time() - token_data["obtained_at"]
        if elapsed < token_data.get("expires_in", 3600) - 60:
            return token_data["access_token"]
        else:
            print("Token expired, refreshing...")
            new_data = refresh_access_token(token_data["refresh_token"])
            if new_data:
                return new_data["access_token"]

    return run_auth_flow()


def run_auth_flow():
    url = get_auth_url()

    print("\n" + "=" * 60)
    print("SPOTIFY AUTHORIZATION")
    print("=" * 60)
    print("\n1. Open this URL in your browser:\n")
    print(url)
    print("\n2. Log in and click Agree")
    print("3. You'll be redirected to a page that won't load.")
    print("   That's fine. Copy the ENTIRE URL from the address bar.")
    print()

    redirect_response = input("4. Paste the full redirect URL here: ").strip()

    parsed = urllib.parse.urlparse(redirect_response)
    params = urllib.parse.parse_qs(parsed.query)

    if "code" not in params:
        print("Error: no authorization code found.")
        return None

    code = params["code"][0]
    print(f"\nCode received! (starts with: {code[:10]}...)")

    token_data = exchange_code_for_token(code)
    if token_data:
        return token_data["access_token"]
    return None


if __name__ == "__main__":
    token = get_valid_token()
    if token:
        print(f"\nSuccess! Token: {token[:20]}...")
    else:
        print("Authentication failed.")