import os
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import importlib
from typing import Dict, List, Any, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyconsoleapp.console_app_component import ConsoleAppComponent


class ConsoleApp():
    def __init__(self, name):
        self.name: str = name
        self._response: Optional[str] = None
        self._root_route: List[str]
        self._route: List[str] = []
        self._route_component_maps: Dict[str, str] = {}
        self._route_exit_guard_maps: Dict[str, str] = {}
        self._route_entrance_guard_maps: Dict[str, str] = {}
        self._components: Dict[str, 'ConsoleAppComponent'] = {}
        self._active_components: List['ConsoleAppComponent'] = []
        self._quit: bool = False
        self._temp_child_output: Optional[str] = None
        self._text_window: tk.Tk = self._config_text_window()
        self._textbox: scrolledtext.ScrolledText = self._config_textbox()
        self.terminal_width_chars: int = 60
        self.error_message: Optional[str] = None
        self.info_message: Optional[str] = None
        self.data: Dict[str, Any] = {}  # For storing any random data in;
        self.state: Dict[str, Any] = {}  # For storing additional app state in;

        # Hide the window that will have popped open;
        self.hide_text_window()

    @property
    def route(self) -> List[str]:
        if self._route == []:
            return self._root_route
        else:
            return self._route

    @route.setter
    def route(self, route: List[str]) -> None:
        # If the first element is '.';
        if route[0] == '.':
            # Route is relative, convert to absolute;
            route.pop(0)
            route = self._route+route
        # Set the route;
        if self._stringify_route(route) in self._route_component_maps.keys():
            self._route = route

    def _config_text_window(self) -> tk.Tk:
        '''Configures and returns Tkinter text window.
        '''
        text_window = tk.Tk()
        text_window.geometry("500x1000")
        text_window.title(self.name)
        return text_window

    def _config_textbox(self) -> scrolledtext.ScrolledText:
        textbox = scrolledtext.ScrolledText(self._text_window)
        textbox.pack(expand=True, fill='both')
        return textbox

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
        # Define helper to use guard;
        def collect_response(guarded_route_key: str) -> str:
            component = self.get_component(
                self._route_exit_guard_maps[guarded_route_key])
            self.clear_console()
            return input(self.run_component(component.name))
        # First check the exit guards;
        for guarded_route_key in self._route_exit_guard_maps.keys():
            guarded_route = self._listify_route(guarded_route_key)
            if not set(guarded_route).issubset(set(self.route)):
                self._response = collect_response(guarded_route_key)
                return
        # Now check the entrance guards;
        for guarded_route_key in self._route_entrance_guard_maps.keys():
            guarded_route = self._listify_route(guarded_route_key)
            if set(guarded_route).issubset(self.route):
                self._response = collect_response(guarded_route_key)
                return

    def register_component(self, name: str, component: 'ConsoleAppComponent'):
        component.app = self
        self._components[name] = component
        component.name = name

    def configure_component(self, component_name: str, configs: Dict) -> None:
        component = self.get_component(component_name)
        component.configure(configs)

    def get_component(self, name: str) -> 'ConsoleAppComponent':
        if name in self._components.keys():
            return self._components[name]
        else:  # Search in the default components.
            component_module = importlib.import_module('pyconsoleapp.components.{name}'
                                                       .format(name=name))
            component = getattr(component_module, name)
            self.register_component(name, component)
            return component

    def run_component(self, component_name: str) -> Optional[str]:
        component = self.get_component(component_name)
        self._active_components.append(component)
        component.responded_already = False
        return component.run()

    def add_root_route(self, route: List[str], component_name: str) -> None:
        self._root_route = route
        self.add_route(route, component_name)

    def add_route(self, route: List[str], component_name: str) -> None:
        self._route_component_maps[self._stringify_route(
            route)] = component_name

    def guard_exit(self, route: List[str], component_name: str) -> None:
        self._route_exit_guard_maps[self._stringify_route(
            route)] = component_name

    def clear_exit(self, route: List[str]) -> None:
        route_key = self._stringify_route(route)
        if route_key in self._route_exit_guard_maps.keys():
            del self._route_exit_guard_maps[route_key]

    def process_response(self, response):
        for component in self._active_components:
            component.process_response(response)

    def run(self) -> None:
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
                    self._response = input(self.run_component(component.name))

    def navigate(self, route: List[str]) -> None:
        self.route = route

    def navigate_back(self):
        if len(self.route) > 1:
            self.navigate(self.route[0:-1])

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def quit(self):
        self._quit = True

    def set_window_text(self, text):
        if not self._text_window:
            self._config_text_window()
        self._textbox.configure(state='normal')
        self._textbox.delete('1.0', tk.END)
        self._textbox.insert(tk.END, text)
        self._textbox.configure(state='disabled')
        self._textbox.update()

    def show_text_window(self):
        if not self._text_window:
            self._config_text_window()
        self._text_window.deiconify()

    def hide_text_window(self):
        if self._text_window:
            self._text_window.withdraw()
