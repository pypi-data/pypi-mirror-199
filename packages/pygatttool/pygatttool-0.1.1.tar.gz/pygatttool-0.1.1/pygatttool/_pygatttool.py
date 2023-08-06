import pexpect


class PyGatttool:
    def __init__(self, address: str, verbose: bool = False, timeout_seconds=10):
        self._addr = address
        self._verbose = verbose
        self._timeout_seconds = 10

        self._child = None

    def _send(self, s: str):
        if self._verbose:
            print(f'sending "{s}"')

        self._child.sendline(s)

    def _expect(self, s: str):
        if self._verbose:
            print(f'expecting "{s}"')

        self._child.expect(s, timeout=self._timeout_seconds)

    def _expect_newline(self):
        if self._verbose:
            print(f'expecting new line')

        self._child.expect('\r\n', timeout=self._timeout_seconds)

    def _wait_for_newline(self):
        self._expect_newline()
        data = self._child.before

        if self._verbose:
            print(f'data: "{data}"')

        return data

    def connect(self) -> bool:
        if self._verbose:
            print(f"connecting to address: {self._addr}")

        self._child = pexpect.spawn("gatttool -I", encoding='utf-8')

        self._send(f"connect {self._addr}")
        self._expect("Connection successful")

        if self._verbose:
            print('connected')

        return True

    def char_write_req(self, value: int, handle: int) -> bool:
        line = f"char-write-req {hex(handle)} {value:04x}"
        expected = "Characteristic value was written successfully"
        self._send(line)
        self._expect(expected)
        return True

    def mtu(self, size: int) -> bool:
        line = f'mtu {size}'
        expected = f"MTU was exchanged successfully: {size}"
        self._send(line)
        self._expect(expected)

    def char_read_hnd(self, handle: int, timeout_seconds: int = 10):
        self._send(f"char-read-hnd {hex(handle)}")
        self._expect("Characteristic value/descriptor: ")
        return self._wait_for_newline()

    def char_write_cmd(self, handle: int, command: bytearray, timeout_seconds: int = 10):
        line = f'char-write-cmd {hex(handle)} {command.hex()}'
        expected = f'Indication   handle = 0x{handle:04x} value: '
        self._send(line)
        self._expect(expected)

        return self._wait_for_newline()

    def wait_for_notification(self, handle: int, timeout_seconds: int = 10):
        expected = f'Notification handle = 0x{handle:04x} value: '
        self._expect(expected)

        return self._wait_for_newline()
