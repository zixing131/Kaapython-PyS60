import kaapython
import ui

_ = kaapython.get_plugin_translator(__file__)
kaapython.app.settings.plugins.append('operations', ui.SettingsGroup(_('Operations')))
kaapython.app.settings.plugins.operations.append('style', ui.IntegerSetting(_('Font style (0-64)'), value=1, vmin=0, vmax=64))

class Selection:
    left = None
    right = None

def set_point():
    style = kaapython.app.settings.plugins.operations.style
    win = ui.screen.windows[0].body
    left, right = Selection.left, Selection.right
    if left is None:
        Selection.left = left = win.get_pos()
    elif right is None:
        Selection.right = right = win.get_pos()
        old_style = win.style
        win.style = style
        min_ = min(left,  right)
        win.apply(min_, max(left,  right) - min_)
        win.style = old_style
        Selection.left = Selection.right = None
    else:
        kaapython.notice(_('PluginError'))

def get_shortcuts(cls):
    menu = old_get_shortcuts()
    menu.append(ui.MenuItem(_('Set border'), target=set_point))
    return menu


old_get_shortcuts = kaapython.repattr(kaapython.TextWindow, 'get_shortcuts', classmethod(get_shortcuts))

 