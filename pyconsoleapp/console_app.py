import os
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import importlib
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from console_app_component import ConsoleAppComponent


class RoutedComponent():
    def __init__(self, route: [str], component: 'ConsoleAppComponent'):
        self.route = route
        self.component = component


class ConsoleApp():
    def __init__(self, name):
        self._routed_components: [RoutedComponent] = []
        self._components = {}
        self._quit = False
        self._route = []
        self._temp_child_output: str = None
        self._exit_guards: [RoutedComponent] = []
        self._entrance_guards: [RoutedComponent] = []
        self._response: str = None
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
    def route(self):
        if self._route == []:
            return self._routed_components[0].route
        else:
            return self._route

    @route.setter
    def route(self, route):
        for routed_component in self._routed_components:
            stored_route = routed_component.route
            if route == stored_route:
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

    def _get_component_for_route(self, req_route: [str]) -> 'ConsoleAppComponent':
        for routed_component in self._routed_components:
            route = routed_component.route
            component_name = routed_component.component
            if req_route == route:
                component = self.get_component(component_name)
                return component

    def register_component(self, name: str, component: 'ConsoleAppComponent'):
        component.app = self
        self._components[name] = component
        component.name = name

    def get_component(self, name: str)->'ConsoleAppComponent':
        if name in self._components.keys():
            self.active_components[name] = self._components[name]
            return self._components[name]
        else:  # Search in the default components.
            component_module = importlib.import_module('pyconsoleapp.components.{name}'
                                                       .format(name=name))
            component = getattr(component_module, name)
            self.active_components[name] = component
            self.register_component(name, component)
            return component

    def add_route(self, route, component_name):
        component = self.get_component(component_name)
        self._routed_components.append(RoutedComponent(route, component))

    def guard_exit(self, route: [str], component_name: str) -> None:
        component = self.get_component(component_name)
        self._exit_guards.append(RoutedComponent(route, component))

    def clear_exit(self, route: [str]) -> None:
        for guard in self._exit_guards:
            if guard.route == route:
                self._exit_guards.remove(guard)

    def process_response(self, response):
        for component in self.active_components.values():
            component.call_for_option_response(response)
        for component in self.active_components.values():
            component.call_for_dynamic_response(response)

    def run(self):
        while not self._quit:
            # If response has been collected;
            if self._response:
                self.process_response(self._response)
                self._response = None
            # If we are drawing the next view;
            else:
                self.active_components = {}
                # Check exit guards;
                for exit_guard in self._exit_guards:
                    if not set(exit_guard.route).issubset(set(self.route)):
                        component = exit_guard.component
                        self._response = input(component.run())
                        continue
                # Check entrance guards;
                for entrance_guard in self._entrance_guards:
                    if set(entrance_guard.route).issubset(set(self.route)):
                        component = entrance_guard.component
                        self._response = input(component.run())
                        continue
                # Not guarded, so go ahead to route;
                component = self._get_component_for_route(self.route)
                self.clear_console()
                self._response = input(component.run())

    def navigate(self, req_route: [str]) -> None:
        self.route = req_route

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
