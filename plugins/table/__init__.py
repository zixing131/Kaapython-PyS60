
import appuifw2 as aw
import kaapython, ui
import table
import os
from graphics import Image
path = '%s\\' %os.path.dirname(table.__file__)

def func_table(x):
    body = aw.app.body
    body.set_input_mode(aw.ENumericInputMode)
    body.set_input_mode(aw.ETextInputMode)
    body.add(x[0])
    body.set_pos(body.get_pos() - x[1])

tb = table.Table(Image.open('%s1.png'%path), func_table, screen='normal')

tb.color_cursor = 0xff5500

tb.initialization()

def get_shortcuts(cls):
    menu = old_get_shortcuts()
    menu.append(ui.MenuItem(_('table'), target=tb.start_menu))
    return menu


_ = kaapython.get_plugin_translator(__file__)
old_get_shortcuts = kaapython.repattr(kaapython.PythonFileWindow, 'get_shortcuts', classmethod(get_shortcuts))

