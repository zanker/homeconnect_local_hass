"""Tests for reauthflow."""

from __future__ import annotations

from binascii import Error as BinasciiError
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, MagicMock, Mock
from uuid import uuid4

from aiohttp import ClientConnectionError, ClientConnectorSSLError
from custom_components.homeconnect_ws import config_flow
from custom_components.homeconnect_ws.const import (
    CONF_AES_IV,
    CONF_FILE,
    CONF_PSK,
    DOMAIN,
)
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .const import (
    MOCK_AES_DEVICE_ID,
    MOCK_CONFIG_DATA,
)

if TYPE_CHECKING:
    import pytest
    from homeassistant.core import HomeAssistant

UPLOADED_FILE = str(uuid4())


async def test_reauth(
    hass: HomeAssistant,
    mock_process_profile_file: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test a reauthentication flow."""
    hc_socket = Mock()
    mock_hc_socket = Mock(return_value=AsyncMock())
    hc_socket.AesSocket = mock_hc_socket
    monkeypatch.setattr(config_flow, "hc_socket", hc_socket)

    mock_process_profile_file.return_value[MOCK_AES_DEVICE_ID]["info"]["key"] = "New_AES_PSK_KEY"
    mock_process_profile_file.return_value[MOCK_AES_DEVICE_ID]["info"]["iv"] = "New_AES_IV"

    mock_config = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG_DATA,
        unique_id=MOCK_AES_DEVICE_ID,
    )
    mock_config.add_to_hass(hass)

    result = await mock_config.start_reauth_flow(hass)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "upload"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_FILE: UPLOADED_FILE,
        },
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
    assert mock_config.data[CONF_PSK] == "New_AES_PSK_KEY"
    assert mock_config.data[CONF_AES_IV] == "New_AES_IV"

    mock_hc_socket.return_value.connect.assert_awaited_once()
    mock_hc_socket.return_value.close.assert_awaited_once()


async def test_reauth_appliance_not_in_profile(
    hass: HomeAssistant,
    mock_process_profile_file: MagicMock,  # noqa: ARG001
    mock_setup_entry: AsyncMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test a reauthentication flow when appliance not in profile."""
    hc_socket = Mock()
    mock_hc_socket = Mock(return_value=AsyncMock())
    hc_socket.AesSocket = mock_hc_socket
    monkeypatch.setattr(config_flow, "hc_socket", hc_socket)

    mock_config = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG_DATA,
        unique_id="other_id",
    )
    mock_config.add_to_hass(hass)
    result = await mock_config.start_reauth_flow(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_FILE: UPLOADED_FILE,
        },
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "appliance_not_in_profile_file"
    mock_setup_entry.assert_not_awaited()
    mock_hc_socket.assert_not_called()


async def test_reauth_auth_failed_ssl_error(
    hass: HomeAssistant,
    mock_process_profile_file: MagicMock,  # noqa: ARG001
    mock_setup_entry: AsyncMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test a reauthentication flow with ClientConnectorSSLError."""
    hc_socket = Mock()
    mock_hc_socket = Mock(return_value=AsyncMock())
    hc_socket.AesSocket = mock_hc_socket
    monkeypatch.setattr(config_flow, "hc_socket", hc_socket)

    mock_config = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG_DATA,
        unique_id=MOCK_AES_DEVICE_ID,
    )
    mock_config.add_to_hass(hass)

    mock_hc_socket.return_value.connect.side_effect = ClientConnectorSSLError(
        MagicMock(), MagicMock()
    )

    result = await mock_config.start_reauth_flow(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_FILE: UPLOADED_FILE,
        },
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "auth_failed"
    mock_hc_socket.return_value.close.assert_awaited_once()
    mock_setup_entry.assert_not_awaited()


async def test_reauth_auth_failed_binascii_error(
    hass: HomeAssistant,
    mock_process_profile_file: MagicMock,  # noqa: ARG001
    mock_setup_entry: AsyncMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test a reauthentication flow with BinasciiError."""
    hc_socket = Mock()
    mock_hc_socket = Mock(return_value=AsyncMock())
    hc_socket.AesSocket = mock_hc_socket
    monkeypatch.setattr(config_flow, "hc_socket", hc_socket)

    mock_config = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG_DATA,
        unique_id=MOCK_AES_DEVICE_ID,
    )
    mock_config.add_to_hass(hass)

    mock_hc_socket.return_value.connect.side_effect = BinasciiError(MagicMock(), MagicMock())

    result = await mock_config.start_reauth_flow(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_FILE: UPLOADED_FILE,
        },
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "auth_failed"
    mock_hc_socket.return_value.close.assert_awaited_once()
    mock_setup_entry.assert_not_awaited()


