# Socket connection
SOCKET_HOST = '192.168.0.50'
SOCKET_PORT = 5000

# Default number of channels in (1, 2) __(used for recording)__
NUM_OF_CHANNELS_DEFAULT = 1

# Record's filename format
FIlE_FORMAT = '__%Y-%m-%d__%H-%M-%S.wav'
FILE_PATH = 'waves/'  # creates a file in the same place if empty

# Byte frames (7992) settings
FRAMES_1CH_PER_SECOND = 30.036
FRAMES_2CH_PER_SECOND = 72.072

# Commands
COMMAND_GET_INFO = {
    'h_text': '47 45 54 5F 49 4E 46 4F 00',
    'response_len': 45,
    'struct_unpack_str': '<3i 8f x',
    'table_info_columns': (
        'Serial number:',
        'Number of channels:',
        'Sampling frequency:',
        'Ch. 1 DC/AC calibration:',
        'Ch. 1 IEPE (ICP) calibration:',
        'Ch. 2 DC/AC calibration:',
        'Ch. 2 IEPE (ICP) calibration:',
        'Ch. 3 DC/AC calibration:',
        'Ch. 3 IEPE (ICP) calibration:',
        'Ch. 4 DC/AC calibration:',
        'Ch. 4 IEPE (ICP) calibration:',
    ),
}

COMMAND_SET_INFO = {
    'h_text': '53 45 54 5F 49 4E 46 4F 00',
    'response_len': 3,
    'response_ok': b'OK\x00',
    'struct_pack_str': '<3i 8f',
}

COMMAND_GET_LAN = {
    'h_text': '47 45 54 5F 4C 41 4E 00',
    'response_len': 23,
    'struct_pack_str': '<i 4B 4B 4B 6s x',
    'table_info_columns': (
        'IPv4Port',
        'IPv4Address',
        'IPv4Netmask',
        'IPv4GetawayAddress',
        'MACAddress',
    ),
}

COMMAND_SET_LAN = {
    'h_text': '53 45 54 5F 4C 41 4E 00',
    'response_len': 3,
    'response_ok': b'OK\x00',
    'struct_pack_str': '<i 4B 4B 4B 6s x',
}

COMMAND_GET_MODE = {
    'h_text': '47 45 54 5F 4D 4F 44 45 00',
    'response_len': 5,
}

COMMAND_SET_MODE = {
    'h_text': '53 45 54 5F 4D 4F 44 45 00',
    'response_len': 3,
    'response_ok': b'OK\x00',
}

COMMAND_ADC_ON = {
    'h_text': '41 44 43 5F 4F 4E 00',
    'response_len': 3,
    'struct_pack_str': '<6c 2b 2I',
}

COMMAND_ADC_OFF = {
    'h_text': '41 44 43 5F 4F 46 46 00',
    'response_len': 3,
    'response_ok': b'OK\x00',
}

COMMAND_REBOOT = {
    'h_text': '52 45 42 4F 4F 54 00',
    'response_len': 3,
    'response_ok': b'OK\x00',
}
