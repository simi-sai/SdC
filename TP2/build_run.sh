#!/bin/bash

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
