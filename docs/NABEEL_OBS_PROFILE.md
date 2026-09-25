# NABEEL OBS profile

`docs/scripts/nabeel-obs-bootstrap.py` installs a deterministic local OBS profile named `NABEEL-1080p60` and scene collection `NABEEL Station`.

Defaults: 1920×1080, 60 fps, 48 kHz stereo, advanced recording, MKV, and `~/Videos/NABEEL/Recordings`. Existing NABEEL profile/scene files are backed up before replacement.

The bootstrap intentionally leaves capture devices and streaming credentials unset. Add the authorized Chiaki window/game capture, microphone and optional camera interactively in OBS; no source credential is committed.

Final certification requires a 30-minute real recording with OBS stats/log evidence for dropped frames and audio/video sync.
