; subroutine asm_main
; Input Parameter:
;   gini_val    - what to increment to (at [ebp + 8])
; Return value:
;   gini_val + 1

%include "asm_io.inc"

; Code
segment .text
        global  asm_main
asm_main:
        enter   0,0               ; Setup routine
        
        mov     eax,[ebp+8]
        inc     eax               ; Add 1 to [ebp+8] (gini_val)

        leave                     ; Return to C
        ret
