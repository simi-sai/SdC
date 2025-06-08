# Trabajo Práctico N°5: Drivers de Dispositivos

### `Breaking Bytes`

- SAILLEN, Simón.
- VARGAS, Rodrigo Sebastian.
- ZÚÑIGA, Guillermo Rubén Darío.

## Introducción

## Desarrollo

### Driver

Un driver (o *controlador*) es un programa que permite la comunicación entre el sistema operativo y un dispositivo de hardware. Los drivers son esenciales para que el sistema operativo pueda interactuar con los dispositivos conectados, como impresoras, discos duros, tarjetas gráficas, etc.

Los drivers son generalmente específicos para cada tipo de dispositivo y sistema operativo. Pueden ser proporcionados por el fabricante del hardware o desarrollados por la comunidad de código abierto. Los drivers pueden ser de espacio de usuario o de espacio del kernel, dependiendo de cómo interactúan con el sistema operativo.

### Device Controller

Un device controller (o *controlador de dispositivo*) es un componente electrónico físico, a menudo un chip o una placa de circuito, que se encuentra directamente en el dispositivo de hardware o en la placa base de la computadora. Su función principal es gestionar y controlar las operaciones del dispositivo de hardware al que está asociado. Esencialmente, el device controller maneja las complejidades de bajo nivel del hardware, liberando al procesador principal de esta tarea y permitiendo que el sistema operativo interactúe con el dispositivo a un nivel más abstracto.

#### Device Drivers

Los device drivers (o *controlador de dispositivos*) son programas que permiten al sistema operativo comunicarse con los **device controllers**. Estos drivers traducen las solicitudes del sistema operativo en comandos que el device controller puede entender y viceversa. Los device drivers son esenciales para el funcionamiento de los dispositivos de hardware, ya que permiten que el sistema operativo y las aplicaciones interactúen con ellos de manera efectiva.

### Bus Driver

Un bus driver (o *controlador de bus*) es un tipo especializado de driver que se encarga de gestionar la comunicación a través de un bus del sistema. Es un componente crítico en la arquitectura de computadoras, ya que permite que múltiples dispositivos se comuniquen a través de un canal compartido. Los bus drivers son responsables de la gestión de la transferencia de datos entre el bus y los dispositivos conectados, asegurando que los datos se transmitan correctamente y sin conflictos.

Las responsabilidades principales de un bus driver incluyen:

- **Enumerar dispositivos:** Descubrir qué dispositivos están conectados a un bus específico. Por ejemplo, un controlador de bus USB detectará cada nuevo dispositivo USB que se conecte.
- **Gestión del Plug and Play (PnP):** Responder a eventos como la conexión o desconexión de dispositivos y la asignación de recursos (como direcciones de memoria o interrupciones) a esos dispositivos.
- **Arbitraje y Multiplexación:** En buses donde varios dispositivos pueden intentar comunicarse al mismo tiempo, el bus driver se encarga de arbitrar el acceso para evitar colisiones y asegurar una comunicación ordenada.
- **Manejo genérico de dispositivos:** Proporcionar una interfaz común para que el sistema operativo y otros drivers puedan interactuar con los dispositivos conectados a ese bus, sin tener que conocer los detalles específicos de cada dispositivo individual.

### CDD: Character Device Driver

Un Character Device Driver (o *controlador de dispositivo de carácter*) es un tipo específico de controlador de dispositivo diseñado para gestionar dispositivos que manejan datos como un flujo de bytes o caracteres individuales, en lugar de bloques de tamaño fijo. A diferencia de los controladores de dispositivo de bloque, los controladores de dispositivo de carácter no suelen implicar el almacenamiento en búfer de grandes cantidades de datos, en cambio, proporcionan una interfaz directa, byte a byte, para que las aplicaciones interactúen con el hardware.

El Sistema Operativo utiliza el CDD para:

- **Leer datos:** Cuando se escribe en un teclado, el CDD lee cada carácter y lo pasa al sistema operativo, que luego lo envía a la aplicación en uso.
- **Escribir datos:** Cuando una aplicación envía datos a un puerto serie o a una impresora, el CDD traduce esos datos a las señales específicas que el hardware entiende, enviándolos carácter por carácter.
- **Controlar operaciones específicas del dispositivo:** Los CDD a menudo incluyen funciones especializadas (como `ioctl` en sistemas tipo Unix) que permiten a las aplicaciones realizar controles específicos del dispositivo que no son solo lectura o escritura de bytes. Por ejemplo, cambiar la velocidad de transmisión (baudios) de un puerto serie.

