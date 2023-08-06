from dataclasses import dataclass


@dataclass
class InfoConfig:
    """Data class for store and update ADC configuration."""
    serial_number: int
    channels_qty: int
    frequency: int
    calibration_dc_ac_ch1: float
    calibration_icp_ch1: float
    calibration_dc_ac_ch2: float
    calibration_icp_ch2: float
    calibration_dc_ac_ch3: float
    calibration_icp_ch3: float
    calibration_dc_ac_ch4: float
    calibration_icp_ch4: float


@dataclass
class LanConfig:
    """Data class for store and update ADC lan configuration."""
    port: int
    ip_1: int
    ip_2: int
    ip_3: int
    ip_4: int
    mask_1: int
    mask_2: int
    mask_3: int
    mask_4: int
    gateway_1: int
    gateway_2: int
    gateway_3: int
    gateway_4: int
    mac: bytes
