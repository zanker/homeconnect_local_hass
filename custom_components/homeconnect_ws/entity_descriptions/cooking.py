"""Description for Cooking Entities."""

from __future__ import annotations

import re
import sys
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
    HCBinarySensorEntityDescription,
    HCButtonEntityDescription,
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
    pattern = re.compile(r"^Cooking\.Oven\.Status\.Cavity\.(\d+)\..*$")
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


def generate_oven_event(appliance: HomeAppliance) -> EntityDescriptions:
    """Get Oven event descriptions."""
    pattern = re.compile(r"^Cooking\.Oven\.Event\.Cavity\.([0-9]*)\..*$")
    groups = get_groups_from_regex(appliance, pattern)
    descriptions = EntityDescriptions(binary_sensor=[])
    for group in groups:
        group_name = f" {int(group[0])}"
        if len(groups) == 1:
            group_name = ""

        # AlarmClockElapsed
        entity = f"Cooking.Oven.Event.Cavity.{group[0]}.AlarmClockElapsed"
        if entity in appliance.entities:
            descriptions["binary_sensor"].append(
                HCBinarySensorEntityDescription(
                    key=f"binary_sensor_oven_alarm_clock_elapsed_{group[0]}",
                    translation_key="binary_sensor_oven_alarm_clock_elapsed",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    value_on={"Present", "Confirmed"},
                    value_off={"Off"},
                )
            )

    return descriptions


def generate_oven_settings(appliance: HomeAppliance) -> HCFanEntityDescription:
    """Get Oven status descriptions."""
    pattern = re.compile(r"^Cooking\.Oven\.Setting\.Cavity\.([0-9]*)\..*$")
    groups = get_groups_from_regex(appliance, pattern)
    descriptions = EntityDescriptions(number=[])
    for group in groups:
        group_name = f" {int(group[0])}"

        # AlarmClock
        entity = f"Cooking.Oven.Setting.Cavity.{group[0]}.AlarmClock"
        if entity in appliance.entities:
            descriptions["number"].append(
                HCNumberEntityDescription(
                    key=f"number_oven_setting_{group[0]}_alarm_clock",
                    translation_key="number_oven_setting_alarm_clock",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    device_class=NumberDeviceClass.DURATION,
                    native_unit_of_measurement=UnitOfTime.SECONDS,
                    native_max_value=sys.float_info.max,
                    mode=NumberMode.BOX,
                )
            )

    return descriptions


HOOD_FAN_ENTITIES = [
    "Cooking.Common.Option.Hood.VentingLevel",
    "Cooking.Common.Option.Hood.IntensiveLevel",
]


def generate_hood_fan(appliance: HomeAppliance) -> HCFanEntityDescription:
    """Get Hood Fan description."""
    available_entities = [entity for entity in HOOD_FAN_ENTITIES if entity in appliance.entities]
    if available_entities:
        return HCFanEntityDescription(key="fan_hood", entities=available_entities)
    return None


