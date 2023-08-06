from gpiopico.input_devices import *
from gpiopico.output_devices import *
from gpiopico.utils import *

try:
    from gpiopico.network_device import Network
except ImportError:
    print(f'Import Error, cant use Network')
    pass
