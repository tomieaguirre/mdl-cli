[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://github.com/tomieaguirre/mdl-cli/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/tomieaguirre/mdl-cli/actions/workflows/ci.yml?query=branch%3Amain)

# mdl-cli

`mdl` is a cross-platform CLI wrapper around `yt-dlp` with safer defaults and a simpler command surface.

## Requirements

- Python `>=3.10`
- `ffmpeg` available in `PATH`

`mdl` executes `yt-dlp` under the hood. Ensure `yt-dlp` is installed and available in `PATH`.

## Installation

Recommended (isolated app install):

```bash
pipx install mdl-cli
```

Alternative (standard Python environment):

```bash
pip install mdl-cli
```

For OS-specific setup (Python, `ffmpeg`, `yt-dlp`, and verification), see the [Installation Guide](docs/installation.md).

## Basic Usage

```bash
mdl audio "URL"
mdl video "URL"
mdl info "URL"
mdl --help
```

Supported platforms: Linux, macOS, and Windows.

## Documentation

Full command reference and advanced configuration:
- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)

## License

MIT (see [License](LICENSE))