Para acceder a estos dispositivos, se utilizan los **Character Device Files (CDF)**, que son archivos especiales en el sistema de archivos que representan estos dispositivos. Estos archivos permiten a las aplicaciones interactuar con los dispositivos de carácter como si fueran archivos normales, utilizando las llamadas al sistema estándar para leer y escribir datos. En linux estos archivos se encuentran en el directorio `/dev/`.

#### Par de Números <Major, Minor>

El vínculo entre un dispositivo (CDF) y su controlador (Device Driver) en sistemas operativos como Linux se establece a través de un par de números conocidos como **Major** y **Minor**. Estos números son utilizados por el kernel para identificar de manera única cada dispositivo y su controlador asociado. Este par de números se puede observar mediante los comandos:

```bash
ls -l /dev/ | grep "^c" # Para listar los archivos de dispositivo de carácter
cat /proc/devices #Para ver los números Major
ls -la /dev/hda? /dev/sda? /dev/ttyS? # Para ver los números Major y Minor de dispositivos específicos
```

Por ejemplo, al ejecutar `ls -l /dev/ttyS0`, se puede ver algo como:

```console
crw-rw---- 1 root dialout 4, 64 jun  8 16:31 /dev/ttyS0
```

En este caso, el número `4` es el **Major** y `64` es el **Minor**, formando el par **<4, 64>**. El Major identifica el tipo de dispositivo (en este caso, un dispositivo de carácter), mientras que el Minor identifica una instancia específica del dispositivo (por ejemplo, el primer puerto serie).

---

### Construcción de un CDD para Sensar Señales

Debemos desarrollar un Character Device Driver (CDD) que genere dos señales periódicas con un periodo de 1 segundo. Luego una aplicación a nivel de usuario deberá leer una de las dos señales y graficarla en función del tiempo. La aplicación tambien debe poder indicarle al CDD cuál de las dos señales leer. 

Las correcciones de escalas de las mediciones, de ser necesario, se harán a nivel de usuario. Los gráficos de la señal deben indicar el tipo de señal que se está sensando, unidades en abscisas y tiempo en ordenadas. Cuando se cambie de señal el gráfico se debe "resetear" y acomodar a la nueva medición.

#### Paso 1: Estructura básica del módulo

La estructura básica del módulo incluye:

- Inclusión de headers necesarios (`linux/module.h`, `linux/fs.h`, etc.).
- Definición de variables globales para el manejo de señales y sincronización.
- Implementación de las funciones principales del driver: `open`, `read`, `release` y `ioctl` (o `unlocked_ioctl`).
- Definición de una estructura `file_operations` que asocia las funciones del driver con las operaciones de archivo correspondientes.
- Inicialización y limpieza del módulo mediante las funciones `module_init` y `module_exit`.

#### Paso 2: Carga y registro del módulo como dispositivo de carácter

Para registrar el driver como un dispositivo de carácter:

- Se utiliza `register_chrdev` para obtener un número mayor dinámico y asociar el driver con el sistema.
- Se crea el archivo de dispositivo correspondiente en `/dev/` usando `mknod` o mediante `udev`.
- El módulo implementa las funciones de inicialización y salida para registrar y desregistrar el dispositivo correctamente.
- Se asegura la correcta gestión de recursos y la liberación de memoria al remover el módulo.

#### Paso 3: Personalización y Extensión del Módulo

Las modificaciones específicas realizadas incluyen:

- Generación de dos señales periódicas (cuadrada y triangular) utilizando temporizadores del kernel (`hrtimer` o `timer_list`).
- Implementación de un mecanismo para seleccionar la señal a sensar mediante una llamada `ioctl` desde espacio de usuario.
- Sincronización del acceso a las señales usando mecanismos como `wait_queue` o semáforos para evitar condiciones de carrera.
- Adaptación de la función `read` para entregar muestras de la señal seleccionada en intervalos de 1 segundo.
- Manejo de cambios de señal, reiniciando el estado interno y notificando a la aplicación usuaria para que reinicie el gráfico.


## Conclusion