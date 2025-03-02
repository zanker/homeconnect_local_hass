"""Sensor entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeconnect_websocket import HomeAppliance

from .entity import HCEntity
from .entity_description import (
    ACTIVE_PROGRAM_DESCRIPTIONS,
    EVENT_SENSOR_DESCRIPTIONS,
    SENSOR_DESCRIPTIONS,
    HCSensorEntityDescription,
)
from .helpers import get_entities_available

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity import DeviceInfo
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeconnect_websocket import HomeAppliance

    from . import HCConfigEntry

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    config_entry: HCConfigEntry,
    async_add_entites: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    appliance = config_entry.runtime_data.appliance
    device_info = config_entry.runtime_data.device_info
    entities = [
        HCSensor(entity_description, appliance, device_info)
        for entity_description in get_entities_available(SENSOR_DESCRIPTIONS, appliance)
    ]
    entities += [
        HCEventSensor(entity_description, appliance, device_info)
        for entity_description in get_entities_available(EVENT_SENSOR_DESCRIPTIONS, appliance)
    ]
    if ACTIVE_PROGRAM_DESCRIPTIONS.entity in appliance.entities:
        entities.append(HCActiveProgram(ACTIVE_PROGRAM_DESCRIPTIONS, appliance, device_info))
    async_add_entites(entities)


class HCSensor(HCEntity, SensorEntity):
    """Sensor Entity."""

    entity_description: HCSensorEntityDescription

    def __init__(
        self,
        entity_description: HCSensorEntityDescription,
        appliance: HomeAppliance,
        device_info: DeviceInfo,
    ) -> None:
        super().__init__(entity_description, appliance, device_info)
        if self._entity.enum:
            if self.entity_description.has_state_translation:
                self._attr_options = [str(value).lower() for value in self._entity.enum.values()]
            else:
                self._attr_options = [str(value) for value in self._entity.enum.values()]

    @property
    def native_value(self) -> int | float | str:
        if self._entity.enum and self.entity_description.has_state_translation:
            return str(self._entity.value).lower()
        return self._entity.value


class HCEventSensor(HCEntity, SensorEntity):
    """Event Sensor Entity."""

    entity_description: HCSensorEntityDescription

    async def async_added_to_hass(self) -> None:
        for entity in self._entities:
            entity.register_callback(self.callback)

    async def async_will_remove_from_hass(self) -> None:
        for entity in self._entities:
            entity.unregister_callback(self.callback)

    @property
    def native_value(self) -> str:
        for entity, value in zip(self._entities, self.entity_description.options, strict=False):
            if entity.value == "Present":
                return value
        return self.entity_description.options[-1]

    @property
    def available(self) -> bool:
        return self._appliance.session.connected


class HCActiveProgram(HCSensor):
    """Active Program Sensor Entity."""

    entity_description: HCSensorEntityDescription

    def __init__(
        self,
        entity_description: HCSensorEntityDescription,
        appliance: HomeAppliance,
        device_info: DeviceInfo,
    ) -> None:
        super().__init__(entity_description, appliance, device_info)
        self._attr_options = [name.split(".")[-1].lower() for name in self._appliance.programs]

    @property
    def native_value(self) -> int | float | str | None:
        return (
            self._appliance.active_program.name.split(".")[-1].lower()
            if self._appliance.active_program
            else None
        )
