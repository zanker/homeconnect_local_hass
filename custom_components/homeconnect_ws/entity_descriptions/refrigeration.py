"""Description for Cooking Entities."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass

from .descriptions_definitions import (
    HCBinarySensorEntityDescription,
    _EntityDescriptionsType,
)

REFRIGERATION_ENTITY_DESCRIPTIONS: _EntityDescriptionsType = {
    "binary_sensor": [
        HCBinarySensorEntityDescription(
            key="binary_sensor_freezer_door_state",
            entity="Refrigeration.Common.Status.Door.Freezer",
            device_class=BinarySensorDeviceClass.DOOR,
            value_on={"Open"},
            value_off={"Closed"},
        ),
        HCBinarySensorEntityDescription(
            key="binary_sensor_fridge_door_state",
            entity="Refrigeration.Common.Status.Door.Refrigerator",
            device_class=BinarySensorDeviceClass.DOOR,
            value_on={"Open"},
            value_off={"Closed"},
        ),
        HCBinarySensorEntityDescription(
            key="binary_sensor_freezer_door_state",
            entity="Refrigeration.FridgeFreezer.Status.DoorFreezer",
            device_class=BinarySensorDeviceClass.DOOR,
            value_on={"Open"},
            value_off={"Closed"},
        ),
        HCBinarySensorEntityDescription(
            key="binary_sensor_fridge_door_state",
            entity="Refrigeration.FridgeFreezer.Status.DoorRefrigerator",
            device_class=BinarySensorDeviceClass.DOOR,
            value_on={"Open"},
            value_off={"Closed"},
        ),
    ],
    "sensor": [],
}