def generate_hob_zones(appliance: HomeAppliance) -> HCFanEntityDescription:
    """Get Oven status descriptions."""
    pattern = re.compile(r"^Cooking\.Hob\.Status\.Zone\.([0-9]*)\..*$")
    groups = get_groups_from_regex(appliance, pattern)
    descriptions = EntityDescriptions(sensor=[])
    for group in groups:
        group_name = f" {int(group[0])}"

        # State
        entity = f"Cooking.Hob.Status.Zone.{group[0]}.State"
        if entity in appliance.entities:
            descriptions["sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_hob_zone_{group[0]}_state",
                    translation_key="sensor_hob_zone_state",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    device_class=SensorDeviceClass.ENUM,
                    has_state_translation=True,
                    extra_attributes=[
                        {
                            "name": "Type",
                            "entity": f"Cooking.Hob.Status.Zone.{group[0]}.Type",
                        }
                    ],
                )
            )

        # OperationState
        entity = f"Cooking.Hob.Status.Zone.{group[0]}.OperationState"
        if entity in appliance.entities:
            descriptions["sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_hob_zone_{group[0]}_operationstate",
                    translation_key="sensor_hob_zone_operationstate",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    device_class=SensorDeviceClass.ENUM,
                    has_state_translation=True,
                )
            )

        # PowerLevel
        entity = f"Cooking.Hob.Status.Zone.{group[0]}.PowerLevel"
        if entity in appliance.entities:
            descriptions["sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_hob_zone_{group[0]}_power_level",
                    translation_key="sensor_hob_zone_power_level",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    device_class=SensorDeviceClass.ENUM,
                    has_state_translation=True,
                )
            )

        # FryingSensorLevel
        entity = f"Cooking.Hob.Status.Zone.{group[0]}.FryingSensorLevel"
        if entity in appliance.entities:
            descriptions["sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_hob_zone_{group[0]}_frying_sensor_level",
                    translation_key="sensor_hob_zone_frying_sensor_level",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    device_class=SensorDeviceClass.ENUM,
                    has_state_translation=True,
                )
            )

        # CurrentTemperature
        entity = f"Cooking.Hob.Status.Zone.{group[0]}.CurrentTemperature"
        if entity in appliance.entities:
            descriptions["sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_hob_zone_{group[0]}_current_temperature",
                    translation_key="sensor_hob_zone_current_temperature",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    device_class=SensorDeviceClass.TEMPERATURE,
                    native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                )
            )

        # HeatupProgress
        entity = f"Cooking.Hob.Status.Zone.{group[0]}.HeatupProgress"
        if entity in appliance.entities:
            descriptions["sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_hob_zone_{group[0]}_heatup_progress",
                    translation_key="sensor_hob_zone_heatup_progress",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    native_unit_of_measurement=PERCENTAGE,
                )
            )

        # Duration
        entity = f"Cooking.Hob.Status.Zone.{group[0]}.Duration"
        if entity in appliance.entities:
            descriptions["sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_hob_zone_{group[0]}_duration",
                    translation_key="sensor_hob_zone_duration",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    device_class=SensorDeviceClass.DURATION,
                    native_unit_of_measurement=UnitOfTime.SECONDS,
                    suggested_unit_of_measurement=UnitOfTime.MINUTES,
                )
            )

        # ElapsedProgramTime
        entity = f"Cooking.Hob.Status.Zone.{group[0]}.ElapsedProgramTime"
        extra_entity = f"Cooking.Hob.Status.Zone.{group[0]}.ElapsedProgramTime.AutoCounting"
        if entity in appliance.entities:
            descriptions["sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_hob_zone_{group[0]}_elapsed_program_time",
                    translation_key="sensor_hob_zone_elapsed_program_time",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    device_class=SensorDeviceClass.DURATION,
                    native_unit_of_measurement=UnitOfTime.SECONDS,
                    suggested_unit_of_measurement=UnitOfTime.MINUTES,
                    extra_attributes=[{"name": "Auto Counting", "entity": extra_entity}],
                )
            )

        # RemainingProgramTime
        entity = f"Cooking.Hob.Status.Zone.{group[0]}.RemainingProgramTime"
        extra_entity = f"Cooking.Hob.Status.Zone.{group[0]}.RemainingProgramTime.AutoCounting"
        if entity in appliance.entities:
            descriptions["sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_hob_zone_{group[0]}_remaining_program_time",
                    translation_key="sensor_hob_zone_remaining_program_time",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    device_class=SensorDeviceClass.DURATION,
                    native_unit_of_measurement=UnitOfTime.SECONDS,
                    suggested_unit_of_measurement=UnitOfTime.MINUTES,
                    extra_attributes=[{"name": "Auto Counting", "entity": extra_entity}],
                )
            )

        # ProgramProgress
        entity = f"Cooking.Hob.Status.Zone.{group[0]}.ProgramProgress"
        if entity in appliance.entities:
            descriptions["sensor"].append(
                HCSensorEntityDescription(
                    key=f"sensor_hob_zone_{group[0]}_program_progress",
                    translation_key="sensor_hob_zone_program_progress",
                    translation_placeholders={"group_name": group_name},
                    entity=entity,
                    native_unit_of_measurement=PERCENTAGE,
                )
            )

    return descriptions


def generate_hood_light(appliance: HomeAppliance) -> HCFanEntityDescription:
    """Get Hood light descriptions."""
    if "Cooking.Hood.Setting.ColorTemperaturePercent" in appliance.entities:
        return HCLightEntityDescription(
            key="light_cooking_lighting",
            entity="Cooking.Common.Setting.Lighting",
            brightness_entity="Cooking.Common.Setting.LightingBrightness",
            color_temperature_entity="Cooking.Hood.Setting.ColorTemperaturePercent",
        )

    if (
        "Cooking.Hood.Setting.LightingBrightness" in appliance.entities
        or "Cooking.Common.Setting.LightingBrightness" in appliance.entities
    ):
        return HCLightEntityDescription(
            key="light_cooking_lighting",
            entity="Cooking.Common.Setting.Lighting",
            brightness_entity="Cooking.Common.Setting.LightingBrightness",
        )

    if "Cooking.Common.Setting.Lighting" in appliance.entities:
        return HCLightEntityDescription(
            key="light_cooking_lighting",
            entity="Cooking.Common.Setting.Lighting",
        )
    return None


