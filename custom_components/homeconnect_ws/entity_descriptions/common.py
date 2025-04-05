"""Description for BSH.Common Entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfTime

from .descriptions_definitions import (
    HCBinarySensorEntityDescription,
    HCButtonEntityDescription,
    HCNumberEntityDescription,
    HCSelectEntityDescription,
    HCSensorEntityDescription,
    HCSwitchEntityDescription,
    _EntityDescriptionsType,
)

if TYPE_CHECKING:
    from homeconnect_websocket import HomeAppliance


POWER_SWITCH_VALUE_MAPINGS = (
    ("On", "MainsOff"),
    ("Standby", "MainsOff"),
    ("On", "Off"),
    ("On", "Standby"),
    ("Standby", "Off"),
)


def generate_power_switch(appliance: HomeAppliance) -> HCSwitchEntityDescription | None:
    """Get Power switch description."""
    if entity := appliance.entities.get("BSH.Common.Setting.PowerState"):
        settable_states = tuple(entity.enum.values())
        if entity.min and entity.max:
            # has min/max
            settable_states = set()
            for key, value in entity.enum.items():
                if int(key) >= entity.min and int(key) <= entity.max:
                    settable_states.add(value)
        else:
            settable_states = set(entity.enum.values())

        if len(settable_states) == 2:
            # only two power states
            for mapping in POWER_SWITCH_VALUE_MAPINGS:
                if settable_states == set(mapping):
                    return HCSwitchEntityDescription(
                        key="switch_power_state",
                        entity="BSH.Common.Setting.PowerState",
                        device_class=SwitchDeviceClass.SWITCH,
                        value_mapping=mapping,
                    )
    return None


COMMON_ENTITY_DESCRIPTIONS: _EntityDescriptionsType = {
    "abort_button": [
        HCButtonEntityDescription(
            key="button_abort_program",
            entity="BSH.Common.Command.AbortProgram",
        )
    ],
    "active_program": [
        HCSensorEntityDescription(
            key="sensor_active_program",
            entity="BSH.Common.Root.ActiveProgram",
            device_class=SensorDeviceClass.ENUM,
            has_state_translation=True,
        )
    ],
    "binary_sensor": [
        HCBinarySensorEntityDescription(
            key="binary_sensor_door_state",
            entity="BSH.Common.Status.DoorState",
            device_class=BinarySensorDeviceClass.DOOR,
            value_on={"Open"},
            value_off={"Closed"},
        ),
        HCBinarySensorEntityDescription(
            key="binary_sensor_aqua_stop",
            device_class=BinarySensorDeviceClass.PROBLEM,
            entity="BSH.Common.Event.AquaStopOccured",
            entity_registry_enabled_default=False,
            value_on={"Present"},
            value_off={"Off", "Confirmed"},
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
        HCBinarySensorEntityDescription(
            key="binary_sensor_low_water_pressure",
            device_class=BinarySensorDeviceClass.PROBLEM,
            entity="BSH.Common.Event.LowWaterPressure",
            entity_registry_enabled_default=False,
            value_on={"Present"},
            value_off={"Off", "Confirmed"},
            entity_category=EntityCategory.DIAGNOSTIC,
        ),
    ],
    "power_switch": [
        HCSwitchEntityDescription(
            key="switch_power_state",
            entity="BSH.Common.Setting.PowerState",
            device_class=SwitchDeviceClass.SWITCH,
        )
    ],
    "program": [
        HCSelectEntityDescription(
            key="select_program",
            entity="BSH.Common.Root.SelectedProgram",
            has_state_translation=True,
        )
    ],
    "select": [
        HCSelectEntityDescription(
            key="select_remote_control_level",
            entity="BSH.Common.Setting.RemoteControlLevel",
            entity_category=EntityCategory.CONFIG,
            entity_registry_enabled_default=False,
            has_state_translation=True,
        ),
    ],
    "sensor": [
        HCSensorEntityDescription(
            key="sensor_remaining_program_time",
            entity="BSH.Common.Option.RemainingProgramTime",
            device_class=SensorDeviceClass.DURATION,
            native_unit_of_measurement=UnitOfTime.SECONDS,
            suggested_unit_of_measurement=UnitOfTime.HOURS,
            extra_attributes=[
                {
                    "name": "Is Estimated",
                    "entity": "BSH.Common.Option.RemainingProgramTimeIsEstimated",
                }
            ],
        ),
        HCSensorEntityDescription(
            key="sensor_program_progress",
            entity="BSH.Common.Option.ProgramProgress",
            native_unit_of_measurement=PERCENTAGE,
        ),
        HCSensorEntityDescription(
            key="sensor_operation_state",
            entity="BSH.Common.Status.OperationState",
            device_class=SensorDeviceClass.ENUM,
        ),
        HCSensorEntityDescription(
            key="sensor_start_in",
            entity="BSH.Common.Option.StartInRelative",
            device_class=SensorDeviceClass.DURATION,
            native_unit_of_measurement=UnitOfTime.SECONDS,
            suggested_unit_of_measurement=UnitOfTime.HOURS,
        ),
        HCSensorEntityDescription(
            key="sensor_count_started",
            entity="BSH.Common.Status.Program.All.Count.Started",
            entity_category=EntityCategory.DIAGNOSTIC,
            entity_registry_enabled_default=False,
            state_class=SensorStateClass.TOTAL_INCREASING,
            extra_attributes=[
                {
                    "name": "Last Start",
                    "entity": "BSH.Common.Status.ProgramSessionSummary.Latest",
                    "value_fn": lambda entity: entity.value["start"],
                },
                {
                    "name": "Last End",
                    "entity": "BSH.Common.Status.ProgramSessionSummary.Latest",
                    "value_fn": lambda entity: entity.value["end"],
                },
            ],
        ),
        HCSensorEntityDescription(
            key="sensor_end_trigger",
            entity="BSH.Common.Status.ProgramRunDetail.EndTrigger",
            device_class=SensorDeviceClass.ENUM,
            entity_category=EntityCategory.DIAGNOSTIC,
            entity_registry_enabled_default=False,
            has_state_translation=True,
        ),
    ],
    "start_button": [
        HCButtonEntityDescription(
            key="button_start_program",
            entity="BSH.Common.Root.ActiveProgram",
        )
    ],
    "start_in": [
        HCNumberEntityDescription(
            key="select_start_in",
            entity="BSH.Common.Option.StartInRelative",
        )
    ],
    "switch": [generate_power_switch],
}
