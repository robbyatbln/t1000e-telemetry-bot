"""GPS tracker entities supplied by MeshCore Location."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.components.device_tracker.const import SourceType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_PARTICIPANT,
    CONF_CHANNEL_IDX,
    CONF_PERSON_ENTITY,
    CONF_SOURCE_ENTITY,
    CONF_TRACKER_NAME,
)
from .discovery import async_logbook_messages
from .parser import MeshCoreLocation, parse_location, text_values

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up a configured MeshCore location tracker."""
    async_add_entities([MeshCoreLocationTracker(entry)])


class MeshCoreLocationTracker(TrackerEntity):
    """Track one participant from a MeshCore message entity."""

    _attr_latitude: float | None = None
    _attr_location_accuracy = 25.0
    _attr_longitude: float | None = None
    _attr_source_type = SourceType.GPS
    _attr_should_poll = False

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the tracker."""
        self._source_entity = entry.data[CONF_SOURCE_ENTITY]
        self._participant = entry.data[CONF_PARTICIPANT]
        self._person_entity = entry.data[CONF_PERSON_ENTITY]
        self._channel_idx = int(entry.data[CONF_CHANNEL_IDX])
        self._attr_name = entry.data[CONF_TRACKER_NAME]
        self._attr_unique_id = entry.unique_id or entry.entry_id
        self._attr_available = False
        self._location: MeshCoreLocation | None = None
        self._attr_device_info = DeviceInfo(
            identifiers={("meshcore_location", self._attr_unique_id)},
            name=self._attr_name,
            manufacturer="MeshCore",
            model="Telemetry Tracker",
        )

    async def async_added_to_hass(self) -> None:
        """Read current data and subscribe to future channel messages."""
        await super().async_added_to_hass()
        self._process_current_state()
        if self._location is None:
            await self._async_process_recent_history()
        self.async_on_remove(
            self.hass.bus.async_listen("meshcore_message", self._async_message_received)
        )
        if self._source_entity:
            self.async_on_remove(
                async_track_state_change_event(
                    self.hass, [self._source_entity], self._async_source_changed
                )
            )

    async def _async_process_recent_history(self) -> None:
        """Restore the newest valid position for this participant from history."""
        try:
            messages = await async_logbook_messages(self.hass, self._source_entity)
        except Exception:  # noqa: BLE001 - recorder may be disabled/unavailable
            _LOGGER.warning(
                "Unable to restore MeshCore position history for %s",
                self._source_entity,
                exc_info=True,
            )
            return
        self._update_location(parse_location(messages, self._participant))

    @callback
    def _async_message_received(self, event) -> None:
        """Update from the live MeshCore event stream."""
        data = event.data
        if data.get("message_type") != "channel":
            return
        if int(data.get("channel_idx", -1)) != self._channel_idx:
            return
        sender = str(data.get("sender_name", ""))
        if sender != self._participant:
            return
        message = f"{sender}: {data.get('message', '')}"
        self._update_location(parse_location([message], self._participant))

    @callback
    def _async_source_changed(self, event: Event[EventStateChangedData]) -> None:
        """Update location when the selected source entity changes."""
        new_state = event.data["new_state"]
        if new_state is None:
            return
        self._update_location(
            parse_location(
                text_values(new_state.state, dict(new_state.attributes)),
                self._participant,
            )
        )

    @callback
    def _process_current_state(self) -> None:
        """Initialize from the current source state if possible."""
        if not self._source_entity:
            return
        state = self.hass.states.get(self._source_entity)
        if state is None:
            return
        self._update_location(
            parse_location(
                text_values(state.state, dict(state.attributes)), self._participant
            )
        )

    @callback
    def _update_location(self, location: MeshCoreLocation | None) -> None:
        """Store and publish a valid position."""
        if location is None:
            return
        self._location = location
        self._attr_latitude = location.latitude
        self._attr_longitude = location.longitude
        self._attr_available = True
        if self.hass is not None:
            self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return diagnostic information about the parsed message."""
        attributes: dict[str, Any] = {
            "meshcore_source_entity": self._source_entity,
            "meshcore_participant": self._participant,
            "selected_person": self._person_entity,
        }
        if self._location is None:
            return attributes
        attributes["last_meshcore_message"] = self._location.message
        if self._location.battery_voltage is not None:
            attributes["battery_voltage"] = self._location.battery_voltage
        if self._location.temperature is not None:
            attributes["temperature"] = self._location.temperature
        if self._location.light_percent is not None:
            attributes["light_percent"] = self._location.light_percent
        return attributes
