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


def plot_top_artists(df, output_path="charts/top_artists.png", title="Your Top Artists"):
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

    ax.set_title(title, fontsize=20, fontweight="bold",
                 color=ACCENT, pad=20)
    ax.set_xlim(0, 13)
    ax.xaxis.set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", labelsize=12)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print(f"  Saved: {output_path}")
    plt.show()


def plot_top_tracks(df, output_path="charts/top_tracks.png", title="Your Top Tracks"):
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

    ax.set_title(title, fontsize=20, fontweight="bold",
                 color=ACCENT, pad=20)
    ax.set_xlim(0, 13)
    ax.xaxis.set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", labelsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print(f"  Saved: {output_path}")
    plt.show()


def plot_listening_hours(
    df,
    output_path="charts/listening_hours.png",
    title="When Do You Listen to Music?",
):
    if df is None or df.empty:
        print("  Listening hours: no data yet.")
        return

    df = df.copy()
    # Recent API data may use a local display value ("Aug 07  1:22 AM"),
    # while saved history uses ISO 8601. Spotify's ISO values can mix entries
    # with and without fractional seconds, so parse each value independently.
    df["hour"] = pd.to_datetime(
        df["played_at"], format="%b %d  %I:%M %p", errors="coerce"
    ).dt.hour
    missing_hours = df["hour"].isna()
    if missing_hours.any():
        iso_timestamps = pd.to_datetime(
            df.loc[missing_hours, "played_at"],
            format="mixed",
            utc=True,
            errors="coerce",
        )
        df.loc[missing_hours, "hour"] = (
            iso_timestamps.dt.tz_convert("America/New_York").dt.hour
        )

    if df["hour"].isna().all():
        print("  Listening hours: no valid timestamps found.")
        return

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
    ax.set_title(title, fontsize=20,
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
    plt.savefig(output_path, dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print(f"  Saved: {output_path}")
    plt.show()


def plot_time_of_day(
    df,
    output_path="charts/time_of_day.png",
    title="When Do You Listen Most?",
):
    """Plot listening time split across broad parts of the day."""
    if df is None or df.empty:
        print("  Time of day: no data yet.")
        return

    timestamp_column = "played_at_utc" if "played_at_utc" in df.columns else "played_at"
    timestamps = pd.to_datetime(df[timestamp_column], utc=True, errors="coerce")
    valid = timestamps.notna()
    if not valid.any():
        print("  Time of day: no valid timestamps found.")
        return

    local_hours = timestamps[valid].dt.tz_convert("America/New_York").dt.hour
    durations = pd.to_numeric(
        df.loc[valid, "duration_min"], errors="coerce"
    ).fillna(0)

    periods = pd.cut(
        local_hours,
        bins=[-1, 5, 11, 17, 21, 23],
        labels=["Late Night", "Morning", "Afternoon", "Evening", "Night"],
    )
    period_order = ["Morning", "Afternoon", "Evening", "Night", "Late Night"]
    listening_minutes = (
        durations.groupby(periods, observed=False).sum().reindex(period_order, fill_value=0)
    )
    total_minutes = listening_minutes.sum()
    percentages = (
        listening_minutes / total_minutes * 100
        if total_minutes > 0
        else listening_minutes
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor("#0d0d0d")
    colors = [SPOTIFY_GREEN if value == listening_minutes.max() else "#555555"
              for value in listening_minutes]
    bars = ax.bar(period_order, listening_minutes.values / 60, color=colors, width=0.65)

    for bar, percentage in zip(bars, percentages):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{bar.get_height():.1f} hrs\n{percentage:.1f}%",
            ha="center", va="bottom", fontsize=10, color="#cccccc",
        )

    peak_period = listening_minutes.idxmax()
    ax.set_title(title, fontsize=20, fontweight="bold", color=ACCENT, pad=20)
    ax.set_ylabel("Listening Time (Hours)", fontsize=11, labelpad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True)
    ax.margins(y=0.2)
    ax.text(
        0.98, 0.95, f"Most active: {peak_period}",
        transform=ax.transAxes, ha="right", va="top", color=SPOTIFY_GREEN,
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="#0d0d0d")
    print(f"  Saved: {output_path} (most active: {peak_period})")
    plt.show()


def plot_most_played_artists(
    df,
    output_path="charts/most_played_artists.png",
    title="Most Played Artists Recently",
):
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

    ax.set_title(title, fontsize=20,
                 fontweight="bold", color=ACCENT, pad=20)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis="y", labelsize=12)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150,
                bbox_inches="tight", facecolor="#0d0d0d")
    print(f"  Saved: {output_path}")
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
