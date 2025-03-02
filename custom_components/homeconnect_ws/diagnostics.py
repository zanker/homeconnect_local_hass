"""Diagnostics support."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.const import CONF_DEVICE_ID

from .const import CONF_AES_IV, CONF_PSK

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeconnect_websocket import HomeAppliance

    from . import HCConfigEntry

TO_REDACT = [CONF_PSK, CONF_AES_IV, CONF_DEVICE_ID, "serialNumber", "deviceID", "shipSki", "mac"]


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HCConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "appliance_state": get_appliance_state(entry.runtime_data.appliance),
    }


def get_appliance_state(appliance: HomeAppliance) -> dict:
    """Convert the appliance state to a JSON-serializable dict."""
    appliance_state = {}
    for entity in appliance.entities.values():
        entity_state = {
            "name": entity.name,
            "uid": entity.uid,
            "value": entity.value,
            "value_raw": entity.value_raw,
            "enum": entity.enum,
        }
        if hasattr(entity, "access"):
            entity_state["access"] = entity.access
        if hasattr(entity, "available"):
            entity_state["available"] = entity.available
        if hasattr(entity, "min") and entity.min is not None:
            entity_state["min"] = entity.min
        if hasattr(entity, "max") and entity.max is not None:
            entity_state["max"] = entity.max
        if hasattr(entity, "step") and entity.step is not None:
            entity_state["step"] = entity.step

        appliance_state[entity.name] = entity_state
    return appliance_state
