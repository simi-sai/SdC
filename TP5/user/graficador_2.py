import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

DRIVER_PATH = "/dev/driver_signal"  # Ruta al dispositivo del driver

class SignalPlotter:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualizador de Señales")

        self.is_running = True
        self.data_y = []
        self.data_x = []
        self.t0 = time.time()
        self.selected_signal = 0
        self.refresh_rate = 0.02

        self._setup_ui()

        self.worker = threading.Thread(target=self._refresh_data, daemon=True)
        self.worker.start()

    def _setup_ui(self):
        controls = ttk.Frame(self.master)
        controls.pack(padx=10, pady=10)

        self.btn_square = ttk.Button(
            controls, text="Señal 0 (cuadrada)", command=lambda: self._switch_signal(1)
        )
        self.btn_square.grid(row=0, column=0, padx=5)

        self.btn_triangle = ttk.Button(
            controls, text="Señal 1 (triangular)", command=lambda: self._switch_signal(2)
        )
        self.btn_triangle.grid(row=0, column=1, padx=5)

        self.figure, self.axis = plt.subplots(figsize=(7, 4))
        self.axis.set_title("Señal Sensada")
        self.axis.set_xlabel("Tiempo (s)")
        self.axis.set_ylabel("Valor")
        (self.plot_line,) = self.axis.plot([], [], "b-")

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack()

    def _switch_signal(self, signal_id):
        try:
            with open(DRIVER_PATH, "w") as dev:
                dev.write(str(signal_id))
            self.selected_signal = signal_id
            self.data_x.clear()
            self.data_y.clear()
            self.t0 = time.time()
            print(f"Señal seleccionada: {signal_id}")
        except Exception as err:
            print(f"Error cambiando señal: {err}")

    def _read_driver(self):
        try:
            with open(DRIVER_PATH, "r") as dev:
                return int(dev.read().strip())
        except Exception as err:
            print(f"Error leyendo driver: {err}")
            return None

    def _refresh_data(self):
        next_update = time.time()
        interval = self.refresh_rate
        while self.is_running:
            now = time.time()
            if now >= next_update:
                val = self._read_driver()
                if val is not None:
                    t = now - self.t0
                    self.data_x.append(t)
                    self.data_y.append(val)
                    max_samples = int(20 / interval)
                    if len(self.data_x) > max_samples:
                        self.data_x = self.data_x[-max_samples:]
                        self.data_y = self.data_y[-max_samples:]
                    self.plot_line.set_data(self.data_x, self.data_y)
                    self.axis.relim()
                    self.axis.autoscale_view()
                    self.canvas.draw()
                next_update += interval
            time.sleep(0.005)

    def close(self):
        self.is_running = False
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalPlotter(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
