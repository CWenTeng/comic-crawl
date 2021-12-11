import importlib
from util.logUtil import plugin_log

def init():
    global PLUGIN_DICT

    PLUGIN_DICT = {}

def get_plugin(site_name):
    if PLUGIN_DICT.get(site_name):
        return PLUGIN_DICT.get(site_name)
    else:
        reload_puglin(site_name)
    return PLUGIN_DICT.get(site_name)


# 重新载入插件
def reload_puglin(site_name):
    pluginName = "plugin." + site_name
    plugin_log.info(f"reloading......  {pluginName}")
    PLUGIN_DICT[site_name] = importlib.import_module(pluginName)

