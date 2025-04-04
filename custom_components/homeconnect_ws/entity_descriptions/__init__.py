"""Description for all supported Entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .common import ENTITY_DESCRIPTIONS
from .descriptions_definitions import (
    HCBinarySensorEntityDescription,
    HCButtonEntityDescription,
    HCEntityDescription,
    HCNumberEntityDescription,
    HCSelectEntityDescription,
    HCSensorEntityDescription,
    HCSwitchEntityDescription,
)

if TYPE_CHECKING:
    from homeconnect_websocket import HomeAppliance

    from .descriptions_definitions import EntityDescriptions


def get_available_entities(appliance: HomeAppliance) -> EntityDescriptions:
    """Get all available Entity descriptions."""
    available_entities: dict[str, list[HCEntityDescription]] = {
        "abort_button": [],
        "active_program": [],
        "binary_sensor": [],
        "event_sensor": [],
        "number": [],
        "power_switch": [],
        "program": [],
        "select": [],
        "sensor": [],
        "start_button": [],
        "start_in": [],
        "switch": [],
    }
    for description_type, descriptions in ENTITY_DESCRIPTIONS.items():
        for description in descriptions:
            all_subscribed_entities = []
            if description.entity:
                all_subscribed_entities.append(description.entity)
            if description.entities:
                all_subscribed_entities.extend(description.entities)
            if set(all_subscribed_entities).intersection(appliance.entities):
                available_entities[description_type].append(description)
    return available_entities


__all__ = [
    "HCBinarySensorEntityDescription",
    "HCButtonEntityDescription",
    "HCEntityDescription",
    "HCNumberEntityDescription",
    "HCSelectEntityDescription",
    "HCSensorEntityDescription",
    "HCSwitchEntityDescription",
    "get_available_entities",
]
