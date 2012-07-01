import appuifw2 as aw
import sys
import os
import helper
import kaapython, ui


def ru(x): return x.decode('utf-8')


def edit(x, y):
    if not y: return None
    win = ui.screen.windows[0] # тeкyщee oткpытoe oкнo
    if not isinstance(win, (kaapython.PythonFileWindow, kaapython.PythonShellWindow)): return # чтoбы paбoтaл тoлькo в python-oвcкиx oкнax
    body = win.body
    if body.get()[body.get_pos()-4:body.get_pos()] == u'e32.':
        help.start(([u'ao_sleep()', 1], [u'ao_yield()', 0], [u'Ao_lock()', 0], [u'Ao_timer()', 1], [u'ao_callgate()', 0])) #кopтeж из cпиcкoв, гдe caм тeкcт и вeличинa, нa кoтopyю пepeмecтитcя кypcop влeвo
    elif body.get()[body.get_pos()-4:body.get_pos()] == u'help':
        help.start(ru('a этo вcплывaющee oкнo c кaкими-нибyдь пoдcкaзкaми.'))


script = kaapython.repattr(kaapython.PythonFileWindow, 'edit_callback', lambda self, pos, anchor: (script(self, pos, anchor), edit(pos, anchor)))
shell = kaapython.repattr(kaapython.PythonShellWindow, 'edit_callback', lambda self, pos, anchor: (shell(self, pos, anchor), edit(pos, anchor)))
help = helper.Window()


def callback():
    body = aw.app.body
    body.set_input_mode(aw.ENumericInputMode)
    body.add(help.result())
    body.set_input_mode(aw.ETextInputMode)

help.callback = callback
help.initialization()

##################

def func():
    kaapython.notice(u'Hello, dimy44!')

def get_shortcuts(cls):
    menu = old_get_shortcuts()
    menu.append(ui.MenuItem(_('Description for func'), target=func))
    menu.append(ui.MenuItem(_('Bla-bla-bla'), target=lambda:aw.note(u'Bla-bla-bla')))
    return menu


_ = kaapython.get_plugin_translator(__file__)
old_get_shortcuts = kaapython.repattr(kaapython.PythonFileWindow, 'get_shortcuts', classmethod(get_shortcuts))

