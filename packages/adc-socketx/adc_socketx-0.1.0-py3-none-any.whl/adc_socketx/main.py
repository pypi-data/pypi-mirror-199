import ipaddress
import struct
from dataclasses import astuple

from adc_socketx import commands, config, data_models

import typer
from rich.console import Console
from rich.table import Table


INFO = 'ADC socket data eXchange script. GTLAB Diagnostic LLC, 2023'

console = Console()

app = typer.Typer(
    add_completion=False,
    help=INFO,
)


@app.command()
def get_info():
    """
    Get the ADC information.
    (serial number, frequency, channels, calibration)
    """
    data = commands.adc_get_info()
    table = Table(show_header=False)

    for table_row in zip(config.COMMAND_GET_INFO['table_info_columns'], data):
        table.add_row(table_row[0], str(table_row[1]), style='green')

    console.print(table)


@app.command()
def get_lan():
    """Get lan configuration and exit."""
    data = commands.adc_get_lan()
    table = Table(show_header=False)
    col = config.COMMAND_GET_LAN['table_info_columns']
    table.add_row(col[0], str(data[0]))
    for index, value in enumerate(range(1, 13, 4)):
        table.add_row(
            col[index + 1],
            '.'.join(str(___) for ___ in data[value:value + 4]),
        )
    table.add_row(col[4], data[13].hex().upper())

    console.print(table)


@app.command()
def set_ip(ipv4: str):
    """Change the ipv4 address setting."""
    try:
        new_ip = ipaddress.IPv4Address(ipv4)
    except ValueError as e:
        msg = f'err: {e}. Please check.'
        typer.secho(msg, fg=typer.colors.BRIGHT_RED)
        raise typer.Exit()

    if not new_ip.is_private:
        typer.secho(
            'Only private IP addresses is supported',
            fg=typer.colors.BRIGHT_RED
        )
        raise typer.Exit()

    typer.confirm(
        f'Are you sure you want to change the ip-address to: {new_ip} ',
        abort=True
    )

    data = commands.adc_get_lan()
    lan_config = data_models.LanConfig(*data)

    l_new_ip = str(new_ip).split('.')

    [setattr(
        lan_config,
        f'ip_{i + 1}',
        int(l_new_ip[i])
    ) for i in range(4)]

    lan_command = struct.pack(
        config.COMMAND_SET_LAN['struct_pack_str'], *astuple(lan_config)
    )

    if commands.adc_set_lan(lan_command):
        console.print(
            f'The new ip address is set to {new_ip}. '
            f'Don\'t forget to update your settings',
            style='green'
        )
    else:
        console.print('err: Failed to update ip settings!', style='red')


@app.command()
def get_wav(
    seconds: int = typer.Argument(..., min=1, max=600),
    ch: int = typer.Option(
        config.NUM_OF_CHANNELS_DEFAULT,
        min=1, max=2,
        help='Set the number of channels to record'
    ),
    iepe: bool = True,
):
    """Record a signal from the ADC to a .wav file."""
    if ch == 2:  # default
        num_of_frames = round(config.FRAMES_2CH_PER_SECOND * seconds)
        commands.adc_set_mode(1, iepe, iepe)
    else:
        num_of_frames = round(config.FRAMES_1CH_PER_SECOND * seconds)
        commands.adc_set_mode(0, iepe, iepe)

    if not commands.record_to_wav(num_of_frames, ch):
        console.print('Something went wrong, check the settings', style='red')


@app.command()
def reboot():
    """Reboot the ADC."""
    if commands.adc_reboot():
        console.print('ADC rebooted!', style='green')


@app.callback()
def sock_connect():
    """Connect to socket when the command is called."""
    commands.sock.connect()


if __name__ == '__main__':
    app()
