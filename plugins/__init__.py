import importlib
import pkgutil
from typing import Dict, Type


class BaseExtractor:
    def extract(self, content: str) -> dict:
        raise NotImplementedError("Extract method must be implemented")


def load_plugins() -> Dict[str, Type[BaseExtractor]]:
    plugins = {}
    package = __package__
    prefix = package + "."

    # 动态加载插件
    for loader, module_name, is_pkg in pkgutil.iter_modules(__path__, prefix):
        module = importlib.import_module(module_name)
        if hasattr(module, 'get_plugin'):
            plugin_instance = module.get_plugin()
            plugin_name = module_name.split('.')[-1]
            plugins[plugin_name] = plugin_instance

    return plugins


# 动态加载所有插件
available_plugins = load_plugins()