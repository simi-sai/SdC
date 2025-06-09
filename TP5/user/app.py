import time
import matplotlib.pyplot as plt

DEVICE = "/dev/signal_driver"

def set_signal(idx):
    with open(DEVICE, "wb") as f:
        f.write(bytes(str(idx), "ascii"))

def read_sample():
    with open(DEVICE, "r") as f:
        val = f.readline().strip()
    return int(val)

def graficar_senial():
    while True:
        try:
            sel = int(
                input("¿Leer señal 1 (cuadrada) o 2 (triangular)? Presione Ctrl+C para salir.\n")
            )
            if sel not in (1, 2):
                print("Opción inválida. Elija 1 o 2.")
                continue
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break
        except Exception:
            print("Entrada inválida.")
            continue

        set_signal(sel)
        print(f"Señal a leer: {sel}. Presione Ctrl+C para detener y graficar.")

        tiempos = []
        valores = []
        ts = 0

        try:
            while True:
                val = read_sample()
                tiempos.append(ts)
                valores.append(val)
                print(f"Tiempo: {ts}, Valor: {val}")
                ts += 1
                time.sleep(1)  # Tiempo de actualizacion de 1 segundo
        except KeyboardInterrupt:
            print("Graficando señal...")

        plt.figure()
        plt.plot(tiempos, valores, marker='o')
        plt.title(f"Señal {sel} leída del driver")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Valor")
        plt.grid(True)
        plt.show()

def main():
    graficar_senial()

if __name__ == "__main__":
    main()