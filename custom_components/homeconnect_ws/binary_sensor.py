"""Binary Sensor entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorEntity

from .entity import HCEntity
from .entity_description import (
    BINARY_SENSOR_DESCRIPTIONS,
    CONNECTION_SENSOR_DESCRIPTIONS,
)
from .helpers import get_entities_available

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.device_registry import DeviceInfo
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeconnect_websocket import HomeAppliance

    from . import HCConfigEntry
    from .entity_descriptions import HCBinarySensorEntityDescription

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    config_entry: HCConfigEntry,
    async_add_entites: AddEntitiesCallback,
) -> None:
    """Set up binary_sensor platform."""
    entities: list[BinarySensorEntity] = []
    appliance = config_entry.runtime_data.appliance
    device_info = config_entry.runtime_data.device_info
    entities = [
        HCBinarySensor(entity_description, appliance, device_info)
        for entity_description in get_entities_available(BINARY_SENSOR_DESCRIPTIONS, appliance)
    ]
    entities.append(
        HCConnectionSensor(
            CONNECTION_SENSOR_DESCRIPTIONS,
            appliance,
            device_info,
        )
    )
    async_add_entites(entities)


class HCBinarySensor(HCEntity, BinarySensorEntity):
    """Binary Sensor Entity."""

    entity_description: HCBinarySensorEntityDescription

    @property
    def is_on(self) -> bool:
        if self.entity_description.value_on:
            if self._entity.value in self.entity_description.value_on:
                return True
            if self._entity.value in self.entity_description.value_off:
                return False
            return None
        return bool(self._entity.value)


class HCConnectionSensor(BinarySensorEntity):
    """Connection sensor Entity."""

    _attr_has_entity_name = True
    _attr_should_poll = True
    _attr_available = True
    entity_description: HCBinarySensorEntityDescription

    def __init__(
        self,
        entity_description: HCBinarySensorEntityDescription,
        appliance: HomeAppliance,
        device_info: DeviceInfo,
    ) -> None:
        super().__init__()
        self._appliance: HomeAppliance = appliance
        self.entity_description = entity_description
        self._attr_unique_id = f"{appliance.info['deviceID']}-{entity_description.key}"
        self._attr_device_info: DeviceInfo = device_info
        self._attr_translation_key = entity_description.key

    @property
    def is_on(self) -> bool:
        return self._appliance.session.connected
