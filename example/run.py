# Add this folder to the path;
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Imports;
import pinjector

from pyconsoleapp.console_app import ConsoleApp
from pyconsoleapp import configs

# Create the app instance;
app = ConsoleApp('PyDiet')

# Register the package containing the components;
app.register_component_package('example.components')

app.root_route('home', 'MainMenuComponent')
app.add_route('home.ingredients', 'IngredientMenuComponent')
app.add_route('home.ingredients.new', 'IngredientEditMenuComponent')
app.add_route('home.ingredients.new.name', 'IngredientNameEditorComponent')

# Customise any configs;
configs.terminal_width_chars = 60

# Run the app;
app.run()