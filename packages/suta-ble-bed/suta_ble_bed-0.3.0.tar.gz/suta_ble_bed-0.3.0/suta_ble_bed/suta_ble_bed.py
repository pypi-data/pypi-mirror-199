#!/usr/bin/env python3
#
# Filename: suta_ble_bed.py
#
# Author: Simon Redman <simon@ergotech.com>
# File Created: 03.03.2023
# Description: Handle BLE communications for a SUTA bed frame such as the i500 or i800.
#   Which also appears to be identical to the Sleep Motion beds.
#   BLE communication based on:
#   https://github.com/stevendodd/sleepmotion-ble/blob/main/pi-zero/sleepmotion-ble.py
#   Code structure inspired by:
#   https://github.com/sopelj/python-ember-mug/blob/main/ember_mug/mug.py
#
#   Trying to decide if your bed is compatible?
#   Connect to it with a generic BLE GATT handler, such as BLE Scanner on Android
#   If one of the services GUIDs starts with "FEE9", it likely is. Try it out!
#   It is unlikely anything harmful will happen, but I take no responsibility if
#   your bed catches on fire.
#

from __future__ import annotations

import asyncio
import contextlib

from bleak import BleakClient, BleakError, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak_retry_connector import establish_connection

from collections.abc import AsyncIterator
from typing import Any, Callable, Literal
import logging

from .suta_ble_consts import BedServices, BedCommands, BedCharacteristic

logger = logging.getLogger(__name__)

class BleSutaBed:

    def __init__(
        self,
        ble_device: BLEDevice,
        controller,
        **kwargs: Any,
    ) -> None:
        """
        Constructor

        @param ble_device: The bleak.BLEDevice which represents the connection to the bed
        @param controller: The SutaBleBedController which controls this connection
        """
        self.device = ble_device
        self.controller = controller

        self._client: BleakClient = None  # type: ignore[assignment]
        self._connect_lock = asyncio.Lock()
        self._operation_lock = asyncio.Lock()
        self._expected_disconnect = False

    def is_connected(self) -> bool:
        return self._client is not None and self._client.is_connected

    async def raise_feet(self) -> None:
        '''
        Raise the feet of the bed a notch.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.FEET_UP.to_bytes(5, 'big'))

    async def lower_feet(self) -> None:
        '''
        Lower the feet of the bed a notch.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.FEET_DOWN.to_bytes(5, 'big'))

    async def raise_head(self) -> None:
        '''
        Raise the head of the bed a notch.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.HEAD_UP.to_bytes(5, 'big'))

    async def lower_head(self) -> None:
        '''
        Lower the head of the bed a notch.
        '''
        await self._write(BedServices.CONTROL, BedCharacteristic.CONTROL_COMMAND, data=BedCommands.HEAD_DOWN.to_bytes(5, 'big'))

    async def _write(self, service: BedServices, characteristic: BedCharacteristic, data: bytearray) -> None:
        """Helper to write characteristic."""
        if self._operation_lock.locked():
            logger.debug("Operation already in progress. Waiting for it to complete")
        async with self._operation_lock:
            await self._ensure_connection()
            try:
                await self._client.write_gatt_char(characteristic.value, data)
                logger.debug("Wrote '%s' to attribute '%s'", data, characteristic)
            except BleakError as e:
                logger.error("Failed to write '%s' to attribute '%s': %s", data, characteristic, e)
                raise

    async def _ensure_connection(self) -> None:
        """Connect to bed."""
        if self._connect_lock.locked():
            logger.debug("Connection to %s already in progress. Waiting first.", self.device.name)

        if self.is_connected():
            return

        async with self._connect_lock:
            # Also check after lock is acquired
            if self.is_connected:
                return
            try:
                logger.debug(f"Connecting to {self.device}")
                async with BleakScanner():
                    # Need to have the scanner running in order for Bluez to populate the device
                    client = await establish_connection(
                        client_class=BleakClient,
                        device=self.device,
                        name=f'{self.device.name} ({self.device.address})',
                        use_services_cache=True,
                        disconnected_callback=self._disconnect_callback,  # type: ignore
                        ble_device_callback=lambda: self.device,
                    )
                    self._expected_disconnect = False
                    self._client = client
            except (asyncio.TimeoutError, BleakError) as error:
                logger.error("%s: Failed to connect to the bed: %s", self.device, error)
                raise
        return

    def _disconnect_callback(self, client: BleakClient) -> None:
        """Disconnect from device."""
        if self._expected_disconnect:
            logger.debug("Disconnect callback called")
        else:
            logger.warning("Unexpectedly disconnected")

    def set_client_options(self, **kwargs: str) -> None:
        """Update options in case they need to overriden in some cases."""
        if kwargs.get('adapter') and IS_LINUX is False:
            raise ValueError('The adapter option is only valid for the Linux BlueZ Backend.')
        self._client_kwargs = {**kwargs}

    @contextlib.asynccontextmanager
    async def connection(self, **kwargs: str) -> AsyncIterator[BleSutaBed]:
        """Helper for establishing a connection and automatically closing it."""
        self.set_client_options(**kwargs)
        # This will happen automatically, but calling it now will give us immediate feedback
        await self._ensure_connection()
        yield self
        await self.disconnect()
