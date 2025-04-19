# filepath: /home/ruben/Documents/SdC/TP2/python_C_asm/lib_send_gini.py
from msl.loadlib import Server32
import ctypes

class LibSendGini(Server32):
    def __init__(self, host, port, quiet, **kwargs):
        super().__init__('c_lib_send_gini.so', 'cdll', host, port, quiet)

    def add_one(self, gini_value):
        self.lib._gini.argtypes = [ctypes.c_int]
        self.lib._gini.restype = ctypes.c_int
        return self.lib._gini(gini_value)
