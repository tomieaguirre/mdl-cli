from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path

from mdl.options import AppConfig

# overrideable for tests via env var
_DEFAULT_CONFIG_DIR = Path("~/.config/mdl").expanduser()
_ENV_CONFIG_DIR = "MDL_CONFIG_DIR"


ALLOWED = {
    "cover": ["on", "off"],
    "cookies": ["none", "brave", "chrome", "chromium", "firefox", "edge"],
    "preset": ["safe", "fast"],
    "audio-format": ["flac", "mp3", "opus", "m4a"],
    "video-format": ["mp4", "mkv"],
}


def default_config() -> AppConfig:
    return AppConfig(
        preset="safe",
        cookies="none",
        cover=False,
        audio_format="flac",
        video_format="mp4",
    )


def _config_dir() -> Path:
    raw = os.environ.get(_ENV_CONFIG_DIR)
    if raw:
        return Path(raw).expanduser()
    return _DEFAULT_CONFIG_DIR


def _config_file() -> Path:
    return _config_dir() / "config.json"


def load_config() -> AppConfig:
    cfg_file = _config_file()
    if not cfg_file.exists():
        return default_config()

    try:
        data = json.loads(cfg_file.read_text(encoding="utf-8"))
    except Exception:
        return default_config()

    cfg = default_config()

    preset = _norm_str(data.get("preset", cfg.preset))
    cookies = _norm_str(data.get("cookies", cfg.cookies))
    cover = bool(data.get("cover", cfg.cover))
    audio_format = _norm_str(data.get("audio_format", cfg.audio_format))
    video_format = _norm_str(data.get("video_format", cfg.video_format))

    preset = preset if preset in ALLOWED["preset"] else cfg.preset
    cookies = cookies if cookies in ALLOWED["cookies"] else cfg.cookies
    audio_format = audio_format if audio_format in ALLOWED["audio-format"] else cfg.audio_format
    video_format = video_format if video_format in ALLOWED["video-format"] else cfg.video_format

    return AppConfig(
        preset=preset,
        cookies=cookies,
        cover=cover,
        audio_format=audio_format,
        video_format=video_format,
    )


def save_config(cfg: AppConfig) -> None:
    cfg_dir = _config_dir()
    cfg_dir.mkdir(parents=True, exist_ok=True)
    payload = asdict(cfg)
    _config_file().write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def list_allowed_values(setting: str) -> list[str]:
    setting = _norm_str(setting)
    if setting not in ALLOWED:
        raise SystemExit(f"[mdl] ERROR: unknown setting '{setting}'.")
    return list(ALLOWED[setting])


def describe_config_value(cfg: AppConfig, setting: str) -> str:
    setting = _norm_str(setting)
    if setting == "cover":
        return "on" if cfg.cover else "off"
    if setting == "cookies":
        return cfg.cookies
    if setting == "preset":
        return cfg.preset
    if setting == "audio-format":
        return cfg.audio_format
    if setting == "video-format":
        return cfg.video_format
    raise SystemExit(f"[mdl] ERROR: unknown setting '{setting}'.")


def set_config_value(cfg: AppConfig, setting: str, value: str) -> AppConfig:
    setting = _norm_str(setting)
    value_n = _norm_str(value)

    if setting not in ALLOWED:
        raise SystemExit(f"[mdl] ERROR: unknown setting '{setting}'.")

    if value_n not in ALLOWED[setting]:
        allowed = ", ".join(ALLOWED[setting])
        raise SystemExit(f"[mdl] ERROR: invalid value '{value}'. Allowed: {allowed}")

    if setting == "cover":
        return AppConfig(cfg.preset, cfg.cookies, value_n == "on", cfg.audio_format, cfg.video_format)
    if setting == "cookies":
        return AppConfig(cfg.preset, value_n, cfg.cover, cfg.audio_format, cfg.video_format)
    if setting == "preset":
        return AppConfig(value_n, cfg.cookies, cfg.cover, cfg.audio_format, cfg.video_format)
    if setting == "audio-format":
        return AppConfig(cfg.preset, cfg.cookies, cfg.cover, value_n, cfg.video_format)
    if setting == "video-format":
        return AppConfig(cfg.preset, cfg.cookies, cfg.cover, cfg.audio_format, value_n)

    raise SystemExit(f"[mdl] ERROR: unknown setting '{setting}'.")


def _norm_str(x: object) -> str:
    return str(x).strip().lower()
