# PyGatttool

A wrapper around gatttool and pexpect, intended to be used as a simple and reliable BLE development tool.

## Requirements

A working `gatttool` install. 

If installing from the repo you need `pexpect` (`pip install pexpect`).

## Installation

```
pip install pygatttool
```

## Usage

The following code (from [PyPolar](https://github.com/wideopensource/pypolar)) starts the raw PPG stream on a Polar OH1. The address and attribute handles for your particular device can be found using `gatttool` or another BLE tool such as nRF Connect.

```
from pygatttool import PyGatttool

OH1_ADDR = "A0:9E:1A:7D:3C:5D"
OH1_CONTROL_ATTRIBUTE_HANDLE = 0x003f
OH1_DATA_ATTRIBUTE_HANDLE = 0x0042
OH1_START_PPG_COMMAND = b'\x02\x01\x00\x01\x82\x00\x01\x01\x16\x00'

if '__main__' == __name__:
    ble = PyGatttool(address=OH1_ADDR, verbose=True)

    ble.connect()
    ble.mtu(232)
    ble.char_write_req(handle=OH1_CONTROL_ATTRIBUTE_HANDLE + 1, value=0x200)
    ble.char_write_req(handle=OH1_DATA_ATTRIBUTE_HANDLE + 1, value=0x100)
    ble.char_write_cmd(handle=OH1_CONTROL_ATTRIBUTE_HANDLE, command=OH1_START_PPG_COMMAND)

    while True:
        ble.wait_for_notification(handle=OH1_DATA_ATTRIBUTE_HANDLE)
```

## Issues

- While still readily available, `gatttool` is long deprecated.

- It is somewhat unhelpful that `gatttool` does not appear report a version number. The `pexpect` code is looking for specific response strings, so if those strings change even slightly between versions it will break PyGatttool. That being said, it has been tested on several versions of Ubuntu 20+ without any issues, and given the deprecation it is probably unlikely that it will change. 




