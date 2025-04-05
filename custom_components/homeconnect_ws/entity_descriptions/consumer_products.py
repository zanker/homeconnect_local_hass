"""Description for ConsumerProducts Entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass

from .descriptions_definitions import (
    HCBinarySensorEntityDescription,
    HCSensorEntityDescription,
)

if TYPE_CHECKING:
    from .descriptions_definitions import _EntityDescriptionsType

CONSUMER_PRODUCTS_ENTITY_DESCRIPTIONS: _EntityDescriptionsType = {
    "binary_sensor": [
        HCBinarySensorEntityDescription(
            key="binary_sensor_bean_container_empty",
            entity="ConsumerProducts.CoffeeMaker.Event.BeanContainerEmpty",
            device_class=BinarySensorDeviceClass.PROBLEM,
            value_on={"Present"},
            value_off={"Off", "Confirmed"},
        ),
    ],
    "event_sensor": [
        HCSensorEntityDescription(
            key="sensor_water_tank",
            entities=[
                "ConsumerProducts.CoffeeMaker.Event.WaterTankEmpty",
                "ConsumerProducts.CoffeeMaker.Event.WaterTankNearlyEmpty",
                "ConsumerProducts.CoffeeMaker.Event.WaterTankNotInserted",
            ],
            device_class=SensorDeviceClass.ENUM,
            options=["empty", "nearly_empty", "not_inserted", "full"],
        )
    ],
}
