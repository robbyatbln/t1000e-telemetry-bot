"""Config flow for MeshCore Location."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    BooleanSelector,
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
)

from .const import (
    CONF_CHANNEL_IDX,
    CONF_CHANNEL_NAME,
    CONF_CHANNEL_SELECTION,
    CONF_MESHCORE_ENTRY_ID,
    CONF_PARTICIPANT,
    CONF_PERSON_ENTITY,
    CONF_SOURCE_ENTITY,
    CONF_TRACKER_NAME,
    DOMAIN,
)
from .discovery import apply_channel_selection, async_logbook_messages, available_channels
from .parser import find_participants, parse_location, text_values

CONF_CONFIRM = "confirm"


class MeshCoreLocationConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MeshCore Location."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the setup values."""
        self._data: dict[str, Any] = {}
        self._detected_participants: list[str] = []
        self._channels: list[dict[str, Any]] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Select one configured channel exposed by the MeshCore integration."""
        self._channels = available_channels(self.hass)
        if user_input is not None:
            self._data.update(user_input)
            apply_channel_selection(self._data, self._channels)
            self._detected_participants = find_participants(
                await self._async_source_messages()
            )
            return await self.async_step_participant()

        if not self._channels:
            return self.async_abort(reason="no_channels")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_CHANNEL_SELECTION): SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                {"value": choice["value"], "label": choice["label"]}
                                for choice in self._channels
                            ],
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    )
                }
            ),
        )

    async def async_step_participant(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Choose or type the MeshCore participant to track."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_person()

        options = self._detected_participants
        participant_field = vol.Required(CONF_PARTICIPANT)
        if options:
            participant_field = vol.Required(CONF_PARTICIPANT, default=options[0])
        return self.async_show_form(
            step_id="participant",
            description_placeholders={
                "participants": ", ".join(self._detected_participants)
                or "Keine Teilnehmer in der aktuellen Nachricht gefunden"
            },
            data_schema=vol.Schema(
                {
                    participant_field: SelectSelector(
                        SelectSelectorConfig(
                            options=options,
                            custom_value=True,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    )
                }
            ),
        )

    async def _async_source_messages(self) -> list[str]:
        """Read visible logbook messages and any useful current attributes."""
        entity_id = self._data.get(CONF_SOURCE_ENTITY)
        messages = await async_logbook_messages(self.hass, entity_id)
        state = self.hass.states.get(entity_id) if entity_id else None
        if state is not None:
            messages.extend(text_values(state.state, dict(state.attributes)))
        return messages

    async def async_step_person(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Choose the existing HA person and tracker name."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_confirm()

        participant = self._data[CONF_PARTICIPANT]
        default_name = f"{participant} MeshCore"
        return self.async_show_form(
            step_id="person",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PERSON_ENTITY): EntitySelector(
                        EntitySelectorConfig(domain="person")
                    ),
                    vol.Required(
                        CONF_TRACKER_NAME, default=default_name
                    ): TextSelector(),
                }
            ),
        )

    async def async_step_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm the parsed position before creating the tracker."""
        parsed = parse_location(
            await self._async_source_messages(),
            self._data[CONF_PARTICIPANT],
        )
        coordinate = (
            f"{parsed.latitude}, {parsed.longitude}"
            if parsed is not None
            else "Noch keine passende GPS-Nachricht erkannt"
        )

        if user_input is not None:
            unique_id = (
                f"{self._data[CONF_MESHCORE_ENTRY_ID]}::"
                f"{int(self._data[CONF_CHANNEL_IDX])}::"
                f"{self._data[CONF_PARTICIPANT]}"
            )
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=self._data[CONF_TRACKER_NAME],
                data=self._data,
            )

        return self.async_show_form(
            step_id="confirm",
            description_placeholders={
                "source_entity": self._data[CONF_SOURCE_ENTITY],
                "channel_idx": (
                    f"{self._data[CONF_CHANNEL_NAME]} "
                    f"({int(self._data[CONF_CHANNEL_IDX])})"
                ),
                "participant": self._data[CONF_PARTICIPANT],
                "person_entity": self._data[CONF_PERSON_ENTITY],
                "coordinate": coordinate,
            },
            data_schema=vol.Schema(
                {vol.Required(CONF_CONFIRM, default=True): BooleanSelector()}
            ),
        )
