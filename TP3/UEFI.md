# UEFI

## Definicion

La Interfaz de Firmware Extensible Unificada​ o UEFI es una especificación que define una interfaz entre el sistema operativo y el firmware. UEFI reemplaza la antigua interfaz del Sistema Básico de Entrada y Salida (BIOS) estándar presentado en los PC IBM, sin embargo, UEFI requiere un modo de emulación de BIOS por razones de compatibilidad.

La UEFI puede proporcionar menús gráficos adicionales e incluso proporcionar acceso remoto para la solución de problemas o mantenimiento. 

## Como usarlo

Las placas base UEFI de última generación vienen con UEFI Interactive Shell. Este es un programa de shell simple (como bash) responsable de iniciar el sistema operativo. También se puede utilizar el shell interactivo de UEFI para ejecutar scripts y comandos de shell de EFI. 

El siguiente artículo muestra cómo acceder al shell interactivo UEFI en placas base UEFI y usar algunos de los comandos comunes de EFI en el shell interactivo UEFI: https://es.linux-console.net/?p=15881

## Vulnerabilidades

El firmware UEFI generalmente es desarrollado por compañías independientes especializados en firmware, que luego es distribuido a los proveedores de hardware, ODMs, etc. Esto, sumado a que los desarrolladores suelen confiar en componentes de código abierto, genera oportunidades para que se introduzcan vulnerabilidades durante el proceso de desarrollo.

Hay tres metodos comunes en los que las vulnerabilidades pueden ser introducidas, ya sea accidentalmente o con propósitos maliciosos.

- Implantes en la cadena de fabricacion (sabotajes)
- Bugs en el codigo fuente
- Mala configuracion durante la fabricacion:
    - El proveedor deja encendido el modo Debug
    - El flash se deja desbloqueado
    - Se dejan test keys en el firmware

Ver: https://firmguard.com/uefi-bios-firmware-vulnerabilities-where-do-they-come-from/

# CSME e Intel MEBx

El Converged Security and Management Engine o CSME es un subsistema embebido y un dispositivo PCIe que implementa un entorno informático aislado del software principal del host que ejecuta la CPU, como el BIOS, el SO y las aplicaciones; lo que le permite detectar vulnerabilidades.

El Intel Management Engine BIOS Extension (Intel MEBx) es un recurso aislado y protegido que ofrece la habilidad de cambiar o recolectar la configuración del hardware del sistema.

# Coreboot

Coreboot es una BIOS libre y ligera diseñado para realizar solamente el mínimo de tareas necesarias para cargar y correr un sistema operativo moderno de 32 bits o de 64 bits.

Hoy en dia es incorporado por las computadoras ThinkPad, Chromebook, Purism, System76, etc.

Su ventaja no reside en una necesidad tecnológica, sino en una ética, ya que para los desarrolladores de este proyecto es importante que todo el software del PC sea libre, y el BIOS ha sido el único que ha quedado olvidado. Los autores esperan que en los próximos años algunos fabricantes estén dispuestos a distribuirlo en sus máquinas, debido a su carácter gratuito. 

