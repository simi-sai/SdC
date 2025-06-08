#!/bin/bash

# === Configuración ===
CDD_NAME="signal_driver"
CDD_DIR="CDD"
USER_APP="user/app.py"
MAJOR_FILE="/dev/$CDD_NAME"
MODULE_NAME="signal_driver.ko"

# === Paso 1: Compilar el módulo ===
echo "[+] Compilando el módulo..."
cd "$CDD_DIR" || {
  echo "[ERROR] No se pudo acceder al directorio del CDD"
  exit 1
}

make clean && make
if [ $? -ne 0 ]; then
  echo "[ERROR] Falló la compilación del módulo"
  exit 1
fi

# === Paso 2: Remover módulo si ya está cargado ===
if lsmod | grep -q "$CDD_NAME"; then
  echo "[+] Removiendo módulo existente..."
  sudo rmmod "$CDD_NAME"
fi

# === Paso 3: Insertar módulo nuevo ===
echo "[+] Insertando módulo..."
sudo insmod "$MODULE_NAME"
if [ $? -ne 0 ]; then
  echo "[ERROR] No se pudo insertar el módulo"
  exit 1
fi

# === Paso 4: Verificación del archivo de dispositivo ===
if [ ! -e "$MAJOR_FILE" ]; then
  echo "[!] Esperando que udev cree /dev/$CDD_NAME..."
  sleep 1
fi

if [ ! -e "$MAJOR_FILE" ]; then
  echo "[ERROR] No se encontró /dev/$CDD_NAME. ¿udev está funcionando?"
  exit 1
fi

# === Paso 5: Asegurar permisos adecuados ===
sudo chmod 666 "$MAJOR_FILE"

cd - >/dev/null

# === Paso 6: Ejecutar la app Python ===
echo "[+] Ejecutando app de usuario..."
python3 "$USER_APP"

make clean
