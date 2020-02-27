import os
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import importlib
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from console_app_component import ConsoleAppComponent


class ConsoleApp():
    def __init__(self, name):
        self._response: str = None
        self._route: [str] = []        
        self._route_component_maps: Dict[str, str] = {}
        self._route_exit_guard_maps: Dict[str, str] = {}
        self._route_entrance_guard_maps: Dict[str, str] = {}
        self._components = {}
        self._quit = False
        self._temp_child_output: str = None
        self.active_components = {}
        self.name = name
        self.terminal_width_chars = 60
        self.error_message = None
        self.info_message = None
        self.data = {}  # For storing any random data in;
        self.state = {}  # For storing additional app state in;
        self._text_window: tk.Tk = None
        self._config_text_window()
        self._text_window.protocol(
            "WM_DELETE_WINDOW", self._on_text_window_close)

    @property
    def route(self) -> [str]:
        if self._route == []:
            return self._route_component_maps[0].route
        else:
            return self._route

    @route.setter
    def route(self, route: [str]) -> None:
        # If the first element is '.';
        if route[0] == '.':
            # Route is relative, convert to absolute;
            route.pop(0)
            route = self._route+route
        # Check the route exists;
        for routed_component in self._route_component_maps:
            if route == routed_component.route:
                # Set it, once confirmed exists;
                self._route = route

    @property
    def active_option_signatures(self):
        signatures = set()
        for component in self.active_components.values():
            for option in component.option_responses.keys():
                signatures.add(option)
        return signatures

    def _config_text_window(self) -> None:
        '''Configures Tkinter text window.
        '''
        self._text_window = tk.Tk()
        self._text_window.geometry("500x1000")
        self._text_window.title(self.name)
        self._textbox = scrolledtext.ScrolledText(self._text_window)
        self._textbox.pack(expand=True, fill='both')
        self.hide_text_window()

    def _on_text_window_close(self) -> None:
        self._text_window.destroy()
        self._text_window = None

    def _keyify_route(self, route: [str]) -> str:
        return route.join(">")

    def _get_component_for_route(self, route: [str]) -> 'ConsoleAppComponent':
        route_key = self._keyify_route(route)
        component_name = self._route_component_maps[route_key]
        return self.get_component(component_name)

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

    def add_route(self, route: [str], component_name: str) -> None:
        self._route_component_maps[self._keyify_route(route)] = component_name

    def guard_exit(self, route: [str], component_name: str) -> None:
        self._route_exit_guard_maps[self._keyify_route(route)] = component_name

    def clear_exit(self, route: [str]) -> None:
        for guard in self._exit_guards:
            if guard.route == route:
                self._exit_guards.remove(guard)

    def process_response(self, response):
        for component in self.active_components.values():
            component.call_for_option_response(response)
        for component in self.active_components.values():
            component.call_for_dynamic_response(response)

    def run(self) -> None:
        while not self._quit:
            # If response has been collected;
            if self._response:
                self.process_response(self._response)
                self._response = None
            # If we are drawing the next view;
            else:
                self.active_components = {}
                # Check guards;
                if self._route_entrance_guarded(self.route):
                    pass
                elif self._route_exit_guarded(self.route):
                    pass
                # Not guarded, so go ahead to route;
                else:
                    component = self._get_component_for_route(self.route)
                    self.clear_console()
                    self.active_components[component.name] = component
                    self._response = input(component.run())

                # Logic for entrance and exit guards;
                if _route_is_guarded(self.route):
                    for exit_guard in self._exit_guards:
                        if not set(exit_guard.route).issubset(set(self.route)):
                            component = self.get_component(
                                exit_guard.component_name)
                            self.clear_console()
                            self._response = input(component.run())
                    for entrance_guard in self._entrance_guards:
                        if set(entrance_guard.route).issubset(set(self.route)):
                            component = entrance_guard.component
                            self.clear_console()
                            self._response = input(component.run())

    def navigate(self, route: [str]) -> None:
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
