import time

DEVICE = "/dev/signal_driver"


# Seleccionar puerto a leer
def set_signal(idx):
    with open(DEVICE, "wb") as f:
        # Escritura en el CDD
        f.write(bytes(str(idx), "ascii"))


# Leer puerto seleccionado
def read_sample():
    with open(DEVICE, "rb") as f:
        # Lectura y decodificacion en el CDD
        val = f.read(32).decode()
    return int(val)


# Plot
def plot_loop():
    # El usuario decide aquí cuál señal leer (0 o 1):
    sel = int(input("¿Leer señal 0 o 1? Presione Ctrl+C para salir.\n"))
    set_signal(sel)
    ts = 0
    print(f"Señal a leer: {sel}. Presione Ctrl+C para leer otra señal.")

    while True:
        try:
            val = read_sample()
            print(f"Tiempo: {ts}, Valor: {val}")
            ts += 1
            time.sleep(1)
        except KeyboardInterrupt:
            sel = int(input("¿Leer señal 0 o 1? Presione Ctrl+C para salir.\n"))
            set_signal(sel)
            ts = 0


def main():
    plot_loop()


if __name__ == "__main__":
    main()

