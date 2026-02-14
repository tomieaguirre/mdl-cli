# mdl-cli

`mdl` is a safe-by-default command-line wrapper around `yt-dlp`.

It builds predictable `yt-dlp` commands with practical defaults and a simplified interface.

---

## Overview

`mdl` does not replace `yt-dlp`.  
It acts as a wrapper that:

- Applies safe defaults (rate limits, retries, sleep intervals)
- Provides persistent configuration
- Simplifies common audio/video workflows

---

## Requirements

The following tools must be installed and available in your system `PATH`:

- Python >= 3.10
- `yt-dlp`
- `ffmpeg`

To verify they are available:

```bash
yt-dlp --version
ffmpeg -version
```

If these commands work, they are correctly installed.

## Install Dependencies

### Install ffmpeg (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install -y ffmpeg
```

### Install yt-dlp (recommended via pipx)

```bash
pipx install yt-dlp
```

Verify:

```bash
yt-dlp --version
```

## Install mdl

### Option 1: Install from local clone (development)

Clone the repository:

```bash
git clone https://github.com/tomieaguirre/mdl-cli.git
cd mdl-cli
```

Install using `pipx`:

```bash
pipx install .
```

This installs the current project using the local `pyproject.toml`.

### Option 2: Install directly from GitHub

```bash
pipx install git+https://github.com/tomieaguirre/mdl-cli.git
```

## Optional: Improve Thumbnail Embedding

If you enable:

```bash
mdl cover on
```

You may improve metadata handling by installing `mutagen` into the `yt-dlp` pipx environment:

```bash
pipx inject yt-dlp mutagen
```

## Quickstart

```bash
mdl --help
mdl out
mdl out ~/Music/mdl
mdl audio "URL" --print
mdl audio "URL"
mdl video "URL"
mdl info "URL"
```

If your URL contains `&`, always quote it:

```bash
mdl audio "https://music.youtube.com/watch?v=ID&si=SOMETHING"
```

## Settings

Show current value:

```bash
mdl preset
mdl cookies
mdl cover
mdl audio-format
mdl video-format
mdl out
```

Set a new value:

```bash
mdl preset fast
mdl cookies brave
mdl cover on
mdl audio-format m4a
mdl video-format mkv
mdl out ~/Music/mdl
```

List allowed values:

```bash
mdl preset --list
mdl cookies --list
mdl cover --list
mdl audio-format --list
mdl video-format --list
# out accepts any path, so it has no --list
```

## Documentation

Full command reference:

- [Usage Guide](docs/usage.md)

## License

MIT (see [License](LICENSE))
