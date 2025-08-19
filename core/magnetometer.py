from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Tuple

try:
    import smbus2 as smbus  # disponible en Raspi
except Exception:  # pragma: no cover
    smbus = None  # evita import error en PC

from utils.config import (
    MAG_ADDRESS, CTRL_REG1_M, CTRL_REG2_M, CTRL_REG3_M, CTRL_REG4_M, CTRL_REG5_M,
    STATUS_REG_M, OFFSET_X_L_M, OFFSET_X_H_M, OFFSET_Y_L_M, OFFSET_Y_H_M, OFFSET_Z_L_M, OFFSET_Z_H_M,
    OUT_X_L_M, OUT_X_H_M, OUT_Y_L_M, OUT_Y_H_M, OUT_Z_L_M, OUT_Z_H_M,
    SCALE_FACTOR_UT_PER_LSB,
)


class Magnetometer(Protocol):
    """Contrato mínimo para backends del magnetómetro."""
    def configure(self) -> None: ...
    def data_ready(self) -> bool: ...
    def set_offsets(self, ox: int, oy: int, oz: int) -> None: ...
    def read_raw(self) -> Tuple[int, int, int]: ...  # LSB
    def read_ut(self) -> Tuple[float, float, float]: ...  # µT


@dataclass
class LSM9DS1Mag:
    bus_id: int = 1
    address: int = MAG_ADDRESS

    def __post_init__(self) -> None:
        if smbus is None:
            # Evita uso accidental sin HW
            raise RuntimeError("smbus2 no disponible: este backend requiere Raspberry/SMBus")
        self.bus = smbus.SMBus(self.bus_id)

    # --- I2C helpers ---
    def _write(self, reg: int, val: int) -> None:
        self.bus.write_byte_data(self.address, reg, val & 0xFF)

    def _read_u8(self, reg: int) -> int:
        return self.bus.read_byte_data(self.address, reg) & 0xFF

    def _read_i16(self, reg_l: int, reg_h: int) -> int:
        lo = self._read_u8(reg_l)
        hi = self._read_u8(reg_h)
        v = (hi << 8) | lo
        return v - 65536 if v >= 32768 else v

    # --- API ---
    def configure(self) -> None:
        # 20 Hz, UHP XY; FS=±4 gauss; modo continuo; UHP Z; BDU=1
        self._write(CTRL_REG1_M, 0x70)
        self._write(CTRL_REG2_M, 0x00)
        self._write(CTRL_REG3_M, 0x00)
        self._write(CTRL_REG4_M, 0x0C)
        self._write(CTRL_REG5_M, 0x40)

    def data_ready(self) -> bool:
        return (self._read_u8(STATUS_REG_M) & 0x08) != 0

    def set_offsets(self, ox: int, oy: int, oz: int) -> None:
        # se escriben bytes low/high
        self._write(OFFSET_X_L_M, ox & 0xFF)
        self._write(OFFSET_X_H_M, (ox >> 8) & 0xFF)
        self._write(OFFSET_Y_L_M, oy & 0xFF)
        self._write(OFFSET_Y_H_M, (oy >> 8) & 0xFF)
        self._write(OFFSET_Z_L_M, oz & 0xFF)
        self._write(OFFSET_Z_H_M, (oz >> 8) & 0xFF)

    def read_raw(self) -> Tuple[int, int, int]:
        x = self._read_i16(OUT_X_L_M, OUT_X_H_M)
        y = self._read_i16(OUT_Y_L_M, OUT_Y_H_M)
        z = self._read_i16(OUT_Z_L_M, OUT_Z_H_M)
        return x, y, z

    def read_ut(self) -> Tuple[float, float, float]:
        x, y, z = self.read_raw()
        s = SCALE_FACTOR_UT_PER_LSB
        return x * s, y * s, z * s
