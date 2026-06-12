import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from fetch_data import get_top_artists, get_top_tracks, get_recently_played

os.makedirs("charts", exist_ok=True)

plt.rcParams.update({
    "figure.facecolor": "#0d0d0d",
    "axes.facecolor": "#0d0d0d",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#cccccc",
    "xtick.color": "#888888",
    "ytick.color": "#888888",
    "text.color": "#cccccc",
    "grid.color": "#1a1a1a",
    "grid.linestyle": "--",
    "font.family": "monospace",
})

SPOTIFY_GREEN = "#1DB954"
ACCENT = "#ffffff"


def plot_top_artists(df):
    if df is None or df.empty:
        print("  Top artists: no data yet.")
        return

    df_plot = df.head(10).iloc[::-1].copy()
    df_plot["score"] = range(1, len(df_plot) + 1)

    n = len(df_plot)
    fig_height = max(4, n * 0.6)
    fig, ax = plt.subplots(figsize=(13, fig_height))
    fig.patch.set_facecolor("#0d0d0d")

    colors = [SPOTIFY_GREEN] * n
    colors[-1] = "#ffffff"

    bars = ax.barh(
        df_plot["name"],
        df_plot["score"],
        color=colors,
        edgecolor="none",
        height=0.4,
    )

    for i, bar in enumerate(bars):
        width = bar.get_width()
        rank = n - i
        ax.text(
            width + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"#{rank}",
            va="center",
            fontsize=10,
            color="#888888",
        )

    ax.set_title("Your Top Artists", fontsize=20, fontweight="bold",
                 color=ACCENT, pad=20)
    ax.set_xlim(0, 13)
    ax.xaxis.set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", labelsize=12)

    plt.tight_layout()
    plt.savefig("charts/top_artists.png", dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print("  Saved: charts/top_artists.png")
    plt.show()


def plot_top_tracks(df):
    if df is None or df.empty:
        print("  Top tracks: no data yet.")
        return

    df_plot = df.head(10).iloc[::-1].copy()
    df_plot["score"] = range(1, len(df_plot) + 1)
    df_plot["label"] = df_plot["name"] + "  —  " + df_plot["artist"]

    n = len(df_plot)
    fig_height = max(4, n * 0.7)
    fig, ax = plt.subplots(figsize=(13, fig_height))
    fig.patch.set_facecolor("#0d0d0d")

    colors = [SPOTIFY_GREEN] * n
    colors[-1] = "#ffffff"

    bars = ax.barh(
        df_plot["label"],
        df_plot["score"],
        color=colors,
        edgecolor="none",
        height=0.4,
    )

    for i, bar in enumerate(bars):
        width = bar.get_width()
        rank = n - i
        ax.text(
            width + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"#{rank}",
            va="center",
            fontsize=10,
            color="#888888",
        )

    ax.set_title("Your Top Tracks", fontsize=20, fontweight="bold",
                 color=ACCENT, pad=20)
    ax.set_xlim(0, 13)
    ax.xaxis.set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", labelsize=10)

    plt.tight_layout()
    plt.savefig("charts/top_tracks.png", dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print("  Saved: charts/top_tracks.png")
    plt.show()


def plot_listening_hours(df):
    if df is None or df.empty:
        print("  Listening hours: no data yet.")
        return

    df = df.copy()
    df["hour"] = pd.to_datetime(
        df["played_at"], format="%b %d  %I:%M %p", errors="coerce"
    ).dt.hour

    if df["hour"].isna().all():
        df["hour"] = pd.to_datetime(
            df["played_at"], utc=True
        ).dt.tz_convert("America/New_York").dt.hour

    hour_counts = df["hour"].value_counts().reindex(range(24), fill_value=0)

    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor("#0d0d0d")

    colors = [SPOTIFY_GREEN if hour_counts[h] > 0 else "#1a1a1a" for h in range(24)]
    bars = ax.bar(range(24), hour_counts.values, color=colors, edgecolor="none", width=0.7)

    for bar in bars:
        if bar.get_height() > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.2,
                str(int(bar.get_height())),
                ha="center", va="bottom",
                fontsize=9, color="#888888",
            )

    time_labels = []
    for h in range(24):
        if h == 0:
            time_labels.append("12 AM")
        elif h < 12:
            time_labels.append(f"{h} AM")
        elif h == 12:
            time_labels.append("12 PM")
        else:
            time_labels.append(f"{h - 12} PM")

    ax.set_xticks(range(24))
    ax.set_xticklabels(time_labels, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Tracks Played", fontsize=11, labelpad=10)
    ax.set_title("When Do You Listen to Music?", fontsize=20,
                 fontweight="bold", color=ACCENT, pad=20)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True)

    peak_hour = hour_counts.idxmax()
    peak_label = time_labels[peak_hour]
    ax.text(0.75, 0.95, f"Peak: {peak_label}",
            transform=ax.transAxes, fontsize=10,
            ha="right", va="top", color=SPOTIFY_GREEN)

    plt.tight_layout()
    plt.savefig("charts/listening_hours.png", dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print("  Saved: charts/listening_hours.png")
    plt.show()


def plot_most_played_artists(df):
    if df is None or df.empty:
        print("  Most played artists: no data yet.")
        return

    artist_counts = (
        df["artist"]
        .str.split(",")
        .str[0]
        .str.strip()
        .value_counts()
        .head(8)
    )

    n = len(artist_counts)
    fig_height = max(4, n * 0.7)
    fig, ax = plt.subplots(figsize=(13, fig_height))
    fig.patch.set_facecolor("#0d0d0d")

    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.85, n))[::-1]
    bars = ax.barh(
        artist_counts.index[::-1],
        artist_counts.values[::-1],
        color=colors[::-1],
        edgecolor="none",
        height=0.4,
    )

    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)} plays",
            va="center", fontsize=10, color="#888888",
        )

    ax.set_title("Most Played Artists Recently", fontsize=20,
                 fontweight="bold", color=ACCENT, pad=20)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis="y", labelsize=12)

    plt.tight_layout()
    plt.savefig("charts/most_played_artists.png", dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print("  Saved: charts/most_played_artists.png")
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
    plot_top_tracks(top_tracks)
    plot_listening_hours(recently_played)
    plot_most_played_artists(recently_played)

    print()
    print("  Done. Charts saved to /charts")