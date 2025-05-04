/* Definicion de constantes */    
    .equ CODE_SEG, 8
    .equ DATA_SEG, gdt_data - gdt_start

    /* Modo 16 bits */
    .code16
    cli

    /* Carga la dirección base y el tamaño de la Tabla de Descriptores Globales (GDT) */
    /* en el registro GDTR del procesador */
    lgdt gdt_descriptor

    /* Setea el bit PE (Protection Enable) en CR0 (Control Register 0) */
    /* Esto permite entrar efectivamente al protected mode */
    mov %cr0, %eax
    orl $0x1, %eax
    mov %eax, %cr0

    ljmp $CODE_SEG, $protected_mode

gdt_start:
/* Entrada nula */
gdt_null:
    .long 0x0
    .long 0x0
/* Segmento de codigo */
gdt_code:
    .word 0xffff
    .word 0x0
    .byte 0x0
    .byte 0b10011010
    .byte 0b11001111
    .byte 0x0
/* Segmento de datos */
gdt_data:
    .word 0xffff
    .word 0x0
    .byte 0x0
    .byte 0b10010010
    .byte 0b11001111
    .byte 0x0
gdt_end:
/* Descriptor */
gdt_descriptor:
    .word gdt_end - gdt_start
    .long gdt_start
vga_current_line:
    .long 0
    
.code32
protected_mode:
    /* Configurar los demas segmentos */
    mov $DATA_SEG, %ax
    mov %ax, %ds
    mov %ax, %es
    mov %ax, %fs
    mov %ax, %gs
    mov %ax, %ss

    /* Para que no se pise el stack */
    mov $0X7000, %ebp

    mov %ebp, %esp 

    /* Finaliza la inicializacion del modo protegido */
    
    /* VGA_PRINT_STRING */

    push %eax
    push %ebx
    push %ecx
    push %edx

    mov $message, %ecx
    mov vga_current_line, %eax
    mov $0, %edx
    /* Número de líneas horizontales. */
    mov $25, %ebx
    div %ebx
    mov %edx, %eax
    /* 160 == 80 * 2 == ancho de línea * bytes por carácter en pantalla */
    mov $160, %edx
    mul %edx
    /* 0xb8000 == dirección de memoria de vídeo que se muestra en la pantalla. */
    lea 0xb8000(%eax), %edx
    mov $0x0f, %ah

/* Bucle que copia una cadena de texto desde una dirección de memoria a la 
/* memoria de video VGA, caracter por caracter. */
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

    /* Fin VGA_PRINT_STRING */

message:
    .asciz "Hello Protected World!"