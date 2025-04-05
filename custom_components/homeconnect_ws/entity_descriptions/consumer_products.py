"""Description for ConsumerProducts Entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
)

from .descriptions_definitions import (
    HCSensorEntityDescription,
)

if TYPE_CHECKING:
    from .descriptions_definitions import (
        _EntityDescriptionsType,
    )

CONSUMER_PRODUCTS_ENTITY_DESCRIPTIONS: _EntityDescriptionsType = {
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
    ]
}
