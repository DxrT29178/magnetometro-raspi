import numpy as np
import time

class Magnetometer:
    def __init__(self, noise=2.0, amplitude=40.0):
        self.noise = noise
        self.amplitude = amplitude
        self.start_time = time.time()

    def configure(self):
        print("Simulador: magnetómetro configurado")

    def read_data(self):
        elapsed = time.time() - self.start_time
        x = self.amplitude * np.sin(elapsed) + np.random.normal(0, self.noise)
        y = self.amplitude * np.cos(elapsed) + np.random.normal(0, self.noise)
        z = np.random.normal(0, self.noise)
        return {"x": x, "y": y, "z": z, "ms": int(elapsed * 1000)}
