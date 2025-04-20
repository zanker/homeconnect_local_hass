"""Description for LaundryCare Entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
)

from .descriptions_definitions import HCSensorEntityDescription

if TYPE_CHECKING:
    from .descriptions_definitions import _EntityDescriptionsType

LAUNDRY_ENTITY_DESCRIPTIONS: _EntityDescriptionsType = {
    "sensor": [
        HCSensorEntityDescription(
            key="sensor_laundry_reload",
            entity="LaundryCare.Common.Status.Laundry.Reload",
            device_class=SensorDeviceClass.ENUM,
            has_state_translation=True,
        ),
    ]
}
