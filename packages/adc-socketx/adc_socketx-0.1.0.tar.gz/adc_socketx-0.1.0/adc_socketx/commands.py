import pathlib
import socket
import struct
import time

from adc_socketx import config

import numpy as np
import typer
from rich.progress import track
from soundfile import SoundFile


class SocketX:
    def __init__(
            self,
            host: str = config.SOCKET_HOST,
            port: str = config.SOCKET_PORT
    ) -> None:
        self._host = host
        self._port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)

    def connect(self) -> None:
        try:
            self.sock.connect((self._host, self._port))
        except socket.error as e:
            msg = (
                f'err: {e}. Check settings: '
                f'{config.SOCKET_HOST}:{config.SOCKET_PORT}'
            )
            typer.secho(msg, fg=typer.colors.BRIGHT_RED)
            raise typer.Exit(1)

    def disconnect(self) -> None:
        self.sock.close()

    def send(self, command: str) -> None:
        """Accept `command` in HEX."""
        try:
            self.sock.send(bytes.fromhex(command))
        except socket.error:
            print('Send error. Command: %s' % command)

    def receive(self, response_length: int) -> bytes:
        try:
            data = self.sock.recv(response_length)
            return data
        except socket.error:
            print('Receive error...')


sock = SocketX()


def adc_get_info() -> tuple:
    """Get info from ADC."""
    sock.send(config.COMMAND_GET_INFO['h_text'])
    data = sock.receive(config.COMMAND_GET_INFO['response_len'])
    unpacked_data = struct.unpack(
        config.COMMAND_GET_INFO['struct_unpack_str'], data
    )
    return unpacked_data


def adc_get_mode():
    """Get mode from ADC."""
    sock.send(config.COMMAND_GET_MODE['h_text'])
    data = sock.receive(config.COMMAND_GET_MODE['response_len'])
    print(data)


def adc_set_mode(num_of_channels: bool, ch1: bool, ch2: bool) -> bool:
    """Set mode to ADC.

    Args:
        num_of_channels (bool):  True = 2, False = 1
        ch1 (bool): True = IEPE, False = AC
        ch2 (bool): True = IEPE, False = AC

    Returns:
        `True` if the mode is set

    """
    com_str = bytearray(bytes.fromhex(config.COMMAND_SET_MODE['h_text']))

    if ch1 and ch2:
        com_str.extend(b'\x0F')
    elif ch1:
        com_str.extend(b'\x03')
    elif ch2:
        com_str.extend(b'\x0C')
    else:
        com_str.extend(b'\x00')

    com_str.extend(b'\x03') if num_of_channels else com_str.extend(b'\x01')
    com_str.extend(b'\x00\x80')  # master ADC

    sock.send(com_str.hex())
    data = sock.receive(config.COMMAND_SET_MODE['response_len'])
    if data != config.COMMAND_SET_MODE['response_ok']:
        return False
    return True


def adc_off() -> bool:
    """Stop sending the ADC data.

    Returns:
        `True` if sending stopped
    """
    data = b''
    while data != config.COMMAND_ADC_OFF['response_ok']:
        sock.send(config.COMMAND_ADC_OFF['h_text'])
        data = sock.receive(8008)
    return True


def record_to_wav(num_of_frames: int, num_of_channels: int) -> bool:
    """Record the ADC data."""
    adc_off()
    data_frame = bytearray()
    sock.send(config.COMMAND_ADC_ON['h_text'])

    p = pathlib.Path(config.FILE_PATH)
    p.mkdir(parents=True, exist_ok=True)
    file_name = time.strftime(config.FIlE_FORMAT)
    path_filename = p / file_name

    with SoundFile(
        path_filename, 'w', 96000, num_of_channels, subtype='PCM_24'
    ) as sf:
        for frame in track(
            range(1, num_of_frames + 1), description='Recording...'
        ):
            while len(data_frame) != 8008:
                data_frame.extend(sock.receive(8008))

            unpacked_head = struct.unpack('<6c 2b 2I', data_frame[:16])

            if unpacked_head[-1] != frame:
                adc_off()
                path_filename.unlink()
                raise ValueError('Data frame is lost')

            data = data_frame[16:]

            if len(data) % 3 != 0:
                adc_off()
                raise ValueError('Size of data must be a multiple of 3 bytes')

            temp = bytearray()

            for _ in range(0, len(data), 3):
                # Add 1 byte (\x00) to each chain
                temp.append(0)
                temp.extend(data[_:_ + 3])

            sig = np.frombuffer(temp, dtype='i4').reshape(-1, num_of_channels)
            sf.write(sig)
            data_frame.clear()
        adc_off()

    if unpacked_head[-1] == num_of_frames:
        print(f'File is written to: {path_filename}')
        return True

    return False


def adc_reboot() -> bool:
    """Reboot ADC."""
    sock.send(config.COMMAND_REBOOT['h_text'])
    data = sock.receive(config.COMMAND_REBOOT['response_len'])
    if data != config.COMMAND_REBOOT['response_ok']:
        return False
    return True


def adc_get_lan() -> tuple:
    """Get lan settings from ADC.

    Returns: LAN settings
        Example:
        (5000, 192, 168, 0, 50, 255, 255, 255, 0, 192, 168, 0, 1, b'MAC')

    """
    sock.send(config.COMMAND_GET_LAN['h_text'])
    data = sock.receive(config.COMMAND_GET_LAN['response_len'])
    unpacked_data = struct.unpack(
        config.COMMAND_GET_LAN['struct_pack_str'], data
    )
    return unpacked_data


def adc_set_lan(settings: bytes) -> bool:
    """Set lan settings to ADC."""
    sock.send(config.COMMAND_SET_LAN['h_text'] + settings.hex())
    lan_data = sock.receive(config.COMMAND_SET_LAN['response_len'])
    if lan_data != config.COMMAND_SET_LAN['response_ok']:
        return False
    return True
