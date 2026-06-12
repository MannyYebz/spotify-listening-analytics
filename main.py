from fetch_data import get_user_profile, get_top_artists, get_top_tracks, get_recently_played
from analyze import plot_top_artists, plot_top_tracks, plot_listening_hours, plot_most_played_artists


def main():
    print()
    print("  SPOTIFY LISTENING PROFILE DASHBOARD")
    print("  ====================================")

    # Step 1: Fetch all data
    get_user_profile()
    top_artists = get_top_artists("short_term", 20)
    top_tracks = get_top_tracks("short_term", 20)
    recently_played = get_recently_played(50)

    # Step 2: Generate charts
    print()
    print("  Generating charts...")
    print()

    plot_top_artists(top_artists)
    plot_top_tracks(top_tracks)
    plot_listening_hours(recently_played)
    plot_most_played_artists(recently_played)

    print()
    print("  Done. Charts saved to /charts")


if __name__ == "__main__":
    main()