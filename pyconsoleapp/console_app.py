import os
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import importlib
from typing import Callable, Dict, List, Optional, TYPE_CHECKING
from tkinter import TclError
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
        self._initialised_components: Dict[str, 'ConsoleAppComponent'] = {}
        self._pending_constructors: List[Callable] = []
        self._active_components: List['ConsoleAppComponent'] = []
        self._quit: bool = False
        self._temp_child_output: Optional[str] = None
        self._text_window: Optional[tk.Tk]
        self._textbox: Optional[ScrolledText]
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
        # First check the exit guards;
        for guarded_route_key in self._route_exit_guard_maps.keys():
            guarded_route = self._listify_route(guarded_route_key)
            if not set(guarded_route).issubset(set(self.route)):
                component = self.get_component(
                    self._route_exit_guard_maps[guarded_route_key])
                self.clear_console()
                self._response = input(self.run_component(component.name))
            return
        # Now check the entrance guards;
        for guarded_route_key in self._route_entrance_guard_maps.keys():
            guarded_route = self._listify_route(guarded_route_key)
            if set(guarded_route).issubset(self.route):
                component = self.get_component(
                    self._route_entrance_guard_maps[guarded_route_key])
                self.clear_console()
                self._response = input(self.run_component(component.name))
                return

    def _init_pending_components(self) -> None:
        # Loop through all constructors and instantiate;
        for constructor in self._pending_constructors:
            comp_name = constructor.__name__
            component = constructor()
            component.app = self
            self._initialised_components[comp_name] = component
        # Zero the list;
        self._pending_constructors = []

    def register_component(self, component_class: Callable):
        self._pending_constructors.append(component_class)

    def get_component(self, name: str) -> 'ConsoleAppComponent':
        # First look inside initialised components;
        if name in self._initialised_components.keys():
            return self._initialised_components[name]
        # Then look in the default components;
        else:
            component_module = importlib.import_module('pyconsoleapp.components.{name}'
                                                       .format(name=name))
            constructor = getattr(component_module, name)
            self.register_component(constructor)
            self._init_pending_components()
            return self._initialised_components[name]

    def run_component(self, component_name: str) -> Optional[str]:
        component = self.get_component(component_name)
        self._active_components.append(component)
        return component.run()

    def add_root_route(self, route: List[str], component_name: str) -> None:
        self._root_route = route
        self.add_route(route, component_name)

    def add_route(self, route: List[str], component_name: str) -> None:
        self._route_component_maps[self._stringify_route(
            route)] = component_name

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
        '''Instructs each component to process the response collected.
        
        Args:
            response (str): The user's response.
        '''
        for component in self._active_components:
            component.process_response(response)

    def run(self) -> None:
        '''Main run loop for the CLI
        '''
        # Create the component instances;
        self._init_pending_components()
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
