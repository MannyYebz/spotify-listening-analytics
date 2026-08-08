from fetch_data import get_user_profile, get_top_artists, get_top_tracks, get_recently_played
from analyze import plot_top_artists, plot_top_tracks, plot_listening_hours, plot_most_played_artists
from analytics_history import (
    HISTORY_DIR,
    RECENT_HISTORY_DIR,
    all_time_top_artists,
    all_time_top_tracks,
    save_recent_listening_history,
    update_listening_history,
)


def main():
    print()
    print("  SPOTIFY LISTENING PROFILE DASHBOARD")
    print("  ====================================")

    # Step 1: Fetch all data
    get_user_profile()
    top_artists = get_top_artists("short_term", 20)
    top_tracks = get_top_tracks("short_term", 20)
    recently_played = get_recently_played(50)

    # Refresh the latest snapshot and keep the cumulative all-time history.
    save_recent_listening_history(recently_played)
    # Add only new plays to the cumulative history used by all-time charts.
    listening_history = update_listening_history(recently_played)

    # Step 2: Generate charts
    print()
    print("  Generating charts...")
    print()

    # Keep the newest charts together with the recent-listening CSV.
    plot_top_artists(top_artists, RECENT_HISTORY_DIR / "top_artists.png")
    plot_top_tracks(top_tracks, RECENT_HISTORY_DIR / "top_tracks.png")
    plot_listening_hours(recently_played, RECENT_HISTORY_DIR / "listening_hours.png")
    plot_most_played_artists(
        recently_played, RECENT_HISTORY_DIR / "most_played_artists.png"
    )

    # Generate the archived charts from every play collected so far.
    plot_top_artists(
        all_time_top_artists(listening_history),
        HISTORY_DIR / "all_time_top_artists.png",
        "Your All-Time Top Artists",
    )
    plot_top_tracks(
        all_time_top_tracks(listening_history),
        HISTORY_DIR / "all_time_top_tracks.png",
        "Your All-Time Top Tracks",
    )
    plot_listening_hours(
        listening_history,
        HISTORY_DIR / "all_time_listening_hours.png",
        "Your All-Time Listening Hours",
    )
    plot_most_played_artists(
        listening_history,
        HISTORY_DIR / "all_time_most_played_artists.png",
        "Your Most Played Artists — All Time",
    )

    print()
    print("  Done. Recent results saved to /recent_history; all-time analytics saved to /analytics_history")


if __name__ == "__main__":
    main()
