# Trabajo Práctico N°3: Modo Protegido

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

La opción `-g` en el comando `as` genera información de depuración, que puede ser útil para el análisis posterior. La opción `--oformat binary` en el comando `ld` indica que se debe generar un archivo binario plano, que es el formato esperado por QEMU.

La opción `-T` en el comando `ld` especifica el script de enlazador a utilizar. En este caso, se utiliza el script `link.ld`, que define la estructura del archivo ejecutable.

La opción `-hda` en el comando `qemu-system-x86_64` especifica el archivo de imagen a utilizar como disco duro virtual. En este caso, se utiliza el archivo `main.img`, que contiene el bootloader.

!["Ejecución del programa"](./Imagenes/qemu-hello-world.png)

##### Salida de `objdump`

Muestra el desensamblado del archivo main.img interpretándolo como código i8086 desde el offset 0. Identifica las instrucciones iniciales (`mov`,  `lods`, `int`, `hlt`). Luego objdump continúa desensamblando más allá de `hlt` (offset `0xe`), tratando los siguientes bytes como código.

!["Objdump"](./Imagenes/objdump.png)

##### Salida de `hd`

Muestra los bytes crudos del archivo desde el offset `0`. Confirma la secuencia de bytes vista por `objdump` (`be 0f 7c...`). Crucialmente, su vista ASCII revela la cadena `"hello world"` exactamente en los bytes que siguen a la instrucción `hlt`.

!["Hexdump"](./Imagenes/hexdump.png)

>[!NOTE]
>Ambas salidas se encuentran completas sus en respectivos archivos de texto. La salida de `objdump` se encuentra en `Archivos/objdump.txt` y la salida de `hd` se encuentra en `Archivos/hexdump.txt`.

La coincidencia de bytes entre ambas herramientas y la revelación de la cadena de texto por `hd` confirman que el programa **(código + datos)** está colocado al inicio del archivo `main.img` (offset `0`). Ambas salidas muestran que el archivo tiene `512 bytes` y termina con la firma de arranque `55 aa`.

#### Debuggeando con GDB y QEMU

Para depurar el programa, se utiliza GDB junto con QEMU. Esto permite inspeccionar el estado del programa en ejecución, incluyendo los registros y la memoria.

```bash
qemu-system-i386 -drive format=raw,file=./Archivos/01HelloWorld/main.img -boot a -s -S -monitor stdio
```