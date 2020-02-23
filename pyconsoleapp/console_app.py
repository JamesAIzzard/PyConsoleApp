import os

class ConsoleApp():
    def __init__(self, name):
        self._routed_pages = []
        self._quit = False
        self._route = []
        self.name = name
        self.response = None
        self.terminal_width_chars = 60

    @property
    def route(self):
        if self._route == []:
            return self._routed_pages[0]['route']
        else:
            return self._route
    @route.setter
    def route(self, route):
        for routed_page in self._routed_pages:
            stored_route = routed_page['route']
            if route == stored_route:
                self._route = route

    def _get_page_for_route(self, req_route):
        for routed_page in self._routed_pages:
            route = routed_page['route']
            page = routed_page['page']
            if req_route == route:
                return page        

    def add_route(self, route, page):
        page.app = self
        page.set_component_app_ref(self)
        self._routed_pages.append({
            'route': route,
            'page': page
        })

    def run(self):
        while not self._quit:
            page = self._get_page_for_route(self.route)
            self.clear_console()
            page.process_response(input(page))

    def navigate(self, req_route):
        self.route = req_route

    def navigate_back(self):
        if len(self.route) > 1:
            self.navigate(self.route[0:-1])

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def quit(self):
        self._quit = True