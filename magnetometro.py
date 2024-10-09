import RTIMU
import os
import time
import numpy as np
import matplotlib.pyplot as plt

# Cargar la configuración de la IMU (incluyendo la calibración)
SETTINGS_FILE = "RTIMULib"
s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

# Verificar que la IMU se haya inicializado correctamente
if not imu.IMUInit():
    print("IMU Init Failed")
    exit(1)
else:
    print("IMU Init Succeeded")

# Configuración de tasas de actualización
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

# Tasa de actualización (en milisegundos)
poll_interval = imu.IMUGetPollInterval()

# Inicializar la gráfica
plt.ion()  # Modo interactivo para gráficos en tiempo real
fig, ax = plt.subplots()

# Variables para almacenar los datos del magnetómetro
x_data, y_data, z_data = [], [], []
t_data = []

# Tiempo inicial
start_time = time.time()

print("Comenzando a medir el magnetismo en tiempo real...")

# Bucle para capturar y graficar los datos en tiempo real
try:
    while True:
        if imu.IMURead():
            data = imu.getIMUData()
            compass = data["compass"]  # Lectura del magnetómetro (X, Y, Z)

            # Obtener los datos del tiempo
            current_time = time.time() - start_time

            # Guardar los datos de X, Y, Z
            t_data.append(current_time)
            x_data.append(compass[0])
            y_data.append(compass[1])
            z_data.append(compass[2])

            # Limitar la cantidad de datos mostrados en el gráfico
            if len(t_data) > 100:
                t_data.pop(0)
                x_data.pop(0)
                y_data.pop(0)
                z_data.pop(0)

            # Limpiar la gráfica anterior y dibujar los nuevos datos
            ax.clear()
            ax.plot(t_data, x_data, label='X')
            ax.plot(t_data, y_data, label='Y')
            ax.plot(t_data, z_data, label='Z')
            ax.set_xlabel('Tiempo (s)')
            ax.set_ylabel('Campo Magnético')
            ax.set_title('Lectura del Magnetómetro en Tiempo Real')
            ax.legend()
            plt.pause(0.001)

        time.sleep(poll_interval * 1.0 / 1000.0)  # Esperar el intervalo de sondeo

except KeyboardInterrupt:
    print("Medición interrumpida")
    plt.ioff()
    plt.show()
