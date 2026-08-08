# Spotify history import plan

When the Spotify Extended Streaming History ZIP arrives:

- Import the lifetime streaming-history JSON files into `analytics_history/listening_history.csv`.
- Preserve every individual listening event as its own row, including consecutive or repeated plays of the same track.
- Never aggregate repeated tracks during import.
- Remove only exact duplicate listening events caused by overlap between the Spotify export, the existing CSV, and recently played API results.
- Continue merging recent API results after the import to cover activity newer than the export.
- Treat the current cumulative dataset as "captured history," not true "all time," until the lifetime export is imported.
- Consider an automated schedule afterward so future plays are captured without gaps.
