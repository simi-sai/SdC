# Trabajo Práctico N°2: Stack frame

### `Breaking Bytes`

- SAILLEN, Simón.
- VARGAS, Rodrigo Sebastian.
- ZÚÑIGA, Guillermo Rubén Darío.

## Introducción

Se diseñó e implementó una interfaz que adquiere el índice GINI de un país, realizando una consulta a la base de datos del banco mundial (https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22), y realiza un cálculo matemático utilizando éste índice. La interfaz consiste de tres capas: una superior realizada en Python, que recupera el índice GINI; mientras que una intermedia realizada en C entrega el dato a una capa inferior en Ensamblador quien es el que suma 1 al índice. Este resultado es mostrado en la capa superior.

## Desarrollo

### 1° Iteración: Uso de Python y C

En este primer caso se realizo la suma del índice en C sin Ensamblador. El índice es convertido a entero en Python y luego es sumado en C.

Para esto se utilizó la librería `requests` para enviar solicitudes HTTP a la página del banco mundial, y `ctypes` para que Python pueda llamar a una función de una librería compartida de C.

```Python
# worldbank.py
# -------------

import requests
import ctypes

# Specify country and year
country_searched = "Argentina"
year_searched = "2020"

api_url = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"

# Search GINI index for the specified country and year
def fetch_gini_index(country_searched, year_searched) -> int:
    response = requests.get(api_url)
    data = response.json()
    gini_val = 0
                
    for item in data[1]:
        country = item.get('country', {}).get('value')
        year = item.get('date')
        
        if country == country_searched and year == year_searched:
            gini_val = item.get('value')
        else:
            continue
                
    return gini_val

# Load C library
lib_send_gini = ctypes.CDLL('./lib_send_gini.so', mode=ctypes.RTLD_GLOBAL)
    
# Set argument and return types
lib_send_gini._gini.argtypes = (ctypes.c_int,)
lib_send_gini._gini.restype = (ctypes.c_int)

# Define python function
def send_gini(num):
    return lib_send_gini._gini(num)

old_gini = fetch_gini_index(country_searched, year_searched)

print("Gini viejo: ", old_gini)
print("Gini actualizado: ", send_gini(int(old_gini)))
```

```C
// send_gini.c
// ------------

int _gini(int gini_val){
    return gini_val + 1;
}
```

![Prueba Python y C](img/py_c.png)

### 2° Iteración: Uso de C y Assembly

En este caso se enfocó en lograr llamar a un subprograma de ensamblador en C, y para esto se requirió el conocimiento de la convencion de llamada de C. Con esto se logró enviar un entero fijo al subprograma para incrementar en 1 su valor.

```C
// send_gini.c
// ------------

int _gini(int gini_val){
    int gini_plus = asm_main(gini_val);
    return gini_plus;
}

int main(){
    int gini_actual = 10;
    printf("%d",_gini(gini_actual));
    return 0;
}
```

```x86asm
; asm_gini.asm
; -------------

; subroutine asm_main
;
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

```

![Prueba C a assembly](img/c_asm.png)