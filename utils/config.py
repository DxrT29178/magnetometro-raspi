from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

# --- Direcciones/Registros LSM9DS1 (mag) ---
MAG_ADDRESS: int = 0x1C
CTRL_REG1_M: int = 0x20
CTRL_REG2_M: int = 0x21
CTRL_REG3_M: int = 0x22
CTRL_REG4_M: int = 0x23
CTRL_REG5_M: int = 0x24
STATUS_REG_M: int = 0x27
OFFSET_X_L_M: int = 0x05
OFFSET_X_H_M: int = 0x06
OFFSET_Y_L_M: int = 0x07
OFFSET_Y_H_M: int = 0x08
OFFSET_Z_L_M: int = 0x09
OFFSET_Z_H_M: int = 0x0A
OUT_X_L_M: int = 0x28
OUT_X_H_M: int = 0x29
OUT_Y_L_M: int = 0x2A
OUT_Y_H_M: int = 0x2B
OUT_Z_L_M: int = 0x2C
OUT_Z_H_M: int = 0x2D

# --- Parámetros generales ---
SCALE_FACTOR_UT_PER_LSB: float = 0.014  # ±4 gauss
SAMPLE_RATE_HZ: int = 10
OUTPUT_DIR: Path = Path("data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # crea carpeta de salida

@dataclass(frozen=True)
class Paths:
    output: Path = OUTPUT_DIR
    config: Path = Path(__file__).parent / "config.py"