def generate_hood_ambient_light(appliance: HomeAppliance) -> HCFanEntityDescription:
    """Get Hood light descriptions."""
    if (
        "BSH.Common.Setting.AmbientLightCustomColor" in appliance.entities
        and "BSH.Common.Setting.AmbientLightColor" in appliance.entities
    ):
        return HCLightEntityDescription(
            key="light_cooking_ambient_lighting",
            entity="BSH.Common.Setting.AmbientLightEnabled",
            brightness_entity="BSH.Common.Setting.AmbientLightBrightness",
            color_entity="BSH.Common.Setting.AmbientLightCustomColor",
            color_mode_entity="BSH.Common.Setting.AmbientLightColor",
        )

    if "BSH.Common.Setting.AmbientLightBrightness" in appliance.entities:
        return HCLightEntityDescription(
            key="light_cooking_ambient_lighting",
            entity="BSH.Common.Setting.AmbientLightEnabled",
            brightness_entity="BSH.Common.Setting.AmbientLightBrightness",
        )

    if "BSH.Common.Setting.AmbientLightEnabled" in appliance.entities:
        return HCLightEntityDescription(
            key="light_cooking_ambient_lighting",
            entity="BSH.Common.Setting.AmbientLightEnabled",
        )
    return None


COOKING_ENTITY_DESCRIPTIONS: _EntityDescriptionsDefinitionsType = {
    "sensor": [
    ],
    "dynamic": [
        generate_oven_status,
        generate_hob_zones,
        generate_oven_event,
        generate_oven_settings,
    ],
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
        HCSelectEntityDescription(
            key="select_oven_level",
            entity="Cooking.Oven.Option.Level",
            has_state_translation=True,
        ),
        HCSelectEntityDescription(
            key="select_oven_used_heating_mode",
            entity="Cooking.Oven.Option.UsedHeatingMode",
            has_state_translation=True,
        ),
        HCSelectEntityDescription(
            key="select_pyrolysis_level",
            entity="Cooking.Oven.Option.PyrolysisLevel",
            has_state_translation=True,
        ),
        HCSelectEntityDescription(
            key="select_oven_child_lock_setting",
            entity="Cooking.Oven.Setting.ConfigureChildLock",
            has_state_translation=True,
            entity_category=EntityCategory.CONFIG,
        ),
        HCSelectEntityDescription(
            key="select_oven_switch_on_delay",
            entity="Cooking.Oven.Setting.SwitchOnDelay",
            has_state_translation=True,
            entity_category=EntityCategory.CONFIG,
        ),
        HCSelectEntityDescription(
            key="select_oven_cooling_fan_runtime",
            entity="Cooking.Oven.Setting.CoolingFanRunOnTime",
            has_state_translation=True,
            entity_category=EntityCategory.CONFIG,
        ),
        HCSelectEntityDescription(
            key="select_oven_signal_duration",
            entity="Cooking.Oven.Setting.SignalDuration",
            has_state_translation=True,
            entity_category=EntityCategory.CONFIG,
        ),
        HCSelectEntityDescription(
            key="select_hood_interval_stage",
            entity="Cooking.Hood.Setting.IntervalStage",
            has_state_translation=True,
        ),
        HCSelectEntityDescription(
            key="select_hob_ventilation",
            entity="Cooking.Hob.Setting.Ventilation",
            has_state_translation=True,
            entity_category=EntityCategory.CONFIG,
        ),
        HCSelectEntityDescription(
            key="select_hob_delaye_shutoff_stage",
            entity="Cooking.Hood.Setting.DelayedShutOffStage",
            has_state_translation=True,
        ),
        HCSelectEntityDescription(
            key="select_hood_carbon_filter_type",
            entity="Cooking.Hood.Setting.CarbonFilterType",
            has_state_translation=True,
            entity_category=EntityCategory.CONFIG,
        ),
>>>>>>> remote/main
    ],
    "switch": [
    ],
    "light": [generate_hood_light, generate_hood_ambient_light],
    "fan": [generate_hood_fan],
    "button": [
        HCButtonEntityDescription(
            key="button_hood_carbon_filter_reset",
            entity="Cooking.Common.Command.Hood.CarbonFilterReset ",
            entity_category=EntityCategory.CONFIG,
        ),
        HCButtonEntityDescription(
            key="button_hood_grease_filter_reset",
            entity="Cooking.Common.Command.Hood.GreaseFilterReset ",
            entity_category=EntityCategory.CONFIG,
        ),
        HCButtonEntityDescription(
            key="button_hood_regenerative_carbon_filter_reset",
            entity="Cooking.Common.Command.Hood.RegenerativeCarbonFilterReset ",
            entity_category=EntityCategory.CONFIG,
        ),
        HCButtonEntityDescription(
            key="button_hood_regenerative_carbon_filter_lifetime_reset",
            entity="Cooking.Common.Command.Hood.RegenerativeCarbonFilterLifeTimeReset ",
            entity_category=EntityCategory.CONFIG,
        ),
    ],
}
