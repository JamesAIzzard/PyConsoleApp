import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import importlib
import importlib.util
from typing import Callable, Dict, List, Optional, TYPE_CHECKING
from tkinter import TclError
from pyconsoleapp.utility_service import UtilityService
from pyconsoleapp.route_data import RouteData
import pyconsoleapp.configs as configs
if TYPE_CHECKING:
    from pyconsoleapp.console_app_component import ConsoleAppComponent


class ConsoleApp():
    def __init__(self, name):
        self._utility_service: UtilityService = UtilityService()
        self._response: Optional[str] = None
        self._root_route: List[str]
        self._route: List[str] = []
        self._route_component_maps: Dict[str, str] = {}
        self._route_exit_guard_maps: Dict[str, str] = {}
        self._route_entrance_guard_maps: Dict[str, str] = {}
        self._components: Dict[str, ConsoleAppComponent] = {}
        self.active_components: List[ConsoleAppComponent] = []
        self._component_packages: List[str] = []
        self._quit: bool = False
        self._text_window: Optional[tk.Tk]
        self._textbox: Optional[ScrolledText]
        self.name: str = name
        self.terminal_width_chars: int = 60
        self.error_message: Optional[str] = None
        self.info_message: Optional[str] = None

        # Configure the text window;
        self._configure_text_window()

    @property
    def route(self) -> List[str]:
        if self._route == []:
            return self._root_route
        else:
            return self._route

    @route.setter
    def route(self, route: List[str]) -> None:
        route = self._complete_relative_route(route)
        # Set the route;
        if self._stringify_route(route) in self._route_component_maps.keys():
            self._route = route

    @property
    def _active_option_responses(self) -> Dict[str, Callable]:
        '''Returns a dict of all currently active option responses.

        Returns:
            Dict[str, Callable]: A dict of all currently active option
            responses.
        '''
        # Collect the option responses map from each active component;
        option_responses = {}
        for component in self._active_components:
            option_responses.update(component.option_responses)
        # Then return them;
        return option_responses

    def _complete_relative_route(self, route: List[str]) -> List[str]:
        if route[0] == '.':
            route.pop(0)
            return self._route+route
        else:
            return route

    def _configure_text_window(self) -> None:
        '''Configures the Tkinter text window.
        '''
        self._text_window = tk.Tk()
        self._text_window.geometry("500x1000")
        self._text_window.title(self.name)
        self._textbox = ScrolledText(self._text_window)
        self._textbox.pack(expand=True, fill='both')
        # Window may have popped up, so hide it;
        self.hide_text_window()

    def _stringify_route(self, route: List[str]) -> str:
        s = ">"
        return s.join(route)

    def _listify_route(self, route: str) -> List[str]:
        return route.split(">")

    def _get_component_for_route(self, route: List[str]) -> 'ConsoleAppComponent':
        route_key = self._stringify_route(route)
        component_name = self._route_component_maps[route_key]
        return self.get_component(component_name)

    def _check_guards(self, route: List[str]) -> None:
        '''Runs and collects response from any applicable guards.

        Args:
            route (List[str]): The current route.
        '''
        # Place to put matching guard component (if found);
        component = None
        # First check the exit guards;
        for guarded_route_key in self._route_exit_guard_maps.keys():
            guarded_route = self._listify_route(guarded_route_key)
            if not set(guarded_route).issubset(set(self.route)):
                component = self.get_component(
                    self._route_exit_guard_maps[guarded_route_key])
        # Now check the entrance guards;
        for guarded_route_key in self._route_entrance_guard_maps.keys():
            guarded_route = self._listify_route(guarded_route_key)
            if set(guarded_route).issubset(self.route):
                component = self.get_component(
                    self._route_entrance_guard_maps[guarded_route_key])
        if component:
            self.clear_console()
            self._response = input(component.print())

    def register_component_package(self, package_path: str) -> None:
        self._component_packages.append(package_path)

    def make_component_active(self, component_name:str)->None:
        self._active_components.append(self.get_component(component_name))

    def get_component(self, name: str) -> 'ConsoleAppComponent':
        # First look inside initialised components;
        if name in self._components.keys():
            return self._components[name]
        # Not found, so create place to put constructor when found;
        constructor = None
        # Convert the PascalCase name to snake_case
        snake_name = self._utility_service.pascal_to_snake(name)
        # Then look in the default components;
        builtins_package = configs.builtin_component_package + '.{}'
        if importlib.util.find_spec(builtins_package.format(snake_name)):
            component_module = importlib.import_module(
                builtins_package.format(snake_name))
            constructor = getattr(component_module, name)
        # Then look in the registered component packages;
        for package_path in self._component_packages:
            if importlib.util.find_spec('{}.{}'.format(package_path, snake_name)):
                component_module = importlib.import_module('{}.{}'
                                                           .format(package_path, snake_name))
                constructor = getattr(component_module, name)
        # Instantiate the class and add it to the components dict;
        component: 'ConsoleAppComponent' = constructor()
        self._components[component.name] = component
        # Add the app reference to the component instance;
        component.app = self
        # Return the finished component;
        return component

    def add_root_route(self, route: List[str], component_name: str) -> None:
        self._root_route = route
        self.add_route(route, component_name)

    def add_route(self, route: List[str], component_name: str) -> None:
        self._route_component_maps[self._stringify_route(
            route)] = component_name

    def route_data(self, route:List[str]) -> RouteData:
        route_key = self._stringify_route(route)
        if route_key in self._route_data.keys():
            return self._route_data[route_key]

    def global_data(self) -> RouteData:
        pass

    def guard_entrance(self, route: List[str], component_name: str) -> None:
        route = self._complete_relative_route(route)
        self._route_entrance_guard_maps[self._stringify_route(route)] = \
            component_name

    def guard_exit(self, route: List[str], component_name: str) -> None:
        route = self._complete_relative_route(route)
        self._route_exit_guard_maps[self._stringify_route(route)] = \
            component_name

    def clear_entrance(self, route: List[str]) -> None:
        route = self._complete_relative_route(route)
        route_key = self._stringify_route(route)
        if route_key in self._route_entrance_guard_maps.keys():
            del self._route_entrance_guard_maps[route_key]

    def clear_exit(self, route: List[str]) -> None:
        route = self._complete_relative_route(route)
        route_key = self._stringify_route(route)
        if route_key in self._route_exit_guard_maps.keys():
            del self._route_exit_guard_maps[route_key]

    def process_response(self, response):
        '''First runs any matching active option responses. Then runs
        all active dynamic responses.

        Args:
            response (str): The user's response.
        '''
        # Collect the currently active option responses;
        active_option_responses = self._active_option_responses
        # If the response matches any static options;
        if response in active_option_responses.keys():
            active_option_responses[response]()
        # If not, run the dynamic responses;
        else:
            for component in self._active_components:
                component.dynamic_response(response)

    def run(self) -> None:
        '''Main run loop for the CLI
        '''
        # Enter the main loop;
        while not self._quit:
            # If response has been collected;
            if self._response:
                self.process_response(self._response)
                self._response = None
            # If we are drawing the next view;
            else:
                self._active_components = []
                # Check guards;
                self._check_guards(self.route)
                # If no guards collected a response;
                if not self._response:
                    component = self._get_component_for_route(self.route)
                    self.clear_console()
                    self._response = input(component.print())

    def navigate(self, route: List[str]) -> None:
        '''Changes the app's current route to the provided one.

        Args:
            route (List[str]): The route to change to.
        '''
        self.route = route

    def navigate_back(self):
        if len(self.route) > 1:
            self.navigate(self.route[0:-1])

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def quit(self):
        self._quit = True

    def set_window_text(self, text: str) -> None:
        try:
            self._textbox.configure(state='normal')
            self._textbox.delete('1.0', tk.END)
            self._textbox.insert(tk.END, text)
            self._textbox.configure(state='disabled')
            self._textbox.update()
        except TclError:
            self._configure_text_window()
            self.set_window_text(text)

    def show_text_window(self) -> None:
        try:
            self._text_window.deiconify()
        except TclError:
            self._configure_text_window()
            self.show_text_window()

    def hide_text_window(self) -> None:
        try:
            self._text_window.withdraw()
        except TclError:
            self.hide_text_window()
