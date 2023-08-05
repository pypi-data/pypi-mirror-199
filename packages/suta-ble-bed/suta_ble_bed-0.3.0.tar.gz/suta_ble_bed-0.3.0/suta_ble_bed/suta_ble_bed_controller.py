#!/usr/bin/env python3
#
# Filename: suta_ble_bed_controller.py
#
# Author: Simon Redman <simon@ergotech.com>
# File Created: 03.22.2023
# Description: Object which handles discovery and connection to SUTA-compatible devices
#

import asyncio
from bleak import BleakScanner
from contextlib import AbstractAsyncContextManager

from types import TracebackType

from .suta_ble_bed import BleSutaBed
from .suta_ble_scanner import SutaBleScanner
from .suta_ble_consts import BED_LOCAL_NAME

class SutaBleBedController(AbstractAsyncContextManager):

    def __init__(self, adapter: str = None) -> None:
        """
        Constructor

        @param adapter: The Bluetooth adapter to use, like "hci0"
        """
        super().__init__()

        self._bed_scanner = SutaBleScanner()
        self._bleak_scanner = BleakScanner(
            detection_callback=self._bed_scanner._scanner_discovery_callback,
            adapter=adapter)

    async def __aenter__(self):
        await self._bleak_scanner.start()
        return self
    
    async def __aexit__(self, __exc_type: type[BaseException] | None, __exc_value: BaseException | None, __traceback: TracebackType | None) -> bool | None:
        await self._bleak_scanner.stop()
        return await super().__aexit__(__exc_type, __exc_value, __traceback)
    
    def devices(self):
        return self._bed_scanner