"""Constants for the MeshCore Location integration."""

from homeassistant.const import Platform

DOMAIN = "meshcore_location"
PLATFORMS: list[Platform] = [Platform.DEVICE_TRACKER, Platform.BUTTON]

CONF_CHANNEL_IDX = "channel_idx"
CONF_CHANNEL_NAME = "channel_name"
CONF_CHANNEL_SELECTION = "channel_selection"
CONF_MESHCORE_ENTRY_ID = "meshcore_entry_id"
CONF_SOURCE_ENTITY = "source_entity"
CONF_PARTICIPANT = "participant"
CONF_PERSON_ENTITY = "person_entity"
CONF_TRACKER_NAME = "tracker_name"

SERVICE_SEND_COMMAND = "send_command"
ATTR_COMMAND = "command"
ATTR_ROUTE = "route"
ROUTE_CHANNEL = "channel"
ROUTE_DIRECT = "direct"
