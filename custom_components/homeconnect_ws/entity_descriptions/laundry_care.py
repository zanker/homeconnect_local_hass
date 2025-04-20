"""Description for LaundryCare Entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.const import EntityCategory
from .descriptions_definitions import HCSensorEntityDescription, HCBinarySensorEntityDescription

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
    ],
    "binary_sensor": [
        HCBinarySensorEntityDescription(
            key="binary_sensor_refresher_level",
            entity="LaundryCare.Dryer.Status.RefresherFillLevel",
            entity_category=EntityCategory.DIAGNOSTIC,
            device_class=BinarySensorDeviceClass.PROBLEM,
            value_on=("Poor"),
            value_off=("Filled"),
        ),
    ],
}
