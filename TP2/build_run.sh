#!/bin/bash

# Dependency installation
sudo dpkg --add-architecture i386
sudo apt update
sudo apt install libz1:i386
sudo apt install libc6:i386 gcc-multilib g++-multilib
sudo apt install nasm build-essential

# Virtual environment setup
python3 -m venv venv
. venv/bin/activate
pip install requests
pip install msl-loadlib
echo ""
echo "Instalación de dependencias completada"

set -e  # Exit on first error

# Cleaning previous builds
rm -f *.o *.so

# Assembling asm_gini.asm
nasm -f elf32 asm_gini.asm -o asm_gini.o

# Compiling send_gini.c 
gcc -m32 -c send_gini.c -o send_gini.o

# Linking into shared library lib_send_gini.so
gcc -m32 -shared -W -o lib_send_gini.so send_gini.o asm_gini.o

echo "[✓] Build successful: lib_send_gini.so created."
echo "[▶] Running Python script..."
python3 asm_worldbank.py
