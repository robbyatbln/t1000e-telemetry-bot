"""Set up the MeshCore Location integration."""

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv

from .const import (
    ATTR_COMMAND,
    ATTR_ROUTE,
    CONF_CHANNEL_IDX,
    CONF_MESHCORE_ENTRY_ID,
    CONF_PARTICIPANT,
    DOMAIN,
    PLATFORMS,
    ROUTE_CHANNEL,
    ROUTE_DIRECT,
    SERVICE_SEND_COMMAND,
)

SERVICE_SCHEMA = vol.Schema(
    {
        vol.Required("entry_id"): cv.string,
        vol.Required(ATTR_COMMAND): cv.string,
        vol.Optional(ATTR_ROUTE, default=ROUTE_CHANNEL): vol.In(
            [ROUTE_CHANNEL, ROUTE_DIRECT]
        ),
    }
)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up services exposed by MeshCore Location."""
    _async_register_services(hass)
    return True


def _async_register_services(hass: HomeAssistant) -> None:
    """Register integration services once."""
    if hass.services.has_service(DOMAIN, SERVICE_SEND_COMMAND):
        return

    async def async_send_command(call) -> None:
        entry = hass.config_entries.async_get_entry(call.data["entry_id"])
        if entry is None or entry.domain != DOMAIN:
            raise HomeAssistantError("MeshCore Location config entry not found")
        await async_send_firmware_command(
            hass,
            entry,
            call.data[ATTR_COMMAND],
            call.data[ATTR_ROUTE],
        )

    hass.services.async_register(
        DOMAIN, SERVICE_SEND_COMMAND, async_send_command, schema=SERVICE_SCHEMA
    )


async def async_send_firmware_command(
    hass: HomeAssistant, entry: ConfigEntry, command: str, route: str
) -> None:
    """Send one firmware command using the existing Meshcore integration."""
    meshcore_entry_id = entry.data.get(CONF_MESHCORE_ENTRY_ID)
    service_data: dict[str, object] = {}
    if meshcore_entry_id:
        service_data["entry_id"] = meshcore_entry_id

    if route == ROUTE_DIRECT:
        service_data.update(
            {
                "node_id": entry.data[CONF_PARTICIPANT],
                "message": f"config {command}",
            }
        )
        await hass.services.async_call(
            "meshcore", "send_message", service_data, blocking=True
        )
        return

    service_data.update(
        {
            "channel_idx": int(entry.data[CONF_CHANNEL_IDX]),
            "message": f"config {entry.data[CONF_PARTICIPANT]} {command}",
        }
    )
    await hass.services.async_call(
        "meshcore", "send_channel_message", service_data, blocking=True
    )


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MeshCore Location from a config entry."""
    _async_register_services(hass)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a MeshCore Location config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
