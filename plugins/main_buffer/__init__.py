
import appuifw2 as aw
import kaapython, ui

_ = kaapython.get_plugin_translator(__file__)
kaapython.app.settings.plugins.append('main_buffer', ui.SettingsGroup(_('Main buffer')))
kaapython.app.settings.plugins.main_buffer.append('length_of_history', ui.IntegerSetting(_('Length of history'), value=30, vmin=1, vmax=1000))

import main_buffer



buf = main_buffer.Buffer()

def get_shortcuts(cls):
    menu = old_get_shortcuts()
    menu.append(ui.MenuItem(_('main_buffer'), target=buf.startinfo))
    return menu

old_get_shortcuts = kaapython.repattr(kaapython.PythonFileWindow, 'get_shortcuts', classmethod(get_shortcuts))
