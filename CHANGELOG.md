# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-02-17

### Added
- New `mdl config` command to print the effective persistent configuration as JSON.

### Changed
- `mdl info` no longer accepts `--print`; it always executes `yt-dlp -F` directly.
- Audio output templates now prefer the first artist (`artists.0`) so playlist/album tracks with collaborators stay in one primary artist folder.
- Playlist downloads now strip a leading `Album - ` prefix from `playlist_title` when generating folder names.
- Added `--mode {auto,album,flat}` to `audio` and changed default playlist layout to `auto` (`OLAK...` => album, otherwise flat single-folder playlist).
- Video playlists now always use flat single-folder layout.

## [0.1.1] - 2026-02-16

### Fixed
- Handle `None` correctly in `smoke_kind` conversion.

### Added
- Unit test suite across core modules (builders, config store, resolve, CLI, services).
- Coverage reporting via `pytest-cov`.

## [0.1.0] - 2026-02-15

### Added
- Initial alpha release of mdl-cli
- `audio`, `video`, `info`, and `smoke` commands
- Persistent configuration system
- Safe and fast presets
- Configurable output directory
- Optional thumbnail embedding
- Robust default download flags
