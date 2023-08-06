# PyGatttool

A wrapper around `gatttool` and `pexpect`, intended to be used as a simple BLE development tool for interacting with peripheral devices.

## Requirements

A working `gatttool` install. 

If installing from the repo you need `pexpect` (`pip install pexpect`).

## Installation

```
pip install pygatttool
```

## Usage

The following code (from [polarpy](https://github.com/wideopensource/polarpy)) starts the raw PPG stream on a Polar OH1. The address and attribute handles for your particular device can be found using `gatttool` or another BLE tool such as nRF Connect.

```
from pygatttool import PyGatttool

OH1_ADDR = "XX:XX:XX:XX:XX:XX"
OH1_CONTROL_ATTRIBUTE_HANDLE = 0xXX
OH1_DATA_ATTRIBUTE_HANDLE = 0xXX

if '__main__' == __name__:
    ble = PyGatttool(address=OH1_ADDR)

    ble.connect()
    ble.mtu(232)
    ble.char_write_req(handle=OH1_CONTROL_ATTRIBUTE_HANDLE + 1, value=0x200)
    ble.char_write_req(handle=OH1_DATA_ATTRIBUTE_HANDLE + 1, value=0x100)
    ble.char_write_cmd(handle=OH1_CONTROL_ATTRIBUTE_HANDLE, b'\x02\x01\x00\x01\x82\x00\x01\x01\x16\x00')

    while True:
        print(ble.wait_for_notification(handle=OH1_DATA_ATTRIBUTE_HANDLE))
```

the output will look something like this:

```
01 00 b2 92 28 f4 52 82 07 00 ce ff 03 71 54 05 f3 60 05 a8 f2 ff 30 00 04 c6 54 05 07 60 05 8a f2 ff 3a ff 03 8c 54 05 88 5f 05 65 f2 ff 97 ff 03 e4 54 05 04 5f 05 41 f2 ff 17 ff 03 d6 54 05 70 5e 05 18 f2 ff a7 ff 03 6d 54 05 4f 5e 05 4b f2 ff 78 ff 03 8b 54 05 5b 5e 05 0b f2 ff 3f 00 04 48 54 05 a0 5e 05 08 f2 ff 18 00 04 f3 54 05 ca 5e 05 13 f2 ff 93 ff 03 84 54 05 67 5f 05 08 f2 ff 26 00 04 66 55 05 f1 5e 05 34 f2 ff e0 ff 03 be 55 05 81 5f 05 0b f2 ff dc ff 03 b2 55 05 c1 5f 05 0b f2 ff 75 00 04 b5 56 05 2b 60 05 2c f2 ff a8 ff 03 a5 56 05 6b 60 05 d6 f1 ff 89 00 04 57 57 05 88 60 05 3a f2 ff d9 00 04 55 57 05 33 61 05 3b f2 ff 45 01 04 7f 57 05 a0 61 05 38 f2 ff 
01 00 b2 72 30 f4 52 82 07 00 4e 01 04 a0 58 05 f2 60 05 49 f1 ff a2 01 04 a6 58 05 28 62 05 3e f2 ff 5f 02 04 41 59 05 9a 62 05 37 f2 ff 16 02 04 1a 5a 05 34 63 05 4e f2 ff 43 02 04 1d 5a 05 1e 63 05 47 f2 ff 05 03 04 ea 5a 05 ba 63 05 3f f2 ff 18 03 04 aa 5a 05 93 64 05 4a f2 ff a7 03 04 b1 5b 05 82 64 05 e6 f1 ff 6f 03 04 ff 5b 05 47 65 05 0d f2 ff e3 03 04 3c 5c 05 47 65 05 51 f2 ff 7b 04 04 db 5c 05 d7 65 05 8d f2 ff 98 04 04 d6 5c 05 3a 66 05 45 f2 ff 38 05 04 d3 5d 05 b3 66 05 5b f2 ff 72 05 04 7d 5d 05 ea 66 05 9d f2 ff b4 05 04 b2 5e 05 3d 67 05 4c f2 ff 8f 05 04 4b 5e 05 57 67 05 61 f2 ff 3c 06 04 ca 5e 05 66 67 05 2d f2 ff fe 05 04 2e 5f 05 93 67 05 16 f2 ff 

...
```

## Issues

- While readily available, `gatttool` is long deprecated.

- It is somewhat unfortunate that `gatttool` does not appear report a version number. The `pexpect` code is looking for specific response strings, so if those strings change even slightly between versions it will break PyGatttool. That being said, it has been tested on several versions of Ubuntu 20+ without any issues, and given the deprecation it is probably unlikely that it will change. 




