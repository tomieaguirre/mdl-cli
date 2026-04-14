# mdl Usage

## Overview

`mdl` is a thin CLI wrapper around `yt-dlp`.  
It provides:

- A small command surface for common download workflows (`audio`, `video`, `info`, `smoke`).
- Persistent settings for default behavior (`preset`, `cookies`, `cover`, formats).
- Predictable `yt-dlp` command generation with optional dry-run printing.

`mdl` does not replace `yt-dlp`; it composes and executes `yt-dlp` commands.

## Full Command Reference

### Global

```bash
mdl --version
mdl --help
```

If you run `mdl` with no arguments, it prints help and exits with code `0`.

### Download and Inspection Commands

```bash
mdl audio URL [--mode auto|album|flat] [--print]
mdl video URL [--print]
mdl info URL
mdl smoke audio [--print]
mdl smoke video [--print]
```

- `URL`: target media URL (single item or playlist).
- `--print` (`audio`, `video`, `smoke`): print final `yt-dlp` command and exit without execution.
- `--mode` (`audio` only):
  - `auto` (default): detect album-like playlists (`list=OLAK...`) as album layout, otherwise flat layout.
  - `album`: force `artist-or-channel/playlist/...`.
  - `flat`: force `playlist/...` (single folder for all entries).

Output base directory is configured persistently with `mdl out`:

```bash
mdl config
mdl out
mdl out ./downloads
```

`smoke` uses fixed test URLs:

```text
audio: https://www.youtube.com/watch?v=dWRCooFKk3c
video: https://www.youtube.com/watch?v=jNQXAC9IVRw
```

### Settings Commands

```bash
mdl config
mdl cover [on|off] [--list]
mdl cookies [BROWSER|none] [--list]
mdl preset [safe|fast] [--list]
mdl audio-format [flac|mp3|opus|m4a] [--list]
mdl video-format [mp4|mkv] [--list]
mdl out [PATH]
```

Behavior:

- `config`: show the effective persistent config as JSON.
- No value (`cover`, `cookies`, `preset`, `audio-format`, `video-format`, `out`): show current value.
- Value provided (`cover`, `cookies`, `preset`, `audio-format`, `video-format`, `out`): validate, persist, and print updated value.
- `--list` (`cover`, `cookies`, `preset`, `audio-format`, `video-format`): show allowed values.
- `out` accepts any path and does not support `--list`.

`--print` is ignored for settings commands.

## Settings Model

Settings are stored in:

```text
Linux: ~/.config/mdl/config.json
macOS/iOS Python environments: ~/Library/Application Support/mdl/config.json
Windows: %APPDATA%\mdl\config.json
```

Override config directory with:

```bash
export MDL_CONFIG_DIR=/custom/path
```

PowerShell:

```powershell
$env:MDL_CONFIG_DIR = "C:\\custom\\path"
```

Default values:

- `preset`: `safe`
- `cookies`: `none`
- `cover`: `off`
- `audio-format`: `m4a`
- `video-format`: `mp4`
- `out`: Linux -> `XDG_MUSIC_DIR/mdl` or `~/Music/mdl`; other platforms -> `~/Music/mdl`

Allowed values:

- `preset`: `safe`, `fast`
- `cookies`: `none`, `brave`, `chrome`, `chromium`, `firefox`, `edge`
- `cover`: `on`, `off`
- `audio-format`: `flac`, `mp3`, `opus`, `m4a`
- `video-format`: `mp4`, `mkv`

Normalization and validation:

- Values are normalized to lowercase.
- Unknown/invalid persisted values fall back to defaults when loaded.
- Invalid values passed on CLI fail with a clear error and allowed set.
- `out` is normalized to an expanded absolute path.

Preset behavior:

- `safe`: applies `--limit-rate 1M --sleep-interval 5 --max-sleep-interval 15`
- `fast`: no rate limit or sleep flags

## Output Behavior

`mdl` always emits the exact command it runs:

```text
[mdl] exec: yt-dlp ...
```

Execution behavior:

- `audio`, `video`, `smoke`: stream `yt-dlp` stdout/stderr directly.
- `info`: runs `yt-dlp -F ...` (plus optional shared flags).
- Exit code is propagated from the `yt-dlp` subprocess.
- `Ctrl+C` returns exit code `130`.

`--print` behavior (`audio`, `video`, `smoke` only):

- Prints the fully quoted final command.
- Does not run subprocesses.
- Exits `0`.

Default robustness flags for downloads:

- `--ignore-errors`
- `--continue`
- `--no-overwrites`

Output templates:

- Audio single: `%(artists.0|artist|uploader)s/%(title)s.%(ext)s`
- Audio playlist (album layout): `%(artists.0|artist|uploader)s/%(playlist_title|playlist)s/%(playlist_index)02d - %(title)s.%(ext)s`
- Audio playlist (flat layout): `%(playlist_title|playlist)s/%(playlist_index)02d - %(title)s.%(ext)s`
- Video single: `%(uploader|channel)s/%(title)s.%(ext)s`
- Video playlist: `%(playlist_title|playlist)s/%(playlist_index)02d - %(title)s.%(ext)s` (always flat)

For audio album layout, this prefers the first artist (`artists.0`) so collaborations stay under the primary artist folder.
For playlist folders, `mdl` removes a leading `Album - ` prefix in `playlist_title` when present.

In `auto` mode, playlist layout detection uses the playlist id:
- `OLAK...` => album layout
- everything else => flat layout
For video playlists, `mdl` always uses flat layout.

## Thumbnail/Cover Behavior

`cover` controls thumbnail embedding strategy:

- `cover off` (default): no thumbnail flags are added.
- `cover on`:
  - Audio command adds `--embed-thumbnail`.
  - Video command adds `--write-thumbnail --embed-thumbnail`.

Command-level behavior:

- `mdl audio ...` uses `-f bestaudio/best -x --audio-format <audio-format>`.
- `mdl video ...` uses `-f bv*+ba/b --remux-video <video-format>`.

Notes:

- Thumbnail embedding is best-effort and depends on `yt-dlp` + media/container support.
- Even with `cover off`, some extract/remux flows may still require `ffmpeg` via `yt-dlp`.

## Dependency Model

Python/runtime:

- Python `>=3.10`
- `mdl` package itself has no required third-party runtime Python dependencies.

External executables:

- `yt-dlp` is required for all non-settings commands.
- `ffmpeg` is hard-checked by `mdl` when `cover=on` for audio/video/smoke.

Dependency checks run before execution:

- Missing dependency returns exit code `127`.
- `mdl` still prints the command it would have executed.

## Troubleshooting

### `yt-dlp not found in PATH`

Install `yt-dlp` and verify it is available in `PATH`:

```bash
pipx install yt-dlp
yt-dlp --version
```

### `ffmpeg not found in PATH`

Install `ffmpeg` (required by `mdl` when `cover=on`):

```bash
sudo apt install ffmpeg
ffmpeg -version
```

### `invalid value '...'`

The setting value is outside the allowed set. Check valid values:

```bash
mdl <setting> --list
```

### Files appear in an unexpected directory

Check effective output base:

- Current setting: `mdl out`
- Set a new base: `mdl out /your/path`

Also verify whether URL matched playlist mode (`list=`), which changes path template.

### Changes to settings are not taking effect

Inspect current settings and config path:

```bash
mdl config
mdl preset
mdl cookies
mdl cover
mdl audio-format
mdl video-format
mdl out
```

Then inspect your platform config file:

```text
Linux: ~/.config/mdl/config.json
macOS/iOS Python environments: ~/Library/Application Support/mdl/config.json
Windows: %APPDATA%\mdl\config.json
```
