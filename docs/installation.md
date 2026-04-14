# Installation

## Requirements

- Python 3.10+
- `ffmpeg` (required for some features)
- `yt-dlp` available in `PATH`

---

## Install Python

### Linux

Use your distribution package manager. Example (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### macOS

```bash
brew install python
```

### Windows

PowerShell:

```powershell
winget install -e --id Python.Python.3.12
```

Manual installer:
- https://www.python.org/downloads/windows/

---

## Install mdl-cli

### Install pipx (if needed)

Linux (Debian/Ubuntu):

```bash
sudo apt install pipx
pipx ensurepath
```

macOS:

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Windows (PowerShell):

```powershell
py -m pip install --user pipx
py -m pipx ensurepath
```

Open a new terminal after `ensurepath`.

### Recommended (pipx)

```bash
pipx install mdl-cli
```

### Alternative (pip)

```bash
pip install mdl-cli
```

---

## Install ffmpeg

### Linux

```bash
sudo apt install ffmpeg
```

### macOS

```bash
brew install ffmpeg
```

### Windows

PowerShell:

```powershell
winget install -e --id Gyan.FFmpeg
```

Manual install:
- https://ffmpeg.org/download.html

---

## Install yt-dlp

```bash
pipx install yt-dlp
```

If you prefer `pip`:

```bash
pip install yt-dlp
```

---

## Verify Installation

```bash
python --version
yt-dlp --version
ffmpeg -version
mdl --version
mdl smoke audio
```
