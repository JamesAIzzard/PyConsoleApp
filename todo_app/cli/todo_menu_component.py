from pyconsoleapp import Component
from todo_app import service

_main_view_template = '''{todos}
----------------------------------------------------------------------
-add, -a         [todo_item]  | -> Add a todo_item.
    --today                   | -> Flags as important.
    --importance [level: 1-3] | -> Describes the importance of a todo.
-remove, -r      [number]     | -> Remove a todo_item.
-edit, -e        [number]     | -> Edit a todo_item.
-dash                         | -> View todo_item dashboard.
----------------------------------------------------------------------
'''


class TodoMenuComponent(Component):

    def __init__(self, **kwds):
        super().__init__(**kwds)

        self.configure(state='home', printer=self.print_home_view, responders=[
            self.configure_responder(self.add_todo, args=[
                StdPrimaryArg(name='todo_item', markers=['-add', '-a']),
                ValuelessOptionArg(name='today', markers=['--today', '--t']),
                StdOptionArg(name='importance', markers=['--importance', '--i'], default_value=1,
                             validators=[pcap.validators.validate_integer,
                                         service.validate_importance_score])
            ]),
            self.configure_responder(self.remove_todo, args=[
                StdPrimaryArg(name='todo_num', markers=['-remove', '-r'], validators=[
                    self.todo_service.validate_todo_num
                ])
            ])
        ])

        self.configure_states(['home', 'dash'])

        # Configure home state;
        self.configure_printer(self.print_home_view, ['home'])
        self.configure_responder(self.add_todo, states=['home'], args=[
            self.configure_std_primary_arg(name='todo_item', markers=['-add', '-a']),
            self.configure_valueless_option_arg(name='today', markers=['--today', '--t']),
            self.configure_std_option_arg('importance', markers=['--importance', '--i'], default_value=1,
                                          validators=[pcap.validators.validate_integer,
                                                      service.validate_importance_score])
        ])
        self.configure_responder(self.remove_todo, states=['home'], args=[
            self.configure_std_primary_arg('todo_num', markers=['-remove', '-r'],
                                           validators=[self.todo_service.validate_todo_num])
        ])
        self.configure_responder(self.edit_todo, states=['home'], args=[
            self.configure_std_primary_arg('todo_num', markers=['-edit', '-e'],
                                           validators=[self.todo_service.validate_todo_num])
        ])
        self.configure_responder(self.change_state('dash'), states=['home'], args=[
            self.configure_valueless_primary_arg('dash', ['-dash'])
        ])

        # Configure dashboard state;
        self.configure_printer(self.print_dash_view, ['dash'])
        self.configure_responder(self.change_state('home'), states=['dash'], args=[
            self.configure_valueless_primary_arg('home', ['-home'])
        ])

    def print_home_view(self):
        # Build the todo_item list;
        if not len(self.todo_service.todos):
            todos_menu = pcap.styles.fore("No TODO's added yet.\n", 'blue')
        else:
            todos_menu = ''
            for i, todo in enumerate(self.todo_service.todos):
                todos_menu = todos_menu + format_todo(i + 1, todo)

        # Build the main page detail;
        output = _main_view_template.format(
            hr=self.app._get_cached_component('single_hr_component').print(),
            todos=todos_menu
        )

        # Return in the standard page;
        return self.app._get_cached_component('standard_page_component').print(
            page_title="TODOs",
            page_content=output
        )

    def print_dash_view(self):
        output = _dash_template.format(
            todo_count=len(self.todo_service.todos)
        )
        return self.app._get_cached_component('standard_page_component').print(
            page_title="Todo Dashboard",
            page_content=output
        )

    def add_todo(self, args) -> None:
        self.todo_service.add_todo(args['todo_item'], args['today'], args['importance'])

    def remove_todo(self, args) -> None:
        self.todo_service.remove_todo(args['todo_num'])

    def edit_todo(self, args) -> None:
        # Configure the editor component;
        tde = self.app._get_cached_component('todo_editor_component')
        tde = cast('TodoEditorComponent', tde)
        tde.subject = self.todo_service.fetch_todo(args['todo_num'])

        # Head to the editor;
        self.app.go_to('todos.edit')


_dash_view_template = '''
There are currently {todo_count} todo_item's.

-home                         -> Back to home.
'''
