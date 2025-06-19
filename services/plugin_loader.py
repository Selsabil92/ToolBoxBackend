import importlib
import os

PLUGIN_FOLDER = "plugins"

def load_plugins():
    plugins = {}
    for file in os.listdir(PLUGIN_FOLDER):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]
            module = importlib.import_module(f"{PLUGIN_FOLDER}.{module_name}")
            plugins[module_name] = module
    return plugins
