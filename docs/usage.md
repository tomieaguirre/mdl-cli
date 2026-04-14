# mdl Usage

## Overview

`mdl` is a cross-platform CLI wrapper around `yt-dlp`.

It provides:

- A focused command surface for common workflows (`audio`, `video`, `info`, `smoke`).
- Persistent settings (`preset`, `cookies`, `cover`, formats, output path).
- Predictable command generation with optional dry-run printing.

`mdl` does not replace `yt-dlp`; it builds and executes `yt-dlp` commands.

## Requirements

- Python `>=3.10`
- `yt-dlp` available in `PATH`
- `ffmpeg` available in `PATH` (required when `cover=on`)

## Installation

Recommended (isolated app install):

```bash
pipx install mdl-cli
```

Alternative (standard Python environment):

```bash
pip install mdl-cli
```

## Command Reference

### Global

```bash
mdl --version
mdl --help
```

Running `mdl` with no arguments prints help and exits with code `0`.

### Download and Inspection

```bash
mdl audio URL [--mode auto|album|flat] [--print]
mdl video URL [--print]
mdl info URL
mdl smoke audio [--print]
mdl smoke video [--print]
```

Notes:

- `URL` can be a single item or playlist URL.
- `--print` (`audio`, `video`, `smoke`) prints the final `yt-dlp` command and exits without execution.
- `--mode` is available only for `audio`:
  - `auto` (default): detects album-like playlists (`list=OLAK...`) and uses album layout.
  - `album`: forces artist/channel + playlist layout.
  - `flat`: forces a single playlist folder.

### Settings

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

- `mdl config`: prints effective persisted config as JSON.
- `mdl <setting>`: prints current value.
- `mdl <setting> <value>`: validates, persists, and prints updated value.
- `mdl <setting> --list`: prints allowed values (except `out`, which accepts any path).
- `--print` is ignored for settings commands.

## Configuration and Defaults

### Config File Location

Settings are stored in:

```text
Linux: ~/.config/mdl/config.json
macOS: ~/Library/Application Support/mdl/config.json
Windows: %APPDATA%\mdl\config.json
```

Override config directory:

```bash
export MDL_CONFIG_DIR=/custom/path
```

PowerShell:

```powershell
$env:MDL_CONFIG_DIR = "C:\\custom\\path"
```

### Default Values

- `preset`: `safe`
- `cookies`: `none`
- `cover`: `off`
- `audio-format`: `m4a`
- `video-format`: `mp4`
- `out`:
  - Linux: `XDG_MUSIC_DIR/mdl` or `~/Music/mdl`
  - macOS/Windows: `~/Music/mdl`

### Allowed Values

- `preset`: `safe`, `fast`
- `cookies`: `none`, `brave`, `chrome`, `chromium`, `firefox`, `edge`
- `cover`: `on`, `off`
- `audio-format`: `flac`, `mp3`, `opus`, `m4a`
- `video-format`: `mp4`, `mkv`

### Validation Rules

- Values are normalized to lowercase.
- Invalid persisted values fall back to defaults on load.
- Invalid CLI values fail with a clear error and allowed set.
- `out` is normalized to an expanded absolute path.

## Runtime Behavior

### Presets

- `safe`: applies `--limit-rate 1M --sleep-interval 5 --max-sleep-interval 15`
- `fast`: disables rate/sleep throttling flags

### Output and Exit Codes

`mdl` always prints the executed command:

```text
[mdl] exec: yt-dlp ...
```

Execution model:

- `audio`, `video`, `smoke`: stream subprocess output.
- `info`: executes `yt-dlp -F URL` (plus shared flags if configured).
- Exit code is propagated from `yt-dlp`.
- `Ctrl+C` returns `130`.
- Missing dependencies return `127`.

### `--print` Mode

For `audio`, `video`, and `smoke`:

- Prints the fully quoted final command.
- Does not execute subprocesses.
- Exits `0`.

### Download Robustness Flags

Downloads include:

- `--ignore-errors`
- `--continue`
- `--no-overwrites`

## Output Templates

- Audio single: `%(artists.0|artist|uploader)s/%(title)s.%(ext)s`
- Audio playlist (album): `%(artists.0|artist|uploader)s/%(playlist_title|playlist)s/%(playlist_index)02d - %(title)s.%(ext)s`
- Audio playlist (flat): `%(playlist_title|playlist)s/%(playlist_index)02d - %(title)s.%(ext)s`
- Video single: `%(uploader|channel)s/%(title)s.%(ext)s`
- Video playlist: `%(playlist_title|playlist)s/%(playlist_index)02d - %(title)s.%(ext)s`

Layout behavior:

- `audio --mode auto`: `OLAK...` playlists use album layout; others use flat layout.
- `video` playlists always use flat layout.

## Cover / Thumbnail Behavior

- `cover off` (default): no thumbnail flags.
- `cover on`:
  - Audio: `--embed-thumbnail`
  - Video: `--write-thumbnail --embed-thumbnail`

Command-level defaults:

- `mdl audio ...`: `-f bestaudio/best -x --audio-format <audio-format>`
- `mdl video ...`: `-f bv*+ba/b --remux-video <video-format>`

## Troubleshooting

### `yt-dlp not found in PATH`

Install `yt-dlp` and verify:

```bash
yt-dlp --version
```

### `ffmpeg not found in PATH`

Install `ffmpeg` with your platform package manager and verify:

```bash
ffmpeg -version
```

### `invalid value '...'`

The setting is outside the allowed set:

```bash
mdl <setting> --list
```

### Unexpected output folder

Check current output path and update if needed:

```bash
mdl out
mdl out ./downloads
```

### Settings changes not reflected

Inspect effective config:

```bash
mdl config
```
