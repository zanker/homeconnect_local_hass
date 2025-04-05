"""Description for Cooking Entities."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
)

from .descriptions_definitions import (
    HCBinarySensorEntityDescription,
    HCEntityDescription,
)

REFRIGERATION_ENTITY_DESCRIPTIONS: dict[str, list[HCEntityDescription]] = {
    "binary_sensor": [
        HCBinarySensorEntityDescription(
            key="binary_sensor_door_state",
            entity="Refrigeration.Common.Status.Door.Freezer",
            device_class=BinarySensorDeviceClass.DOOR,
            value_on={"Open"},
            value_off={"Closed"},
        ),
        HCBinarySensorEntityDescription(
            key="binary_sensor_door_state",
            entity="Refrigeration.Common.Status.Door.Refrigerator",
            device_class=BinarySensorDeviceClass.DOOR,
            value_on={"Open"},
            value_off={"Closed"},
        ),
    ]
}
