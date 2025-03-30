# Introduccion

El objetivo de este informe es aplicar los conocimientos adquiridos sobre el rendimiento y la performance de los sistemas computacionales, con el fin de tomar decisiones informadas sobre el hardware y optimizar el código. Esta tarea se divide en dos partes: la primera consiste en utilizar benchmarks de terceros para evaluar y comparar el rendimiento de distintos componentes de hardware, mientras que la segunda se centra en el análisis del rendimiento de nuestro propio código mediante herramientas de time profiling.

## Desarrollo

### Benchmarks para tareas diarias

| **Tarea Diaria**                        | **Benchmark Representativo** | **Descripción**                                                                                                                                      |
| --------------------------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Desarrollo de software**              | `Phoronix Test Suite`        | Suite completa de benchmarks que evalúa el rendimiento del sistema en diversas tareas, incluyendo compilación y rendimiento de aplicaciones.         |
|                                         | `time make -j$(nproc)`       | Comando de terminal utilizado para medir el tiempo de compilación en proyectos grandes, aprovechando todos los núcleos de CPU disponibles.           |
|                                         | `Cinebench R23`              | Benchmark que mide el rendimiento de la CPU en tareas de renderizado 3D, útil para evaluar el rendimiento de procesadores en entornos de desarrollo. |
| **Redes y comunicación**                | `iPerf`                      | Herramienta de línea de comandos que mide el rendimiento de la red, específicamente el ancho de banda y la latencia, en pruebas TCP/UDP.             |
|                                         | `netperf`                    | Benchmark que evalúa el rendimiento de redes, incluyendo el rendimiento de TCP y UDP en condiciones de red controladas.                              |
|                                         | `ping -f`                    | Comando para probar la conectividad de red y medir la latencia mediante el envío de paquetes ICMP en modo "flood".                                   |
|                                         | `Wireshark` (análisis)       | Herramienta de análisis de paquetes de red que permite inspeccionar el tráfico y rendimiento de la red en tiempo real.                               |
| **Navegación web**                      | `JetStream 2`                | Benchmark que evalúa el rendimiento de los navegadores en la ejecución de aplicaciones web complejas, como JavaScript.                               |
|                                         | `Speedometer 2.0`            | Mide el rendimiento de navegación web, evaluando la capacidad de respuesta del navegador al interactuar con aplicaciones web dinámicas.              |
|                                         | `MotionMark`                 | Benchmark que evalúa el rendimiento gráfico de los navegadores, especialmente en la ejecución de gráficos y animaciones.                             |
|                                         | `Octane`                     | Benchmark enfocado en medir el rendimiento de JavaScript en los navegadores web, evaluando cómo manejan aplicaciones y scripts complejos.            |
| **Multitarea**                          | `Geekbench Multi-Core`       | Mide el rendimiento del procesador en tareas de múltiples núcleos, evaluando cómo maneja tareas que requieren alta concurrencia.                     |
|                                         | `PCMark`                     | Evaluación de rendimiento en tareas diarias de productividad, incluyendo multitarea, como navegar y usar aplicaciones ofimáticas.                    |
|                                         | `Phoronix Multitasking`      | Parte de la suite Phoronix, mide el rendimiento del sistema bajo condiciones de multitarea intensiva.                                                |
| **Reproducción de video y streaming**   | `YouTube Playback Benchmark` | Evalúa el rendimiento de la CPU y la GPU en la reproducción de contenido en YouTube, midiendo la fluidez y el uso de recursos.                       |
|                                         | `VLC Benchmark`              | Mide el rendimiento de la decodificación de video utilizando el popular reproductor multimedia VLC.                                                  |
| **Gaming**                              | `3DMark`                     | Benchmark que mide el rendimiento gráfico y de CPU en juegos 3D, evaluando la capacidad de procesamiento de los gráficos del sistema.                |
|                                         | `Unigine Heaven`             | Test gráfico que evalúa el rendimiento 3D de la GPU en entornos de alta demanda gráfica, simulando juegos y aplicaciones visualmente intensivas.     |
| **Servidores - Procesamiento de datos** | `SPEC CPU`                   | Benchmark de rendimiento de CPU que mide el desempeño de la CPU en tareas intensivas como la compilación y simulaciones científicas.                 |
|                                         | `Sysbench`                   | Herramienta para evaluar el rendimiento de CPU, memoria y bases de datos, utilizada para pruebas de servidores y sistemas.                           |
|                                         | `TPC-C Benchmark`            | Benchmark que evalúa el rendimiento de las bases de datos transaccionales simulando un entorno de servidor de base de datos real.                    |
|                                         | `fio` (almacenamiento)       | Benchmark que mide el rendimiento de entrada/salida de almacenamiento, evaluando la capacidad de lectura/escritura de discos y SSDs.                 |

### Rendimiento al compilar el kernel de Linux

El rendimiento de un sistema se mide por su capacidad para completar una tarea en un tiempo determinado. Utilizando los tiempos de ejecución, podemos calcular el rendimiento absoluto:

$$ \text{Rendimiento} = \frac{1}{T} $$

La siguiente tabla muestra los tiempos y rendimientos de los procesadores:

| Procesador        | Tiempo (s) | Rendimiento absoluto (1/s) |
| ----------------- | ---------- | -------------------------- |
| Intel i5-13600K   | 83 ± 3     | 0.012                      |
| AMD Ryzen 9 5900X | 97 ± 6     | 0.010                      |
| AMD Ryzen 9 7950X | 53 ± 3     | 0.019                      |

Para calcular la aceleración del **AMD Ryzen 9 7950X 16-Core**, usamos la fórmula de **Speedup**:

$$ \text{Speedup} = \frac{T*{\text{base}}}{T*{\text{Ryzen 9 7950X}}} $$

#### Comparación con Intel Core i5-13600K:

$$ \text{Speedup} = \frac{83}{53} = 1.566 $$

#### Comparación con AMD Ryzen 9 5900X:

$$ \text{Speedup} = \frac{97}{53} = 1.830 $$

#### Aceleracion al usar AMD Ryzen 9 7950X 16-Core

El **Ryzen 9 7950X** es **1.57 veces más rápido** que el **i5-13600K** y **1.83 veces más rápido** que el **Ryzen 9 5900X** al compilar el kernel de Linux. Además, su eficiencia energética lo hace ideal para tareas relacionadas a la compilación y servidores, siendo una opción destacada por su rendimiento y economía de energía.
