"""Parse participant positions from MeshCore channel messages."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

_PARTICIPANT_RE = re.compile(
    r"<[^>\n]+>\s*([^:\n<>]{1,80}):",
    re.MULTILINE,
)
_LOCATION_RE = re.compile(
    r"https?://(?:www\.)?maps\.google\.com/\?q="
    r"(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)",
    re.IGNORECASE,
)
_VOLTAGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*V\b", re.IGNORECASE)
_TEMPERATURE_RE = re.compile(r"(-?\d+(?:\.\d+)?)\s*C\b", re.IGNORECASE)
_LIGHT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class MeshCoreLocation:
    """Parsed GPS position and optional sensor values."""

    participant: str
    latitude: float
    longitude: float
    message: str
    battery_voltage: float | None = None
    temperature: float | None = None
    light_percent: float | None = None


def text_values(state: str, attributes: dict[str, Any]) -> list[str]:
    """Return useful string values from an entity state and attributes."""
    values = [state]
    values.extend(_flatten_text(attributes))
    return [value for value in values if value]


def _flatten_text(value: Any) -> list[str]:
    """Collect text recursively from common entity attribute containers."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for nested in value.values():
            result.extend(_flatten_text(nested))
        return result
    if isinstance(value, (list, tuple)):
        result = []
        for nested in value:
            result.extend(_flatten_text(nested))
        return result
    return []


def find_participants(messages: list[str]) -> list[str]:
    """Return participant names visible in channel messages."""
    participants: set[str] = set()
    for message in messages:
        if _LOCATION_RE.search(message) is None:
            continue
        for match in _PARTICIPANT_RE.finditer(message):
            participants.add(match.group(1).strip())
    return sorted(participants, key=str.casefold)


def parse_location(messages: list[str], participant: str) -> MeshCoreLocation | None:
    """Return the newest matching location visible in the supplied messages."""
    location: MeshCoreLocation | None = None
    marker = f"{participant}:"

    for message in messages:
        if marker not in message:
            continue
        coordinate_match = _LOCATION_RE.search(message)
        if coordinate_match is None:
            continue
        location = MeshCoreLocation(
            participant=participant,
            latitude=float(coordinate_match.group(1)),
            longitude=float(coordinate_match.group(2)),
            message=message,
            battery_voltage=_optional_float(_VOLTAGE_RE, message),
            temperature=_optional_float(_TEMPERATURE_RE, message),
            light_percent=_optional_float(_LIGHT_RE, message),
        )

    return location


def _optional_float(pattern: re.Pattern[str], message: str) -> float | None:
    """Read one optional number from a message."""
    match = pattern.search(message)
    return float(match.group(1)) if match else None
