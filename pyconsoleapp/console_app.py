import os
import tkinter as tk
import tkinter.scrolledtext as scrolledtext

class ConsoleApp():
    def __init__(self, name):
        self._routed_components = []
        self._quit = False
        self._route = []           
        self.name = name
        self.response = None
        self.terminal_width_chars = 60
        self.error_message = None
        self.info_message = None
        # Configure text window;
        self._tk_root = tk.Tk()  
        self._tk_root.geometry("500x1000")
        self._tk_root.title(name)
        self._text_window = scrolledtext.ScrolledText(self._tk_root)
        self._text_window.pack(expand=True, fill='both')
        self.hide_text_window() 

    @property
    def route(self):
        if self._route == []:
            return self._routed_components[0]['route']
        else:
            return self._route
    @route.setter
    def route(self, route):
        for routed_component in self._routed_components:
            stored_route = routed_component['route']
            if route == stored_route:
                self._route = route

    def _get_component_for_route(self, req_route):
        for routed_component in self._routed_components:
            route = routed_component['route']
            component = routed_component['component']
            if req_route == route:
                return component        

    def add_route(self, route, component):
        component.app = self
        component.set_component_app_ref(self)
        self._routed_components.append({
            'route': route,
            'component': component
        })

    def run(self):
        while not self._quit:
            component = self._get_component_for_route(self.route)
            self.clear_console()
            component.process_response(input(component))

    def navigate(self, req_route):
        self.route = req_route

    def navigate_back(self):
        if len(self.route) > 1:
            self.navigate(self.route[0:-1])

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def quit(self):
        self._quit = True
        
    def set_window_text(self, text):
        self._text_window.configure(state='normal')
        self._text_window.delete('1.0', tk.END)
        self._text_window.insert(tk.END, text)
        self._text_window.configure(state='disabled')
        self._tk_root.update()
        
    def show_text_window(self):
        self._tk_root.deiconify()
        
    def hide_text_window(self):
        self._tk_root.withdraw()        