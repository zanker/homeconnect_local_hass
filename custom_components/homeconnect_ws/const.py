"""Constants."""

from __future__ import annotations

from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "homeconnect_ws"
PLATFORMS: Final = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.SELECT,
    Platform.BUTTON,
    Platform.NUMBER,
]

CONF_PSK: Final = "psk"
CONF_AES_IV: Final = "aes_iv"
CONF_FILE: Final = "file"