async def test_reauth_connection_failed_timeout(
    hass: HomeAssistant,
    mock_process_profile_file: MagicMock,  # noqa: ARG001
    mock_setup_entry: AsyncMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test a reauthentication flow with TimeoutError."""
    hc_socket = Mock()
    mock_hc_socket = Mock(return_value=AsyncMock())
    hc_socket.AesSocket = mock_hc_socket
    monkeypatch.setattr(config_flow, "hc_socket", hc_socket)

    mock_config = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG_DATA,
        unique_id=MOCK_AES_DEVICE_ID,
    )
    mock_config.add_to_hass(hass)

    mock_hc_socket.return_value.connect.side_effect = TimeoutError()

    result = await mock_config.start_reauth_flow(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_FILE: UPLOADED_FILE,
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "host"
    assert result["errors"]["base"] == "cannot_connect"

    mock_hc_socket.return_value.close.assert_awaited_once()
    hass.config_entries.flow.async_abort(result["flow_id"])
    mock_setup_entry.assert_not_awaited()


async def test_reauth_connection_failed_connection_error(
    hass: HomeAssistant,
    mock_process_profile_file: MagicMock,  # noqa: ARG001
    mock_setup_entry: AsyncMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test a reauthentication flow with ClientConnectionError."""
    hc_socket = Mock()
    mock_hc_socket = Mock(return_value=AsyncMock())
    hc_socket.AesSocket = mock_hc_socket
    monkeypatch.setattr(config_flow, "hc_socket", hc_socket)

    mock_config = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG_DATA,
        unique_id=MOCK_AES_DEVICE_ID,
    )
    mock_config.add_to_hass(hass)

    mock_hc_socket.return_value.connect.side_effect = ClientConnectionError()

    result = await mock_config.start_reauth_flow(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_FILE: UPLOADED_FILE,
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "host"
    assert result["errors"]["base"] == "cannot_connect"

    mock_hc_socket.return_value.close.assert_awaited_once()
    hass.config_entries.flow.async_abort(result["flow_id"])
    mock_setup_entry.assert_not_awaited()


async def test_reauth_invalid_config_parser(
    hass: HomeAssistant,
    mock_process_profile_file: MagicMock,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test a reauthentication flow with error in config parser."""
    mock_config = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG_DATA,
        unique_id=MOCK_AES_DEVICE_ID,
    )
    mock_config.add_to_hass(hass)

    mock_process_profile_file.side_effect = KeyError()

    result = await mock_config.start_reauth_flow(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_FILE: UPLOADED_FILE,
        },
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "invalid_profile_file"
    mock_setup_entry.assert_not_awaited()

    mock_process_profile_file.side_effect = ValueError()

    result = await mock_config.start_reauth_flow(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_FILE: UPLOADED_FILE,
        },
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "invalid_profile_file"
    mock_setup_entry.assert_not_awaited()


async def test_reauth_invalid_profile_no_info(
    hass: HomeAssistant,
    mock_process_profile_file: MagicMock,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test a reauthentication flow with no profile info."""
    mock_process_profile_file.return_value[MOCK_AES_DEVICE_ID] = {}

    mock_config = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG_DATA,
        unique_id=MOCK_AES_DEVICE_ID,
    )
    mock_config.add_to_hass(hass)

    result = await mock_config.start_reauth_flow(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_FILE: UPLOADED_FILE,
        },
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "invalid_profile_file"
    mock_setup_entry.assert_not_awaited()


async def test_reauth_invalid_profile_info(
    hass: HomeAssistant,
    mock_process_profile_file: MagicMock,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test a reauthentication flow with invalid info."""
    mock_process_profile_file.return_value[MOCK_AES_DEVICE_ID]["info"].pop("key")

    mock_config = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG_DATA,
        unique_id=MOCK_AES_DEVICE_ID,
    )
    mock_config.add_to_hass(hass)

    result = await mock_config.start_reauth_flow(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_FILE: UPLOADED_FILE,
        },
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "invalid_profile_file"
    mock_setup_entry.assert_not_awaited()
