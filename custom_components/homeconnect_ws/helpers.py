"""Helper functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from homeconnect_websocket import HomeAppliance

    from .entity_descriptions import HCEntityDescription


def get_entities_available(
    entity_descriptions: Sequence[HCEntityDescription], appliance: HomeAppliance
) -> list[HCEntityDescription]:
    """Get all entity_descriptions available for this appliance."""
    valid_entities_descriptions = []
    for entity in entity_descriptions:
        all_subscribed_entities = []
        if entity.entity:
            all_subscribed_entities.append(entity.entity)
        if entity.entities:
            all_subscribed_entities.extend(entity.entities)
        if set(all_subscribed_entities).intersection(appliance.entities):
            valid_entities_descriptions.append(entity)
    return valid_entities_descriptions
