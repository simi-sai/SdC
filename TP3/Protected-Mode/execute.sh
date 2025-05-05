#!/bin/bash

as -g -o pmode_bb.o pmode_bb.S
ld --oformat binary -o pmode_bb.img -T linker.ld pmode_bb.o

# Preguntar al usuario qué hacer
echo "¿Qué querés hacer?"
echo "1) Ejecutar normalmente"
echo "2) Ejecutar con GDB (debug mode)"
read -p "Elegí una opción (1/2): " opcion

if [ "$opcion" == "2" ]; then
  echo "🚀 Ejecutando QEMU con GDB (puerto abierto en 1234)..."
  qemu-system-i386 -hda pmode_bb.img -s -S
else
  echo "🚀 Ejecutando QEMU normalmente..."
  qemu-system-i386 -hda pmode_bb.img
fi
