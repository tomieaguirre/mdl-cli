# mdl-cli

`mdl` is a command-line wrapper around `yt-dlp`, with a simpler interface and practical defaults for day-to-day use.

It does not replace `yt-dlp`: it builds and runs `yt-dlp` commands with persistent configuration and predictable behavior.

## What It Does

- Downloads audio (`mdl audio URL`) and video (`mdl video URL`) at best available quality.
- Supports persistent settings (`preset`, `cookies`, `cover`, formats).
- Includes a quick setup check (`mdl smoke audio|video`).
- Lets you inspect available formats (`mdl info URL`).
- Can print the final command without executing it (`--print`).

## Requirements

- Python `>= 3.10`
- `yt-dlp` available in `PATH`
- `ffmpeg` available in `PATH` (recommended; required in many extract/remux flows and for embedded thumbnails)

### Ubuntu / Debian

```bash
sudo apt install ffmpeg
pipx install yt-dlp
```

## Installing `mdl`

### Local install with `pipx` (recommended)

From the project root:

```bash
pipx install .
```

### Development install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Quick Usage

### Download audio

```bash
mdl audio "URL"
```

### Download video

```bash
mdl video "URL"
```

### Show available formats

```bash
mdl info "URL"
```

### Run setup smoke test

```bash
mdl smoke audio
mdl smoke video
```

### Print command without executing

```bash
mdl audio "URL" --print
```

## Options

### `--out`

Sets the base output directory for `audio` and `video`.

```bash
mdl audio "URL" --out /path/to/output
```

By default, `mdl` uses `XDG_MUSIC_DIR/mdl` (if present in `~/.config/user-dirs.dirs`) or falls back to `~/Music/mdl`.

### `--version`

```bash
mdl --version
```

## Persistent Configuration

Stored at:

```text
~/.config/mdl/config.json
```

### Show current value

```bash
mdl cover
mdl cookies
mdl preset
mdl audio-format
mdl video-format
```

### Change value

```bash
mdl cover on
mdl cover off

mdl cookies brave
mdl cookies none

mdl preset safe
mdl preset fast

mdl audio-format flac
mdl audio-format mp3
mdl audio-format opus
mdl audio-format m4a

mdl video-format mp4
mdl video-format mkv
```

### List allowed values

```bash
mdl cover --list
mdl cookies --list
mdl preset --list
mdl audio-format --list
mdl video-format --list
```

## Presets

### `safe` (default)

Enables more conservative network behavior:

- `--limit-rate 1M`
- `--sleep-interval 5`
- `--max-sleep-interval 15`

### `fast`

Disables rate limiting and random sleep between items.

## Output Structure

`mdl` uses different templates for single items and playlists.

Audio:

- Single: `%(artist|uploader)s/%(title)s.%(ext)s`
- Playlist: `%(artist|uploader)s/%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s`

Video:

- Single: `%(uploader|channel)s/%(title)s.%(ext)s`
- Playlist: `%(uploader|channel)s/%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s`

## Technical Behavior (Summary)

- Audio: `-f bestaudio/best -x --audio-format <format>`
- Video: `-f bv*+ba/b --remux-video <format>`
- Info: `-F`
- Download robustness: `--ignore-errors --continue --no-overwrites`
- Optional cookies: `--cookies-from-browser <browser>`
- Optional thumbnails (`cover on`): `--write-thumbnail --embed-thumbnail`

## Common Errors

### `yt-dlp not found in PATH`

Install `yt-dlp`:

```bash
pipx install yt-dlp
```

### `ffmpeg not found in PATH`

Install `ffmpeg`:

```bash
sudo apt install ffmpeg
```

### `invalid value ... Allowed: ...`

The config value is not in the allowed set. Use `--list` for that setting to see valid options.

## Philosophy

- Small, stable CLI.
- Sensible defaults.
- Transparency: you can always inspect the final command.
- `yt-dlp` remains the source of truth.

## License

MIT. See `LICENSE`.
