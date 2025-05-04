# Trabajo Práctico N°3: Protected Mode

### `Breaking Bytes`

- SAILLEN, Simón.
- VARGAS, Rodrigo Sebastian.
- ZÚÑIGA, Guillermo Rubén Darío.

## Introducción

## Desarrollo

### UEFI / Coreboot

>[!NOTE]
>COPIAR PARTE UEFI COREBOOT DE RUBEN

### Linker

Un enlazador (linker) es una herramienta esencial en el proceso de compilación de un programa. Permite combinar varios modulos objeto en un solo archivo ejecutable que puede correr en un sistema.

La tarea del enlazador es manejar y conectar diferentes piezas de codigo y datos, asegurando que todas las referencias entre los mismos sean resueltas apropiadamente.

#### Linker Script

Un script de enlazador es un archivo de texto que contiene instrucciones para el enlazador sobre cómo debe organizar y combinar los modulos objeto. Define la estructura del archivo ejecutable final, incluyendo la ubicacion de las secciones de codigo y datos, y como deben ser alineadas en memoria.

EL script linker a utilizar en este trabajo es el siguiente:

```Linker Script
SECTIONS
{
    . = 0x7c00;
    .text :
    {
        __start = .;
        *(.text)
        . = 0x1FE;
        SHORT(0xAA55)
    }
}
```

>[!NOTE]
>Se quitaron los comentarios para que el script sea más legible.

##### Explicación del script

La dirección `0x7c00` es la dirección de carga del bootloader en la memoria. El bootloader se carga en esta dirección por el BIOS al iniciar el sistema. Esto es importante porque el bootloader debe saber dónde se encuentra en memoria para poder ejecutar correctamente el código.

La directiva `__start` define una etiqueta que representa la dirección de inicio de la sección `.text`. Esta etiqueta puede ser utilizada en el código para referirse a la dirección de inicio de la sección.

La sección `.text` contiene el código ejecutable del bootloader. La directiva `*` indica que se deben incluir todas las secciones de código de los modulos objeto.

La directiva `0x1FE` indica la dirección de la tabla de particiones en el disco. Esta dirección es importante porque el bootloader debe leer la tabla de particiones para poder cargar el sistema operativo.

La directiva `SHORT(0xAA55)` indica que se debe escribir el valor `0xAA55` en la dirección `0x1FE`. Este valor es la firma del bootloader y es utilizado por el BIOS para identificar un sector de arranque válido. Si el bootloader no contiene esta firma, el BIOS no podrá cargarlo y el sistema no podrá arrancar.

#### Comparativa entre la salida de objdump y hd

Utilizando el siguiente codigo en Assembly (`01HelloWodl/main.S`):

```Assembly
.code16
    mov $msg, %si
    mov $0x0e, %ah
loop:
    lodsb
    or %al, %al
    jz halt
    int $0x10
    jmp loop
halt:
    hlt
msg:
    .asciz "hello world"
```

El programa en ensamblador realiza una simple tarea: imprime el mensaje "hello world" en la pantalla utilizando la interrupción de BIOS `0x10`. La directiva `.code16` al inicio del código indica que el programa debe ejecutarse en modo real de 16 bits, que es el modo utilizado por el BIOS para interactuar con el hardware.

##### Compilación y enlazado

Para compilar, enlazar y ejecutar el programa, se utilizan los siguientes comandos:

```bash
as -g -o main.o main.S
ld --oformat binary -o main.img -T link.ld main.o
qemu-system-x86_64 -hda main.img
```