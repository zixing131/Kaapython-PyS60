import appuifw2 as aw
import sys
import os
import helper
import kaapython, ui

moduls = map(None, sys.builtin_module_names)
path = sys.path
path.append('e:\\sys\\bin\\')
path.append('c:\\sys\\bin\\')
path.append('f:\\sys\\bin\\')
 
for ii in path:
    try:
        files_mod = os.listdir(ii)
        for mod in files_mod:
            l=len(mod)
            if mod[l-4:l] == u'.pyc':moduls.append(mod[0:l-4])
            elif mod[l-3:l] == u'.py':moduls.append(mod[0:l-3])
            elif mod[l-4:l] == u'.pyd':moduls.append(mod[0:l-4])
    except:
        pass


def ru(x): return x.decode('utf-8')


def edit(self, pos, anchor):
    global moduls
    if anchor < 0: return None
    body = win.body
    pos = body.get_pos()
    if not isinstance(body, (kaapython.PythonFileWindow, kaapython.PythonShellWindow)): return
    text = body.get()
    exp = self._get_expression(text, pos)
    beg_of_line = max(text.rfind(u'\u2029', pos), 0)
    
    if help.runing == 1:
        if pos >= help.start_x:
            mask = text[help.start_x:pos]
            help.sort(mask)
        else:
            help.stop()
    elif text.lstrip()[beg_of_line:beg_of_line+7] == u'import ':
        help.start(moduls) 
    elif text[pos-1:pos] == u'.':
        try:
            mod_id = moduls.index(exp.encode('utf8'))
            try:
                mod = __import__(moduls[mod_id], globals(), globals())
                funcs = dir(mod)
                help.start(funcs)
            except Exception, info:
                ui.infopopup.show(_('Exception:\n%s') % info)
        except IndexError:
            if exp in globals(): help.start(dir(globals()[exp]))



script = kaapython.repattr(kaapython.PythonFileWindow, 'edit_callback', lambda self, pos, anchor: (script(self, pos, anchor), edit(self, pos, anchor)))
shell = kaapython.repattr(kaapython.PythonShellWindow, 'edit_callback', lambda self, pos, anchor: (shell(self, pos, anchor), edit(self, pos, anchor)))

move = kaapython.repattr(kaapython.PythonFileWindow, 'move_callback', lambda self: (move(self), edit(self, self.body.get_pos(), 0)))


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
    help.start(moduls)
    
def get_shortcuts(cls):
    menu = old_get_shortcuts()
    menu.append(ui.MenuItem(_("Forced autocompleten"), target=func))
    return menu


_ = kaapython.get_plugin_translator(__file__)
old_get_shortcuts = kaapython.repattr(kaapython.PythonFileWindow, 'get_shortcuts', classmethod(get_shortcuts))
