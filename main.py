from __future__ import annotations
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils.config import Paths, SAMPLE_RATE_HZ, SCALE_FACTOR_UT_PER_LSB
from utils.file_io import save_csv  # Importa la función save_csv para guardar datos            
from core.magnetometer import Magnetometer
from analysis.visualization import plot_3d
from interface.main_gui import run_gui
from utils.file_io import save_csv



from __future__ import annotations
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils.config import Paths, SAMPLE_RATE_HZ, SCALE_FACTOR_UT_PER_LSB
from utils.file_io import save_csv  # Importa la función save_csv para guardar datos            
from core.magnetometer import Magnetometer
from analysis.visualization import plot_3d
from interface.main_gui import run_gui

if __name__ == "__main__":
    run_gui()