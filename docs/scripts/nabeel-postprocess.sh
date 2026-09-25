#!/usr/bin/env bash
set -euo pipefail

ROOT="${NABEEL_MEDIA_ROOT:-$HOME/Videos/NABEEL}"
RECORDINGS="$ROOT/Recordings"
CLIPS="$ROOT/Clips"
EXPORTS="$ROOT/Exports"
ARCHIVE="$ROOT/Archive"
mkdir -p "$RECORDINGS" "$CLIPS" "$EXPORTS" "$ARCHIVE"

usage() { echo "Usage: $0 <source.mkv> [start_seconds] [duration_seconds]"; }
[ $# -ge 1 ] || { usage; exit 2; }
SOURCE=$(readlink -f "$1")
[ -f "$SOURCE" ] || { echo "source_not_found" >&2; exit 3; }
START="${2:-0}"
DURATION="${3:-}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
BASE=$(basename "$SOURCE")
NAME="${BASE%.*}"
OUT="$EXPORTS/${NAME}-${STAMP}.mp4"
MANIFEST="$OUT.manifest.json"

args=(-hide_banner -loglevel error -y -ss "$START" -i "$SOURCE")
[ -z "$DURATION" ] || args+=(-t "$DURATION")
args+=(-map 0:v:0 -map '0:a:0?' -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k "$OUT")
ffmpeg "${args[@]}"

SOURCE_SHA=$(sha256sum "$SOURCE" | awk '{print $1}')
OUTPUT_SHA=$(sha256sum "$OUT" | awk '{print $1}')
DURATION_OUT=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT")
python3 - "$MANIFEST" "$SOURCE" "$SOURCE_SHA" "$OUT" "$OUTPUT_SHA" "$DURATION_OUT" <<'PY'
import json,sys,datetime
manifest,source,source_sha,out,out_sha,duration=sys.argv[1:]
data={
  'schema':'nabeel.postproduction.v1',
  'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'source':source,
  'source_sha256':source_sha,
  'export':out,
  'export_sha256':out_sha,
  'duration_seconds':float(duration),
  'profile':'youtube-h264-aac-faststart'
}
open(manifest,'w',encoding='utf-8').write(json.dumps(data,indent=2)+"\n")
PY
echo "EXPORT=$OUT"
echo "MANIFEST=$MANIFEST"
