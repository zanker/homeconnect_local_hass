"""Description for Cooking Entities."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from homeassistant.components.number import NumberDeviceClass, NumberMode
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfTemperature, UnitOfTime

from custom_components.homeconnect_ws.helpers import get_groups_from_regex, get_all_programs

from .descriptions_definitions import (
    EntityDescriptions,
    HCFanEntityDescription,
    HCLightEntityDescription,
    HCNumberEntityDescription,
    HCSelectEntityDescription,
    HCSensorEntityDescription,
    HCSwitchEntityDescription,
    HCBinarySensorEntityDescription,
    _EntityDescriptionsDefinitionsType,
)

if TYPE_CHECKING:
    from homeconnect_websocket import HomeAppliance

def add_if_entity_exists(appliance: HomeAppliance, list: Any, to_add: Any) -> None:
    if to_add.entity in appliance.entities:
        list.append(to_add)

def generate_oven_status(appliance: HomeAppliance) -> [EntityDescriptions]:
    """Get Oven status descriptions."""
    pattern = re.compile(r"^Cooking\.Oven\.Status\.Cavity\.([0-9]*)\..*$")
    groups = get_groups_from_regex(appliance, pattern)
    
    descriptions = EntityDescriptions(event_sensor=[], sensor=[], number=[], switch=[], select=[], binary_sensor=[])
    add_if_entity_exists(
        appliance,
        descriptions["select"],
        HCSelectEntityDescription(
            key="select_oven_cavity",
            entity=f"Cooking.Oven.Option.CavitySelector",
            translation_key="select_oven_cavity",
            device_class=SensorDeviceClass.ENUM,
            has_state_translation=True,
        )
    )

    add_if_entity_exists(
        appliance,
        descriptions["number"],
        HCNumberEntityDescription(
            key="number_oven_setpoint_temperature",
            entity="Cooking.Oven.Option.SetpointTemperatureFahrenheit",
            device_class=NumberDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
            mode=NumberMode.AUTO,
            step=5
        )
    )

    for group in groups:
        group_key = ""
        if int(group[0]) == 230:
            group_key = "upper"
            group_name = "Upper "
        if int(group[0]) == 140:
            group_key = "lower"
            group_name = "Lower "

        add_if_entity_exists(
            appliance,
            descriptions["binary_sensor"],
            HCBinarySensorEntityDescription(
                key=f"binary_sensor_oven_{group_key}_meatprobe_plugged",
                translation_key="binary_sensor_oven_meatprobe_plugged",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.MeatprobePlugged",
                entity_category=EntityCategory.DIAGNOSTIC
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_current_meatprobe_temperature",
                translation_key="sensor_oven_current_meatprobe_temperature",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.CurrentMeatprobeTemperatureFahrenheit",
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_setpoint_meatprobe_temperature",
                translation_key="sensor_oven_setpoint_meatprobe_temperature",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.MeatProbeTemperatureFahrenheit",
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["event_sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_regular_preheat",
                translation_key="sensor_regular_preheat_finished",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Event.Cavity.{group[0]}.RegularPreheatFinished",
                device_class=SensorDeviceClass.ENUM,
                has_state_translation=True,
                options=["off","present","confirmed"]
            )
        )        

        add_if_entity_exists(
            appliance,
            descriptions["event_sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_rfast_preheat",
                translation_key="sensor_fast_preheat_finished",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Event.Cavity.{group[0]}.FastPreheatFinished",
                device_class=SensorDeviceClass.ENUM,
                has_state_translation=True,
                options=["off","present","confirmed"]
            )
        )
         
        add_if_entity_exists(
            appliance,
            descriptions["switch"],
            HCSwitchEntityDescription(
                key=f"select_oven_{group_key}_light_power",
                entity=f"Cooking.Oven.Setting.Light.Cavity.{group[0]}.Power",
                translation_key="select_light_specific",
                translation_placeholders={"group_name": group_name},
                device_class=SwitchDeviceClass.SWITCH,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_cavity_state",
                translation_key="sensor_oven_cavity_state",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.State",
                device_class=SensorDeviceClass.ENUM,
                has_state_translation=True,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_current_temperature",
                translation_key="sensor_oven_current_temperature",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.CurrentTemperatureFahrenheit",
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_power_state",
                translation_key="sensor_specific_power_state",
                translation_placeholders={"group_name": group_name},
                entity="BSH.Common.Setting.PowerState",
                device_class=SensorDeviceClass.ENUM,
                has_state_translation=True,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_setpoint_temperature",
                translation_key="sensor_oven_setpoint_temperature",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.SetpointTemperatureFahrenheit",
                device_class=SensorDeviceClass.TEMPERATURE,
                native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_door_state",
                translation_key="sensor_door_state_specific",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.DoorState",
                device_class=SensorDeviceClass.ENUM,
                has_state_translation=True,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_operation_state",
                translation_key="sensor_operation_state_specific",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.OperationState",
                device_class=SensorDeviceClass.ENUM,
                has_state_translation=True,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_active_program",
                translation_key="sensor_active_program_specific",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.ActiveProgram",
                has_state_translation=False,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_selected_program",
                translation_key="sensor_selected_program_specific",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.SelectedProgram",
                has_state_translation=False,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_elapsed_program_time",
                translation_key="sensor_oven_elapsed_program_time",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.ElapsedProgramTime",
                device_class=SensorDeviceClass.DURATION,
                native_unit_of_measurement=UnitOfTime.SECONDS,
                suggested_unit_of_measurement=UnitOfTime.HOURS,
            )
        )

        add_if_entity_exists(
            appliance,
            descriptions["sensor"],
            HCSensorEntityDescription(
                key=f"sensor_oven_{group_key}_remaining_program_time",
                translation_key="sensor_oven_remaining_program_time",
                translation_placeholders={"group_name": group_name},
                entity=f"Cooking.Oven.Status.Cavity.{group[0]}.RemainingProgramTime",
                device_class=SensorDeviceClass.DURATION,
                native_unit_of_measurement=UnitOfTime.SECONDS,
                suggested_unit_of_measurement=UnitOfTime.HOURS,
            )
        )

    return descriptions

COOKING_ENTITY_DESCRIPTIONS: _EntityDescriptionsDefinitionsType = {
    "sensor": [
    ],
    "dynamic": [generate_oven_status],
    "number": [
        HCNumberEntityDescription(
            key="number_oven_setpoint_temperature",
            entity="Cooking.Oven.Option.SetpointTemperature",
            device_class=NumberDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            mode=NumberMode.AUTO,
        ),
    ],
    "select": [
    ],
    "switch": [
    ],
    "light": [
    ],
    "fan": [],
}