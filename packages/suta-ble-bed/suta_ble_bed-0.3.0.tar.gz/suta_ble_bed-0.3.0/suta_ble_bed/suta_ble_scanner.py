#!/usr/bin/env python3
#
# Filename: scanner.py
#
# Author: Simon Redman <simon@ergotech.com>
# File Created: 03.03.2023
# Description: Functionality to scan for BLE devices which should be compatible with the rest of this module

import asyncio

from bleak import AdvertisementData
from bleak.backends.device import BLEDevice

from typing import Any

from .suta_ble_bed import BleSutaBed
from .suta_ble_consts import BedCharacteristic, IS_LINUX, BED_LOCAL_NAME

class SutaBleScanner():

    def __init__(self) -> None:
        self.scanner_running_lock = asyncio.Lock()

        self._new_devices = asyncio.Queue()

        self._tasks = set()

    def __aiter__(self):
        return self

    async def __anext__(self) -> BleSutaBed:
        return await self._new_devices.get()

    def _scanner_discovery_callback(self, device: BLEDevice, advertising_data: AdvertisementData) -> None:
        task = asyncio.create_task(self._scanner_discovery_callback_int(device, advertising_data))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def _scanner_discovery_callback_int(self, device: BLEDevice, advertising_data: AdvertisementData) -> None:
        if advertising_data.local_name == BED_LOCAL_NAME:
            await self._new_devices.put(BleSutaBed(device, self))
