"""Find MeshCore channels and read their activity entries."""

from __future__ import annotations

from datetime import timedelta
from functools import partial
from typing import Any

from homeassistant.components.logbook.helpers import async_determine_event_types
from homeassistant.components.logbook.processor import EventProcessor
from homeassistant.components.recorder import get_instance
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.util import dt as dt_util

from .const import CONF_CHANNEL_IDX, CONF_CHANNEL_NAME, CONF_MESHCORE_ENTRY_ID, CONF_SOURCE_ENTITY

_HISTORY_HOURS = 24


def available_channels(hass: HomeAssistant) -> list[dict[str, Any]]:
    """Return configured MeshCore channels from loaded integration entries."""
    registry = er.async_get(hass)
    choices: list[dict[str, Any]] = []

    for entry in hass.config_entries.async_entries("meshcore"):
        coordinator = hass.data.get("meshcore", {}).get(entry.entry_id)
        if coordinator is None:
            continue
        max_channels = getattr(coordinator, "_max_channels", 4)
        channel_info = getattr(coordinator, "_channel_info", {})
        for idx in range(max_channels):
            name = channel_info.get(idx, {}).get("channel_name", "(unused)")
            if not name or name == "(unused)":
                continue
            source_entity = _find_message_entity(registry, entry.entry_id, idx)
            value = f"{entry.entry_id}|{idx}|{source_entity or ''}"
            label = f"{name} ({idx})"
            if source_entity:
                label += f" - {source_entity}"
            choices.append(
                {
                    "value": value,
                    "label": label,
                    CONF_MESHCORE_ENTRY_ID: entry.entry_id,
                    CONF_CHANNEL_IDX: idx,
                    CONF_CHANNEL_NAME: name,
                    CONF_SOURCE_ENTITY: source_entity,
                }
            )
    return choices


def apply_channel_selection(data: dict[str, Any], channels: list[dict[str, Any]]) -> None:
    """Expand a selected option value into config-entry fields."""
    selection = data["channel_selection"]
    chosen = next(item for item in channels if item["value"] == selection)
    data.update(
        {
            CONF_MESHCORE_ENTRY_ID: chosen[CONF_MESHCORE_ENTRY_ID],
            CONF_CHANNEL_IDX: chosen[CONF_CHANNEL_IDX],
            CONF_CHANNEL_NAME: chosen[CONF_CHANNEL_NAME],
            CONF_SOURCE_ENTITY: chosen[CONF_SOURCE_ENTITY],
        }
    )


def _find_message_entity(registry: er.EntityRegistry, entry_id: str, channel_idx: int) -> str | None:
    """Find the channel message binary sensor that owns the visible logbook."""
    for entity in registry.entities.values():
        if entity.config_entry_id != entry_id or entity.domain != "binary_sensor":
            continue
        if f"_ch_{channel_idx}_messages" in entity.entity_id:
            return entity.entity_id
    return None


async def async_logbook_messages(hass: HomeAssistant, entity_id: str | None) -> list[str]:
    """Read messages visible in the Activity popup for a channel entity."""
    if not entity_id:
        return []
    start = dt_util.utcnow() - timedelta(hours=_HISTORY_HOURS)
    end = dt_util.utcnow()
    entity_ids = [entity_id]
    event_types = async_determine_event_types(hass, entity_ids, None)
    processor = EventProcessor(
        hass,
        event_types,
        entity_ids,
        None,
        None,
        timestamp=False,
        include_entity_name=True,
    )
    entries = await get_instance(hass).async_add_executor_job(
        partial(processor.get_events, start, end)
    )
    messages: list[str] = []
    for entry in entries:
        name = str(entry.get("name", ""))
        message = str(entry.get("message", ""))
        messages.append(f"{name}: {message}" if message else name)
    return messages
