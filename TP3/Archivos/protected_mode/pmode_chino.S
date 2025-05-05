# Modo protegido sin macros

# Seteo del estado inicial
    
    .code16 # Ingresar al modo real (16 bits)
    cli     # Deshabilitar interrupciones

    # Limpieza de todos los registros de segmento.
    # Esto se cree que NO es obligatorio
    ljmp $0, $1f    # Setear CS en cero
    1:
    xor %ax, %ax    # Cargar valor 0 en AX
    mov %ax, %ds    # Limpiar DS
    mov %ax, %es    # Limpiar ES
    mov %ax, %fs    # Limpiar FS
    mov %ax, %gs    # Limpiar GS
    mov %ax, %bp    # Limpiar BP

    # Automaticamente se deshabilitan las interrupciones hasta el final de la proxima instruccion

    mov %ax, %ss    # Limpiar SS
    mov %bp, %sp    # Setear SP porque la BIOS podria depender de él

# Limpieza de la pantalla: No es necesario hacerlo

    mov $0x0600, %ax
    mov $0x7, %bh
    mov $0x0, %cx
    mov $0x184f, %dx
    int $0x10

    # BIOS
    mov $0x02, %ah
    mov $0x00, %bh
    mov $0, %dh
    mov $0, %dl
    int $0x10

# Configuracion del Modo Protegido
    # Definiciones
    .equ CODE_SEG, 8
    .equ DATA_SEG, gdt_data - gdt_start

    lgdt gdt_descriptor # Indicar al procesador donde se encuentra la GDT en la memoria

    # Setear el bit PE (Protection Enable) del CR0, entrando al modo protegido
    mov %cr0, %eax
    orl $0x1, %eax
    mov %eax, %cr0

    ljmp $CODE_SEG, $protected_mode

gdt_start:
gdt_null:
    .long 0x0
    .long 0x0
gdt_code:
    .word 0xffff
    .word 0x0
    .byte 0x0
    .byte 0b10011010
    .byte 0b11001111
    .byte 0x0
gdt_data:
    .word 0xffff
    .word 0x0
    .byte 0x0
    .byte 0b10010010
    .byte 0b11001111
    .byte 0x0
gdt_end:
gdt_descriptor:
    .word gdt_end - gdt_start
    .long gdt_start
vga_current_line:
    .long 0
    
    .code32
protected_mode:

    # Setear los registros de segmento para actualizar el cache del descriptor
    mov $DATA_SEG, %ax
    mov %ax, %ds
    mov %ax, %es
    mov %ax, %fs
    mov %ax, %gs
    mov %ax, %ss
    mov $0X7000, %ebp
    mov %ebp, %esp

# Impresión en VGA
    
    push %eax
    push %ebx
    push %ecx
    push %edx

    mov $message, %ecx
    mov vga_current_line, %eax
    mov $0, %edx
    /* Numero de lineas horizontales */
    mov $25, %ebx
    div %ebx
    mov %edx, %eax
    /* 160 == 80 * 2 == ancho de linea * bytes por caracter en la pantalla */
    mov $160, %edx
    mul %edx
    /* 0xb8000 == dirección de memoria de vídeo que se muestra en la pantalla */
    lea 0xb8000(%eax), %edx
    /* White on black. */
    mov $0x0f, %ah
loop:
    mov (%ecx), %al
    cmp $0, %al
    je end
    mov %ax, (%edx)
    add $1, %ecx
    add $2, %edx
    jmp loop
end:
    incl vga_current_line

    pop %edx
    pop %ecx
    pop %ebx
    pop %eax

    jmp .

message:
    .asciz "hello world"
