"""Description for Cooking Entities."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.number import NumberDeviceClass, NumberMode
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.const import UnitOfTemperature

from .descriptions_definitions import (
    HCBinarySensorEntityDescription,
    HCNumberEntityDescription,
    HCSensorEntityDescription,
    HCSwitchEntityDescription,
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
    "sensor": [
        HCSensorEntityDescription(
            key="sensor_temperature_ambient",
            entity="Refrigeration.FridgeFreezer.Status.TemperatureAmbient",
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        )
    ],
    "number": [
        HCNumberEntityDescription(
            key="number_setpoint_freezer",
            entity="Refrigeration.FridgeFreezer.Setting.SetpointTemperatureFreezer",
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            device_class=NumberDeviceClass.TEMPERATURE,
            mode=NumberMode.AUTO,
            step=1,
        ),
        HCNumberEntityDescription(
            key="number_setpoint_refrigerator",
            entity="Refrigeration.FridgeFreezer.Setting.SetpointTemperatureRefrigerator",
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            device_class=NumberDeviceClass.TEMPERATURE,
            mode=NumberMode.AUTO,
            step=1,
        ),
    ],
    "switch": [
        HCSwitchEntityDescription(
            key="switch_super_freezer",
            entity="Refrigeration.FridgeFreezer.Setting.SuperModeFreezer",
            device_class=SwitchDeviceClass.SWITCH,
        ),
        HCSwitchEntityDescription(
            key="switch_super_refrigerator",
            entity="Refrigeration.FridgeFreezer.Setting.SuperModeRefrigerator",
            device_class=SwitchDeviceClass.SWITCH,
        ),
    ],
}
