# Tutorial Time Profiling

## Herramienta GNU GCC Profiling

Se realizó el tutorial sobre la generación de archivos de perfil en los códigos `test_gprof.c` y `test_gprof_new.c`.  

Se agregó la opción '-pg' en el
paso de compilación. Se puede observar la creacion del binario `test_gprof`.
![Compilacion](img/tp1_01.png)
![Reorganizacion de los archivos](img/tp1_02.png)

Luego de ejecutarlo se crea el archivo `gmon.out`.
![Ejecucion del binario](img/tp1_03.png)
![Archivo gmon.out](img/tp1_04.png)

Se ejecutó posteriormente la herramienta Gprof produciendo el archivo de análisis.
![Ejecucion gprof](img/tp1_05.png)
![Texto en analysis.txt](img/tp1_06.png)

Se personalizó el archivo con distintos comandos.
![gprof -a](img/tp1_07.png)
![gprof -b](img/tp1_08.png)
![gprof -p -b](img/tp1_09.png)
![gprof -pfun1 -b](img/tp1_10.png)

Para ver un gráfico de la salida de gprof, se utilizó gprof2dot que genera una imagen .png del mismo.
![Generacion del grafico](img/tp1_14.png)
![Grafico del perfil](img/profile.png)

## Herramienta Perf
Para este caso, se realizó el perfil del programa con Linux Perf.
![Ejecucion del perfil](img/tp1_11.png)
![Lista de funciones mostrada por Perf](img/tp1_12.png)

Esta herramienta es interesante ya que permite ver en codigo ensamblador a las distintas funciones del programa.
![Codigo ensamblador de la funcion new_func1](img/tp1_13.png)
