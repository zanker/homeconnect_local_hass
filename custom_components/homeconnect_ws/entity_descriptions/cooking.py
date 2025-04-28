"""Description for Cooking Entities."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTemperature, UnitOfTime

from custom_components.homeconnect_ws.helpers import get_groups_from_regex

from .descriptions_definitions import (
    EntityDescriptions,
    HCSensorEntityDescription,
    _EntityDescriptionsDefinitionsType,
)

if TYPE_CHECKING:
    from homeconnect_websocket import HomeAppliance


def generate_oven_status(appliance: HomeAppliance) -> EntityDescriptions:
    pattern = re.compile(r"^Cooking\.Oven\.Status\.Cavity\.(.*)\..*$")
    groups = get_groups_from_regex(appliance, pattern)
    descriptions = EntityDescriptions(event_sensor=[], sensor=[])
    for group in groups:
        group_name = int(group[0])
        if len(groups) == 1:
            group_name = ""

        # Water Tank
        entities = (
            f"Cooking.Oven.Status.Cavity.{group[0]}.WaterTankUnplugged",
            f"Cooking.Oven.Status.Cavity.{group[0]}.WaterTankEmpty",
        )
        if all(entity in appliance.entities for entity in entities):
            descriptions["event_sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_oven_water_tank_{group[0]}",
                    translation_key="sensor_oven_water_tank",
                    translation_placeholders={"group_name": group_name},
                    entities=entities,
                    device_class=SensorDeviceClass.ENUM,
                    options=["unplugged", "empty", "ok"],
                )
            )

        # Temperatur
        entity = f"Cooking.Oven.Status.Cavity.{group[0]}.CurrentTemperature"
        if entity in appliance.entities:
            descriptions["sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_oven_current_temperature_{group[0]}",
                    translation_key="sensor_oven_current_temperature",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    device_class=SensorDeviceClass.TEMPERATURE,
                    native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                )
            )

    return descriptions


COOKING_ENTITY_DESCRIPTIONS: _EntityDescriptionsDefinitionsType = {
    "sensor": [
        HCSensorEntityDescription(
            key="sensor_interval_time_off",
            entity="Cooking.Hood.Setting.IntervalTimeOff",
            device_class=SensorDeviceClass.DURATION,
            native_unit_of_measurement=UnitOfTime.SECONDS,
        ),
        HCSensorEntityDescription(
            key="sensor_interval_time_on",
            entity="Cooking.Hood.Setting.IntervalTimeOn",
            device_class=SensorDeviceClass.DURATION,
            native_unit_of_measurement=UnitOfTime.SECONDS,
        ),
        HCSensorEntityDescription(
            key="sensor_delayed_shutoff_time",
            entity="Cooking.Hood.Setting.DelayedShutOffTime",
            device_class=SensorDeviceClass.DURATION,
            native_unit_of_measurement=UnitOfTime.SECONDS,
        ),
    ],
    "dynamic": [generate_oven_status],
}
