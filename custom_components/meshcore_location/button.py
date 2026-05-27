"""Command buttons for configured MeshCore telemetry trackers."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import async_send_firmware_command
from .const import (
    CONF_PARTICIPANT,
    CONF_TRACKER_NAME,
    ROUTE_CHANNEL,
    ROUTE_DIRECT,
)


@dataclass(frozen=True, slots=True)
class CommandDescription:
    """Describe one exposed firmware command."""

    key: str
    name: str
    command: str
    route: str
    icon: str
    enabled_default: bool = True


COMMANDS: tuple[CommandDescription, ...] = (
    CommandDescription("channel_status", "Status abfragen", "status", ROUTE_CHANNEL, "mdi:information-outline"),
    CommandDescription("channel_start", "Telemetrie starten", "start", ROUTE_CHANNEL, "mdi:play-circle-outline"),
    CommandDescription("channel_stop", "Telemetrie stoppen", "stop", ROUTE_CHANNEL, "mdi:stop-circle-outline"),
    CommandDescription("channel_all", "Alle Messwerte melden", "all", ROUTE_CHANNEL, "mdi:format-list-checks"),
    CommandDescription("channel_gps", "Nur GPS melden", "gps", ROUTE_CHANNEL, "mdi:crosshairs-gps"),
    CommandDescription("channel_gps_full", "GPS und Sensoren melden", "gps akku temp licht", ROUTE_CHANNEL, "mdi:map-marker-check-outline"),
    CommandDescription("channel_sync", "Zeitsync anfordern", "sync", ROUTE_CHANNEL, "mdi:clock-sync-outline"),
    CommandDescription("channel_ble_on", "Bluetooth einschalten", "ble on", ROUTE_CHANNEL, "mdi:bluetooth"),
    CommandDescription("channel_ble_off", "Bluetooth ausschalten", "ble off", ROUTE_CHANNEL, "mdi:bluetooth-off"),
    CommandDescription("channel_interval_10", "Intervall 10 Minuten", "interval 10", ROUTE_CHANNEL, "mdi:timer-outline", False),
    CommandDescription("channel_interval_30", "Intervall 30 Minuten", "interval 30", ROUTE_CHANNEL, "mdi:timer-outline", False),
    CommandDescription("direct_sound_on", "Ton einschalten", "sound on", ROUTE_DIRECT, "mdi:volume-high"),
    CommandDescription("direct_sound_off", "Ton ausschalten", "sound off", ROUTE_DIRECT, "mdi:volume-off"),
    CommandDescription("direct_find", "Suchton abspielen", "wo ist 3", ROUTE_DIRECT, "mdi:bell-ring-outline"),
    CommandDescription("direct_alarm_off", "Wecker ausschalten", "wecker aus", ROUTE_DIRECT, "mdi:alarm-off", False),
    CommandDescription("direct_timesync_once", "GPS Zeitsync einmalig", "timesync einmal", ROUTE_DIRECT, "mdi:satellite-variant", False),
    CommandDescription("direct_timesync_off", "GPS Zeitsync aus", "timesync aus", ROUTE_DIRECT, "mdi:satellite-variant", False),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up MeshCore firmware command buttons."""
    async_add_entities(
        [MeshCoreCommandButton(entry, description) for description in COMMANDS]
    )


class MeshCoreCommandButton(ButtonEntity):
    """A button that sends one supported firmware command."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, entry: ConfigEntry, description: CommandDescription) -> None:
        """Initialize one command button."""
        self._entry = entry
        self._description = description
        participant = entry.data[CONF_PARTICIPANT]
        self._attr_name = description.name
        self._attr_icon = description.icon
        self._attr_unique_id = f"{entry.unique_id or entry.entry_id}_{description.key}"
        self._attr_entity_registry_enabled_default = description.enabled_default
        self._attr_device_info = DeviceInfo(
            identifiers={("meshcore_location", entry.unique_id or entry.entry_id)},
            name=entry.data[CONF_TRACKER_NAME],
            manufacturer="MeshCore",
            model=f"Telemetry Tracker ({participant})",
        )

    async def async_press(self) -> None:
        """Send the configured command."""
        await async_send_firmware_command(
            self.hass,
            self._entry,
            self._description.command,
            self._description.route,
        )

