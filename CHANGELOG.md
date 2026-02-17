# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-02-17

### Added
- New `mdl config` command to print the effective persistent configuration as JSON.
- Added `--mode {auto,album,flat}` to `audio` command to control playlist layout behavior.
- Playlist downloads now automatically strip a leading `Album - ` prefix from `playlist_title`.

### Changed
- `mdl info` no longer accepts `--print`; it now always executes `yt-dlp -F`.
- Audio playlist layout now prefers the primary artist (`artists.0`) to prevent album fragmentation when tracks contain collaborators.
- Default playlist layout mode for audio is now `auto` (`OLAK...` playlists → album layout, others → flat layout).
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
