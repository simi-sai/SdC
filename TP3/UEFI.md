# UEFI

## Definicion

La Interfaz de Firmware Extensible Unificada​ o UEFI (del inglés unified extensible firmware interface) es una especificación que define una interfaz entre el sistema operativo y el firmware. UEFI reemplaza la antigua interfaz del Sistema Básico de Entrada y Salida (BIOS) estándar presentado en los PC IBM.

La UEFI puede proporcionar menús gráficos adicionales e incluso proporcionar acceso remoto para la solución de problemas o mantenimiento. 

## Como usarlo

Las placas base UEFI de última generación vienen con UEFI Interactive Shell. El shell interactivo UEFI es un programa de shell simple (como bash) responsable de iniciar su sistema operativo. También puede usar el shell interactivo de UEFI para ejecutar scripts y comandos de shell de EFI. 
Ver: https://es.linux-console.net/?p=15881

## Vulnerabilidades

- Implantes en la cadena de fabricacion (sabotajes)
- Bugs en el codigo fuente
- Mala configuracion durante la fabricacion:
    - El proveedor deja encendido el modo Debug
    - El flash se deja desbloqueado
    - Se dejan test keys en el firmware

Ver: https://firmguard.com/uefi-bios-firmware-vulnerabilities-where-do-they-come-from/

# CSME e Intel MEBx

El Converged Security and Management Engine o CSME es un asistente de deteccion de vulnerabilidades sobre el UEFI, los drivers y todos los procesos sensibles que realiza el procesador.

# Coreboot

Coreboot es una BIOS libre y ligera diseñado para realizar solamente el mínimo de tareas necesarias para cargar y correr un sistema operativo moderno de 32 bits o de 64 bits.

Hoy en dia es incorporado por las computadoras ThinkPad, Chromebook, Purism, System76, etc.

Su ventaja no reside en una necesidad tecnológica, sino en una ética, ya que para los desarrolladores de este proyecto es importante que todo el software del PC sea libre, y el BIOS ha sido el único que ha quedado olvidado. Los autores esperan que en los próximos años algunos fabricantes estén dispuestos a distribuirlo en sus máquinas, debido a su carácter gratuito. 

