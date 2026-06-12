import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from fetch_data import get_top_artists, get_top_tracks, get_recently_played

os.makedirs("charts", exist_ok=True)


def plot_top_artists(df):
    if df is None or df.empty:
        print("  Top artists: no data yet.")
        return

    fig, ax = plt.subplots(figsize=(12, 8))
    df_plot = df.head(10).iloc[::-1]

    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(df_plot)))
    bars = ax.barh(df_plot["name"], df_plot["popularity"], color=colors, edgecolor="white")

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{int(width)}", va="center", fontsize=9)

    ax.set_xlabel("Popularity Score (0-100)", fontsize=11)
    ax.set_title("Your Top 10 Artists", fontsize=16, fontweight="bold", pad=15)
    ax.set_xlim(0, 108)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig("charts/top_artists.png", dpi=150, bbox_inches="tight")
    print("  Saved: charts/top_artists.png")
    plt.show()


def plot_genre_distribution(df):
    if df is None or df.empty:
        print("  Genre distribution: no data yet.")
        return

    all_genres = []
    for genres_str in df["genres"]:
        if genres_str and genres_str != "N/A":
            for genre in genres_str.split(", "):
                all_genres.append(genre.strip())

    if not all_genres:
        print("  Genre distribution: no genre data found.")
        return

    genre_counts = pd.Series(all_genres).value_counts().head(8)

    fig, ax = plt.subplots(figsize=(9, 9))
    colors = plt.cm.Set3(np.linspace(0, 1, len(genre_counts)))

    wedges, texts, autotexts = ax.pie(
        genre_counts.values,
        labels=genre_counts.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        pctdistance=0.82,
    )

    for text in texts:
        text.set_fontsize(11)
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight("bold")

    ax.set_title("Your Genre Distribution", fontsize=16, fontweight="bold", pad=20)
    plt.tight_layout()
    plt.savefig("charts/genre_distribution.png", dpi=150, bbox_inches="tight")
    print("  Saved: charts/genre_distribution.png")
    plt.show()


def plot_listening_hours(df):
    if df is None or df.empty:
        print("  Listening hours: no data yet.")
        return

    df = df.copy()
    df["hour"] = pd.to_datetime(df["played_at"]).dt.hour
    hour_counts = df["hour"].value_counts().reindex(range(24), fill_value=0)

    fig, ax = plt.subplots(figsize=(13, 5))
    colors = ["#1DB954" if hour_counts[h] > 0 else "#e0e0e0" for h in range(24)]
    ax.bar(range(24), hour_counts.values, color=colors, edgecolor="white")

    ax.set_xticks(range(24))
    ax.set_xticklabels([f"{h}:00" for h in range(24)], rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Tracks Played", fontsize=11)
    ax.set_title("When Do You Listen to Music?", fontsize=16, fontweight="bold", pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig("charts/listening_hours.png", dpi=150, bbox_inches="tight")
    print("  Saved: charts/listening_hours.png")
    plt.show()


def plot_popularity_distribution(df):
    if df is None or df.empty:
        print("  Popularity distribution: no data yet.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["popularity"], bins=15, color="#1DB954", edgecolor="white", alpha=0.9)
    ax.axvline(df["popularity"].mean(), color="#ff4444", linestyle="--", linewidth=1.5,
               label=f"Average: {df['popularity'].mean():.0f}")

    ax.set_xlabel("Popularity Score (0-100)", fontsize=11)
    ax.set_ylabel("Number of Tracks", fontsize=11)
    ax.set_title("Track Popularity Distribution", fontsize=16, fontweight="bold", pad=15)
    ax.legend(fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    avg = df["popularity"].mean()
    if avg > 70:
        taste = "You listen to mostly mainstream music"
    elif avg > 45:
        taste = "Your taste is a mix of mainstream and underground"
    else:
        taste = "You lean toward underground and niche music"

    ax.text(0.98, 0.95, taste, transform=ax.transAxes,
            fontsize=9, ha="right", va="top", color="#666666", style="italic")

    plt.tight_layout()
    plt.savefig("charts/popularity_distribution.png", dpi=150, bbox_inches="tight")
    print("  Saved: charts/popularity_distribution.png")
    plt.show()


if __name__ == "__main__":
    print()
    print("  SPOTIFY LISTENING PROFILE - ANALYSIS")
    print("  ======================================")
    print()

    top_artists = get_top_artists("short_term", 20)
    top_tracks = get_top_tracks("short_term", 20)
    recently_played = get_recently_played(50)

    print()
    print("  Generating charts...")
    print()

    plot_top_artists(top_artists)
    plot_genre_distribution(top_artists)
    plot_listening_hours(recently_played)
    plot_popularity_distribution(top_tracks)

    print()
    print("  Done. Charts saved to /charts")