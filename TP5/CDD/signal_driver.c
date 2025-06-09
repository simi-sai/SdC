/**
 * @file signal_driver.c
 * @brief Controlador de dispositivo de caracteres que simula señales cuadrada y triangular.
 */

#include <linux/cdev.h>
#include <linux/delay.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/kernel.h>
#include <linux/kthread.h>
#include <linux/module.h>
#include <linux/uaccess.h>

/**
 * @brief Nombre del dispositivo.
 */
#define DEVICE_NAME "signal_driver"

// Variables globales
static dev_t dev_num;                     // Número de dispositivo asignado dinámicamente
static struct cdev c_dev;                 // Estructura del character device
static struct class *cl;                  // Clase de dispositivo para /sys/class/
static struct task_struct *signal_thread; // Hilo kernel para simular señales

static int selected_signal = 1; // Señal seleccionada por usuario (1 o 2)
static int square_signal = 0;   // Señal cuadrada binaria
static int triangle_signal = 0; // Señal triangular creciente/decreciente
static int direction = 1;       // Dirección de la triangular (asc/desc)

/**
 * @brief Función ejecutada por el hilo kernel para simular señales.
 *
 * Genera una señal cuadrada alternando entre 0 y 1, y una señal triangular
 * que sube y baja entre 0 y 10. 
 * 
 * @note Ambas se actualizan cada segundo.
 * 
 * @return 0 al finalizar correctamente.
 */
static int signal_loop(void *data)
{
  while (!kthread_should_stop())
  {
    square_signal = !square_signal;
    triangle_signal += direction;
    if (triangle_signal >= 10 || triangle_signal <= 0)
      direction *= -1;

    msleep(1000); // Espera de 1 segundo
  }
  return 0;
}

/**
 * @brief Función de lectura desde espacio de usuario.
 *
 * @param f puntero al archivo
 * @param buf buffer de usuario donde se copiará la señal
 * @param len tamaño del buffer
 * @param off offset (sin uso aquí)
 *
 * @returns número de bytes leídos o -EFAULT si falla
 */
static ssize_t my_read(struct file *f, char __user *buf, size_t len,
                       loff_t *off)
{
  char out[4];
  int val = (selected_signal == 1) ? square_signal : triangle_signal;
  int bytes = snprintf(out, sizeof(out), "%d\n", val);
  return copy_to_user(buf, out, bytes) ? -EFAULT : bytes;
}

/**
 * @brief Cambia la señal seleccionada.
 *
 * @param f puntero al archivo
 * @param buf buffer desde el espacio de usuario ('1' o '2')
 * @param len longitud de los datos
 * @param off offset (sin uso aquí)
 *
 * @returns número de bytes escritos o -EFAULT si falla
 */
static ssize_t my_write(struct file *f, const char __user *buf, size_t len,
                        loff_t *off)
{
  char kbuf[2];
  if (copy_from_user(kbuf, buf, 1))
    return -EFAULT;

  kbuf[1] = '\0';

  selected_signal = kbuf[0] - '0'; // Convertir de char a int

  return len;
}

/**
 * @brief Tabla de operaciones del device file (VFS -> driver).
 */
static struct file_operations fops = {
    .owner = THIS_MODULE,
    .read = my_read,
    .write = my_write,
};

/**
 * @brief Función de inicialización del módulo.
 *
 * Registra el driver en el VFS, crea el nodo de dispositivo y lanza
 * un hilo kernel que simula las señales.
 * 
 * @returns 0 si se inicializa correctamente, -1 en caso de error.
 */
static int __init signal_init(void)
{
  if (alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME) < 0)
    return -1;

  if (IS_ERR(device_create(cl, NULL, dev_num, NULL, DEVICE_NAME)))
  {
    class_destroy(cl);
    unregister_chrdev_region(dev_num, 1);
    return -1;
  }

  cdev_init(&c_dev, &fops);
  
  if (cdev_add(&c_dev, dev_num, 1) < 0)
  {
    device_destroy(cl, dev_num);
    class_destroy(cl);
    unregister_chrdev_region(dev_num, 1);
    return -1;
  }

  signal_thread = kthread_run(signal_loop, NULL, "signal_thread");

  if (IS_ERR(signal_thread))
  {
    cdev_del(&c_dev);
    device_destroy(cl, dev_num);
    class_destroy(cl);
    unregister_chrdev_region(dev_num, 1);
    return PTR_ERR(signal_thread);
  }

  printk(KERN_INFO "Signal driver loaded.\n");
  return 0;
}

/**
 * @brief Limpieza del módulo al removerlo.
 */
static void __exit signal_exit(void)
{
  kthread_stop(signal_thread);
  cdev_del(&c_dev);
  device_destroy(cl, dev_num);
  class_destroy(cl);
  unregister_chrdev_region(dev_num, 1);
  printk(KERN_INFO "Signal driver unloaded.\n");
}

module_init(signal_init);
module_exit(signal_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Breaking Bytes - SdC Course");
MODULE_DESCRIPTION("Character Device Driver with Simulated Signals");
