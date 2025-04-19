# my_client.py

from msl.loadlib import Client64

class MyClient(Client64):
    """Call a function in 'send_gini.so' via the 'MyServer' wrapper."""

    def __init__(self):
        # Specify the name of the Python module to execute on the 32-bit server (i.e., 'my_server')
        super(MyClient, self).__init__(module32='my_server.py')

    def _gini(self, a):
        # The Client64 class has a 'request32' method to send a request to the 32-bit server
        # Send the 'a' argument to the '_gini' method in MyServer
        return self.request32('_gini', a)
