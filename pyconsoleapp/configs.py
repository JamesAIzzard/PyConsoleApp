from typing import Any, Dict

default_configs = {
    'builtin_component_package': 'pyconsoleapp.builtin_components',
    'terminal_width_chars': 60
}


class Configurator():

    def __getattr__(self, name: str) -> Any:
        return default_configs[name]

    def __setattr__(self, name: str, value: Any) -> None:
        default_configs[name] = value

    def configure(self, configs:Dict[str, Any]):
        default_configs.update(configs)

configurator = Configurator()
