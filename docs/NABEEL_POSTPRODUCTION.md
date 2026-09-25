# NABEEL post-production pipeline

Canonical media root: `~/Videos/NABEEL` (override with `NABEEL_MEDIA_ROOT`).

- `Recordings/` — OBS source recordings, preferably MKV.
- `Clips/` — intermediate cuts.
- `Exports/` — publish-ready H.264/AAC MP4 plus a SHA-256 provenance manifest.
- `Archive/` — retained source recordings after publication/retention review.

Run:

```bash
scripts/nabeel-postprocess.sh ~/Videos/NABEEL/Recordings/session.mkv
scripts/nabeel-postprocess.sh ~/Videos/NABEEL/Recordings/session.mkv 30 90
```

The export profile is H.264, yuv420p, AAC, and `faststart`, suitable for standard YouTube upload. Every export gets a JSON manifest tying it to the exact source path and SHA-256.

Optional transcription is intentionally not silently installed or enabled. Add a transcription adapter only when an approved local model/tool is available; publishing must not depend on it.
