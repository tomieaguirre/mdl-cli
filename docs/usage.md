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
mdl audio URL [--print]
mdl video URL [--print]
mdl info URL [--print]
mdl smoke audio [--print]
mdl smoke video [--print]
```

- `URL`: target media URL (single item or playlist).
- `--print`: print final `yt-dlp` command and exit without execution.

Output base directory is configured persistently with `mdl out`:

```bash
mdl out
mdl out ~/Music/mdl
```

`smoke` uses fixed test URLs:

```text
audio: https://www.youtube.com/watch?v=dWRCooFKk3c
video: https://www.youtube.com/watch?v=jNQXAC9IVRw
```

### Settings Commands

```bash
mdl cover [on|off] [--list]
mdl cookies [BROWSER|none] [--list]
mdl preset [safe|fast] [--list]
mdl audio-format [flac|mp3|opus|m4a] [--list]
mdl video-format [mp4|mkv] [--list]
mdl out [PATH]
```

Behavior:

- No value: show current value.
- Value provided: validate, persist, and print updated value.
- `--list`: show allowed values.
- `out` accepts any path and does not support `--list`.

`--print` is ignored for settings commands.

## Settings Model

Settings are stored in:

```text
~/.config/mdl/config.json
```

Override config directory with:

```bash
MDL_CONFIG_DIR=/custom/path
```

Default values:

- `preset`: `safe`
- `cookies`: `none`
- `cover`: `off`
- `audio-format`: `m4a`
- `video-format`: `mp4`
- `out`: `XDG_MUSIC_DIR/mdl` or `~/Music/mdl`

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

`--print` behavior:

- Prints the fully quoted final command.
- Does not run subprocesses.
- Exits `0`.

Default robustness flags for downloads:

- `--ignore-errors`
- `--continue`
- `--no-overwrites`

Output templates:

- Audio single: `%(artist|uploader)s/%(title)s.%(ext)s`
- Audio playlist: `%(artist|uploader)s/%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s`
- Video single: `%(uploader|channel)s/%(title)s.%(ext)s`
- Video playlist: `%(uploader|channel)s/%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s`

Playlist template selection uses a URL heuristic (`list=` in URL).

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
which yt-dlp
```

### `ffmpeg not found in PATH`

Install `ffmpeg` (required by `mdl` when `cover=on`):

```bash
sudo apt install ffmpeg
which ffmpeg
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
mdl preset
mdl cookies
mdl cover
mdl audio-format
mdl video-format
mdl out
cat ~/.config/mdl/config.json
```
