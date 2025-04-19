# my_server.py

from msl.loadlib import Server32

class MyServer(Server32):
    """Wrapper around a 32-bit C++ library 'send_gini.so' that has an 'add' and 'version' function."""

    def __init__(self, host, port, **kwargs):
        # Load the 'send_gini' shared-library file using ctypes.CDLL
        super(MyServer, self).__init__('send_gini.so', 'cdll', host, port)

        # The Server32 class has a 'lib' property that is a reference to the ctypes.CDLL object

    def _gini(self, a):
        # The shared library's '_gini' function takes an integer as input and returns the sum
        return self.lib._gini(a)