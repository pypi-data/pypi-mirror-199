#!/usr/bin/env python3
#
# Filename: suta_ble_consts.py
#
# Author: Simon Redman <simon@ergotech.com>
# File Created: 03.03.2023
# Description: Constants required for BLE communication with the SUTA beds
#

from enum import IntEnum, Enum
import platform

# Normally, one would identify a BLE devuce by its UUID
# As far as I can tell (I know nothing about BLE),
# the bed does not advertise a UUID.
# Use the name instead.
BED_LOCAL_NAME = "QRRM104150"

class BedServices(Enum):
    CONTROL = '0000fee9-0000-1000-8000-00805f9b34fb' # Control the bed
    ACK_CMD = '0000ffe0-0000-1000-8000-00805f9b34fb' # I don't know what this is
    UPDATE = '00010203-0405-0607-0809-0a0b0c0d1912' # I can guess what this is, best not to mess with it

# Characteristics exposed by the bed
class BedCharacteristic(Enum):
    CONTROL_COMMAND = 'd44bc439-abfd-45a2-b575-925416129600' # Send commands here - Write
    CONTROL_READ = 'd44bc439-abfd-45a2-b575-925416129601' # Read the current state here. Read/Notify
    ACK_CMD_ACK = '0000ffe1-0000-1000-8000-00805f9b34fb' # "ACK OutPut" - Read/Notify
    ACK_CMD_CMD = '0000ffe2-0000-1000-8000-00805f9b34fb' # "CMD Input" - Write
    UPDATE_OTA = '00010203-0405-0607-0809-0a0b0c0d2b12' # Brick your bed here - Write

class BedCommands(IntEnum):
    '''
    These were reverse engineered and documented in
    https://github.com/stevendodd/sleepmotion-ble/blob/main/pi-zero/sleepmotion-ble.py
    '''
    LIGHT = 0x6e01003cab
    ZERO_GRAVITY = 0x6e010045b4
    FLAT = 0x6e010031a0
    HEAD_UP = 0x6e01002493
    HEAD_DOWN = 0x6e01002594
    FEET_UP = 0x6e01002695
    FEET_DOWN = 0x6e01002796

IS_LINUX = platform.system() == "Linux"
