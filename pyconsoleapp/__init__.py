import pinjector

from pyconsoleapp.console_app import ConsoleApp
from pyconsoleapp.console_app_component import ConsoleAppComponent
from pyconsoleapp import utilities
from pyconsoleapp import configs

# Configure the DI;
pinjector.create_namespace('pyconsoleapp')
pinjector.register('pyconsoleapp', utilities)
pinjector.register('pyconsoleapp', configs)